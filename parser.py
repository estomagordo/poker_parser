import time

from collections import defaultdict
from datetime import datetime, timedelta
from os import listdir
from sys import argv

import plot

from db import Db
from hand import Hand
from rules import calculate_hero_evs
from tournament import Tournament


def parse_datetime(s):
    EDT = 'EDT'
    UTC = 'UTC'
    DATE_FORMAT = '%a %b %d %H:%M:%S %Z %Y'
    TIME_DIFF = 4

    dt = datetime.strptime(s.replace(EDT, UTC), DATE_FORMAT)

    return int((dt + timedelta(hours=TIME_DIFF)).timestamp())


def parse_timestamp(n):
    SHORT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    TIME_DIFF = 4 * 3600

    return time.strftime(SHORT_DATE_FORMAT, time.gmtime(n + TIME_DIFF))


def parse_cents(s):
    if '.' not in s:
        return 100 * int(s)

    if not s[-1].isdigit():
        s = s[:-1]

    parts = s.split('.')
    dollars, cents = list(map(int, parts))
    if len(parts[1]) == 1:
        cents *= 10

    return 100 * dollars + cents


def get_evs(lines, hero_cards, villains, hero_after):
    cEV, icmEV, actual_chips, actual_icm = -1, -1, -1, -1

    return cEV, icmEV, actual_chips, actual_icm # Rather than properly separating it, for now.
      
    hero_ai = any('Hero is all-In.' in ' '.join(line) for line in lines)

    if hero_ai:
        ai = []
        
        for line in lines:
            if 'is all-In.' in ' '.join(line):
                ai.append(line[0])
            if 'Dealing Flop' in ' '.join(line):
                break

        if len(ai) == 2:          
            hero_2way_ai = True
            hero_2way_ai_street = 0
            villain = [p for p in ai if p != 'Hero'][0]

            for line in lines[::-1]:
                if line[0] == villain:
                    hero_2way_ai_opponent_hand = line[9][:-1] + line[10]
                    break

            for line in lines:
                if line[0] == 'Main':
                    hero_2way_ai_pot_size = int(line[2])
                    break

            villain_cards = ''

            for line in lines:
                if line[1] == 'balance' and line[0] == villain:
                    villain_cards = line[9][:-1] + line[10] if line[9][-1] == ',' else line[5][:-1] + line[6]
                    break
            
            hands = [hero_cards, villain_cards]
            stacks = [hero_after] + [v[1] for v in villains]
            first_in_pos = True #Obviously have to do this for real later
            actual = 1

            for line in lines:
                if line[1] == 'balance':
                    if line[0] == 'Hero':
                        actual -= any('+' in part for part in line)
                    elif line[0] == villain:
                        actual += any('+' in part for part in line)

            cEV, icmEV, actual_chips, actual_icm = calculate_hero_evs(hands, hero_2way_ai_pot_size, stacks, [380, 380, 380], first_in_pos, actual)

    return cEV, icmEV, actual_chips, actual_icm


