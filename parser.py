from datetime import datetime, timedelta

from hand import Hand


def parse_datetime(s):
    EDT = 'EDT'
    UTC = 'UTC'
    DATE_FORMAT = '%a %b %d %H:%M:%S %Z %Y'
    time_diff = 4

    dt = datetime.strptime(s.replace(EDT, UTC), DATE_FORMAT)

    return int((dt + timedelta(hours=time_diff)).timestamp())


def parse_cents(s):
    if '.' not in s:
        return 100 * int(s)

    dollars, cents = list(map(int, s.split('.')))

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
            before = after + int(line[4])
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
                        hero_before, hero_after, _ = extract_player_info(line)
                    else:
                        villain_pos = (i - hero_line - 1) % (player_count - 1)
                        
                        if i < hero_line:
                            villain_pos = (player_count - 1) + i - hero_line

                        villains[villain_pos] = extract_player_info(line)
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