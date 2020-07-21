import time

from collections import defaultdict
from datetime import datetime, timedelta
from os import listdir
from sys import argv

import plot

from db import Db
from hand import Hand
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
    full = ''.join(''.join(line) for line in lines)

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
            flop = line[6][:-1] + line[7] + line[8]
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

        if line[3] == 'lost':
            deltas = line[4]
            if not deltas[-1].isdigit():
                deltas = deltas[:-1]

            before = after + int(deltas)
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
        full
        )
    
    return tournament_id, buyin_cents, rake_cents, hand


def parse_file(filename):
    tournaments = defaultdict(dict)

    handpart = []

    with open(filename) as f:
        for line in f.readlines():
            if line.strip():
                handpart.append(line.split())
            elif handpart:
                if handpart[1][7] == '(SNG' and handpart[1][11] == '$1.9' and handpart[1][13] == '$0.1)':
                    tournament_id, buyin_cents, rake_cents, hand = parse_hand(handpart)
                    tournaments[(tournament_id, buyin_cents, rake_cents)][hand.id] = hand
                handpart = []

    if handpart:
        if handpart[1][7] == '(SNG' and handpart[1][11] == '$1.9' and handpart[1][13] == '$0.1)':
            tournament_id, buyin_cents, rake_cents, hand = parse_hand(handpart)
            tournaments[(tournament_id, buyin_cents, rake_cents)][hand.id] = hand
    
    return tournaments


def to_percentage(f):
    return '%.2f' % (f * 100.0)


def produce_stats(tournobjs, elapsed):
    tournament_count = len(tournobjs)
    profit = 0.0
    wagered = 0.0
    cashes = 0
    win_streak = 0
    win_longest = 0
    lose_streak = 0
    lose_longest = 0
    first_time = 10**10
    last_time = 0

    for t in tournobjs:
        profit += t.hero_result_cents
        wagered += t.buyin_cents + t.rake_cents

        first_time = min(first_time, t.start_time)
        last_time = max(last_time, t.start_time)

        if t.hero_result_cents > 0.0:
            cashes += 1
            win_streak += 1
            lose_longest = max(lose_longest, lose_streak)
            lose_streak = 0
        else:
            win_longest = max(win_longest, win_streak)
            win_streak = 0
            lose_streak += 1

    win_longest = max(win_longest, win_streak)
    lose_longest = max(lose_longest, lose_streak)

    roi = ((profit + wagered) / wagered) - 1.0
    formated_profit = '%.2f' % (profit / 100.0)

    first_start = parse_timestamp(first_time)
    last_start = parse_timestamp(last_time)

    print(f'Found {tournament_count} tournaments in {elapsed} seconds.')
    print(f'The first one started at: {first_start}')
    print(f'The last one started at: {last_start}')
    print(f'Cashed in {cashes} ({to_percentage(cashes / tournament_count)}%)')
    print(f'Made a profit of ${formated_profit} (ROI {to_percentage(roi)}%)')
    print(f'Longest win streak: {win_longest}. Longest lose streak: {lose_longest}.')


def update_database(tournobjs):
    db = Db()
    db.create_if_needed()
    
    for tournament in tournobjs:
        db.upsert_tournament(tournament)
        for hand in tournament.hands:
            db.upsert_hand(hand)

    db.close()


def main():
    start_time = time.time()

    mode, path = argv[1], argv[2]

    tournaments = {}
    
    if mode == 'f':
        tournaments = dict(tournaments,  **parse_file(path))
    elif mode == 'd':
        for filename in listdir(path):
            if filename.endswith('txt'):
                parsed_tournaments = parse_file(filename)
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

    produce_stats(tournobjs, elapsed)
    update_database(tournobjs)

    plot.plot_tournaments(tournobjs, 'results.svg')

if __name__ == '__main__':
    main()