def parse_hand(lines):
    hand_id = lines[0][5]
    blinds = lines[1][0]
    sb, bb = list(map(int, blinds.split('/')))
    ante = int(lines[10][-1][1:-1])
    tournament_id = lines[1][9][1:-1]
    buyin_cents = parse_cents(lines[1][11][1:])
    rake_cents = parse_cents(lines[1][13][1:])
    time = parse_datetime(' '.join(lines[1][-6:]))
    player_count = int(lines[3][-1].split('/')[0])
    full = '\n'.join(' '.join(line) for line in lines)

    villains = [[-1, -1, '']] * 9
    hero_cards = None
    flop = None
    turn = None
    river = None
    hero_before = -1
    hero_after = -1

    for line in lines:
        if len(line) < 3:
            continue
        if line[:2] == ['Dealt', 'to', 'Hero']:
            hero_cards = line[4][:-1] + line[5]
        elif line[2] == 'Flop':
            flop = line[6][:-1] + line[7][:-1] + line[8]
        elif line[2] == 'Turn':
            turn = line[6]
        elif line[2] == 'River':
            river = line[6]

    button_pos = lines[2][-4]
    button_line = -1
    hero_line = -1

    for x in range(player_count):
        if lines[4 + x][1][0] == button_pos:
            button_line = x
            break

    for x in range(player_count):
        if lines[4 + x][2] == 'Hero':
            hero_line = x
            break

    hero_pos = (hero_line + player_count - 1 - button_line) % player_count

    def extract_player_info(line):
        after = int(line[2][:-1])
        before = -1
        hand = ''

        for x, part in enumerate(line):
            if part == 'lost':
                deltas = line[x + 1]
                if not deltas[-1].isdigit():
                    deltas = deltas[:-1]

                before = after + int(deltas)
                break
        else:
            for part in line:
                if part[0] == '+':
                    if part[-1] == '[':
                        before = after - int(part[1:-1])
                    else:
                        before = after - int(part[1:])
                    break

        for x, part in enumerate(line):
            if part[-1] == '[':
                hand = line[x + 1][:-1] + line[x + 2]
                break

        return before, after, hand

    for x, line in enumerate(lines):
        if line[1] == 'balance':
            for i in range(player_count):
                if i == hero_line:
                    hero_before, hero_after, _ = extract_player_info(lines[x + i])
                else:
                    villain_pos = (i - hero_line - 1) % (player_count - 1)
                    
                    if i < hero_line:
                        villain_pos = (player_count - 1) + i - hero_line

                    villains[villain_pos] = extract_player_info(lines[x + i])
            break

    if not hero_cards:
        for line in lines:
            if line[:3] == ['Dealt', 'to', 'Hero']:
                hero_cards = line[4][:-1] + line[5]
                break

    hero_2way_ai = False
    hero_2way_ai_street = None
    hero_2way_ai_opponent_hand = None
    hero_2way_ai_pot_size = None
    hero_2way_ai_cevdiff = None
    hero_2way_ai_icmevdiff = None

    cEV, icmEV, actual_chips, actual_icm = get_evs(lines, hero_cards, villains, hero_after)
    
    hand = Hand(
        hand_id,
        time,
        tournament_id,
        sb,
        bb,
        ante,
        hero_pos,
        player_count,
        hero_before,
        hero_after,
        hero_cards,
        villains,
        flop,
        turn,
        river,
        hero_2way_ai,
        hero_2way_ai_street,
        hero_2way_ai_opponent_hand,
        hero_2way_ai_pot_size,
        hero_2way_ai_cevdiff,
        hero_2way_ai_icmevdiff,
        cEV,
        icmEV,
        actual_chips,
        actual_icm,
        full
        )
    
    return tournament_id, buyin_cents, rake_cents, hand, cEV, icmEV, actual_chips, actual_icm


def parse_file(filename):
    print('Parsing', filename)
    tournaments = defaultdict(dict)

    totCEV = 0.0
    totICMEV = 0.0
    counter = 0

    handpart = []

    with open(filename) as f:
        for line in f.readlines():
            if line.strip():
                handpart.append(line.split())
            elif handpart:
                sng = handpart[1][7] == '(SNG'
                two = handpart[1][11] == '$1.9' and handpart[1][13] == '$0.1)'
                five = handpart[1][11] == '$4.8' and handpart[1][13] == '$0.2)'
                if sng and (two or five):
                    tournament_id, buyin_cents, rake_cents, hand, cEV, icmEV, actual_chips, actual_icm = parse_hand(handpart)
                    if actual_chips > -1:
                        counter += 1
                        totCEV += (actual_chips - cEV)
                        totICMEV += (actual_icm - icmEV)
                        print(f'Hand number {counter}. Chip EV: {totCEV}. ICM EV: {totICMEV}')
                    tournaments[(tournament_id, buyin_cents, rake_cents)][hand.id] = hand
                handpart = []

    if handpart:
        sng = handpart[1][7] == '(SNG'
        two = handpart[1][11] == '$1.9' and handpart[1][13] == '$0.1)'
        five = handpart[1][11] == '$4.8' and handpart[1][13] == '$0.2)'
        if sng and (two or five):
            tournament_id, buyin_cents, rake_cents, hand, cEV, icmEV, actual_chips, actual_icm = parse_hand(handpart)
            if actual_chips > -1:
                        counter += 1
                        totCEV += (actual_chips - cEV)
                        totICMEV += (actual_icm - icmEV)
                        print(f'Hand number {counter}. Chip EV: {totCEV}. ICM EV: {totICMEV}')
            tournaments[(tournament_id, buyin_cents, rake_cents)][hand.id] = hand
    
    return tournaments


def to_percentage(f):
    return '%.2f' % (f * 100.0)


def sessionize(tournaments):
    sessions = []
    session = []

    for tournament in tournaments:
        if not session:
            session.append(tournament)
        elif session[-1].end_time > tournament.start_time:
            session.append(tournament)
        else:
            sessions.append(session)
            session = [tournament]

    sessions.append(session)

    return sessions


def produce_stats(tournaments):
    tournament_count = len(tournaments)
    profit = 0.0
    wagered = 0.0
    cashes = 0
    win_streak = 0
    win_longest = 0
    lose_streak = 0
    lose_longest = 0
    first_time = 10**10
    last_time = 0
    biggest_recovery = 10**10
    biggest_throwaway = 0
    buyins = {}

    for t in tournaments:
        profit += t.hero_result_cents
        cost = t.buyin_cents + t.rake_cents
        wagered += cost

        if cost not in buyins:
            buyins[cost] = [0, 0.0]

        buyins[cost][0] += 1
        buyins[cost][1] += t.hero_result_cents

        first_time = min(first_time, t.start_time)
        last_time = max(last_time, t.end_time)

        if t.hero_result_cents > 0.0:
            cashes += 1
            win_streak += 1
            lose_longest = max(lose_longest, lose_streak)
            lose_streak = 0
        else:
            win_longest = max(win_longest, win_streak)
            win_streak = 0
            lose_streak += 1
        
        highest = 0
        lowest = 10**10

        for x, hand in enumerate(t.hands):
            highest = max(highest, hand.hero_after)
            
            if x < len(t.hands) - 1:
                lowest = min(lowest, hand.hero_after)

        if t.hero_result_cents > 0:
            biggest_recovery = min(biggest_recovery, lowest)
        else:
            biggest_throwaway = max(biggest_throwaway, highest)

    win_longest = max(win_longest, win_streak)
    lose_longest = max(lose_longest, lose_streak)

    roi = ((profit + wagered) / wagered) - 1.0
    formated_profit = '%.2f' % (profit / 100.0)
    result = 'profit' if profit >= 0.0 else 'loss'

    first_start = parse_timestamp(first_time)
    last_end = parse_timestamp(last_time)

    print(f'The first one started at: {first_start}')
    print(f'The last one ended at: {last_end}')
    print(f'Cashed in {cashes} ({to_percentage(cashes / tournament_count)}%)')
    print(f'Made a {result} of ${formated_profit} (ROI {to_percentage(roi)}%)')
    print(f'Longest win streak: {win_longest}. Longest lose streak: {lose_longest}.')
    print(f'The biggest comeback came from {biggest_recovery} and the biggest throwaway came from {biggest_throwaway}.')
    print('Per buyin results:')
    for k, v in buyins.items():
        buyin = '%.2f' % (k / 100.0)
        number = v[0]
        result = '%.2f' % (v[1] / 100.0)
        print(f'${buyin}: {result} in {number} played.')


def handle_stats(tournaments, full_stats):    
    if full_stats:
        print()

        sessions = sessionize(tournaments)

        print(f'Found {len(sessions)} different sessions.')

        print('Session data:\n')

        for x, session in enumerate(sessions):
            print(f'Session #{x + 1} lasted for {round((session[-1].end_time - session[0].start_time) / 60.0, 2)} minutes.')
            print(f'It contained {len(session)} tournaments.')
            produce_stats(session)
            print()

    produce_stats(tournaments)


def update_database(tournobjs):
    db = Db()
    db.create_if_needed()
    
    for tournament in tournobjs:
        db.upsert_tournament(tournament)
        for hand in tournament.hands:
            db.upsert_hand(hand)

    db.commmit_and_close()


def main():
    start_time = time.time()

    mode, path = argv[1], argv[2]
    use_db = len(argv) > 3 and argv[3] == 'write'
    full_stats = len(argv) > 4 and argv[4] == 'full'

    tournaments = {}
    
    if mode == 'f':
        tournaments = dict(tournaments,  **parse_file(path))
    elif mode == 'd':
        for filename in listdir(path):
            if filename.endswith('txt') and filename != 'requirements.txt':
                parsed_tournaments = parse_file(path + '//' + filename)
                for k, v in parsed_tournaments.items():
                    if k not in tournaments:
                        tournaments[k] = v
                    else:
                        for hand_id in v.keys():
                            if hand_id not in tournaments[k]:
                                tournaments[k][hand_id] = v[hand_id]

    tournobjs = []
    
    for k, v in tournaments.items():
        tournament_id, buyin_cents, rake_cents = k
        tournament = Tournament(tournament_id, buyin_cents, rake_cents, list(v.values()))
        tournament.finalize()
        tournobjs.append(tournament)

    tournobjs.sort(key=lambda t: t.start_time)

    elapsed = '%.2f' % (time.time() - start_time)
    print(f'Found {len(tournobjs)} tournaments in {elapsed} seconds.')

    if tournobjs:
        handle_stats(tournobjs, full_stats)

    if use_db:
        update_database(tournobjs)

    plot.plot_tournaments(tournobjs, 'plots//results.svg')

if __name__ == '__main__':
    main()