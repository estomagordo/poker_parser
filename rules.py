from collections import Counter
from itertools import combinations, permutations
from random import shuffle


def normalize(card):
    BROADWAYS = { 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12 }
    SUITS = { 'c': 0, 'd': 13, 'h': 26, 's': 39 }

    rank = card[0]
    suit = card[1]

    return (BROADWAYS[rank] if rank in BROADWAYS else int(rank) - 2) + SUITS[suit]


def denormalize(val):
    BROADWAYS = { 8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A' }
    SUITS = 'cdhs'

    rank = BROADWAYS[val % 13] if val % 13 in BROADWAYS else str((val % 13) + 2)
    suit = SUITS[val // 13]

    return rank + suit


def is_flush(hand):
    return len(set(card // 13 for card in hand)) == 1


def is_straight(hand):
    ranks = sorted([card % 13 for card in hand])

    if len(set(ranks)) < 5:
        return False

    return ranks[0] + 4 == ranks[4] or ranks == [0, 1, 2, 3, 12]


def score_high(hand):
    multiples = Counter(card % 13 for card in hand)
    ranks = tuple(sorted([card % 13 for card in hand], reverse=True))
    flush = is_flush(hand)
    straight = is_straight(hand)
    wheel = ranks == (12, 3, 2, 1, 0)
    reverse_count_order = [v[0] for v in multiples.most_common()]

    if flush and straight:
        if wheel:
            return (8, -1)
        return (8, max(ranks))
    elif any(multiples[rank] == 4 for rank in multiples):
        return (7, reverse_count_order[0], reverse_count_order[1])
    elif any(multiples[rank] == 3 for rank in multiples) and any(multiples[rank] == 2 for rank in multiples):
        return (6, reverse_count_order[0], reverse_count_order[1])
    elif flush:
        return (5, ranks)
    elif straight:
        if wheel:
            return (4, -1)
        return (4, max(ranks))
    elif any(multiples[rank] == 3 for rank in multiples):
        return (3, reverse_count_order[0], max(reverse_count_order[1:]), min(reverse_count_order[1:]))
    elif multiples[reverse_count_order[1]] == 2:
        return (2, max(reverse_count_order[:2]), min(reverse_count_order[:2]), reverse_count_order[2])
    elif any(multiples[rank] == 2 for rank in multiples):
        singles = list(reversed(reverse_count_order[1:]))
        return (1, reverse_count_order[0], singles[0], singles[1], singles[2])
    return (0, ranks)


def score_ace_to_five(cards):
    pass


def score_deuce_to_seven(cards):
    pass


def score_badugi(cards):
    pass


def hand_split(hand):
    return [hand[x:x + 2] for x in range(0, len(hand), 2)]


def score(hand, rules='high'):
    cards = hand_split(hand)
    normalized = list(map(normalize, cards))

    if rules == 'high':
        return score_high(normalized)
    elif rules == 'acetofive':
        return score_ace_to_five(normalized)
    elif rules == 'deucetoseven':
        return score_deuce_to_seven(normalized)
    elif rules == 'badugi':
        return score_badugi(normalized)


def score_holdem(hole, community):
    hole_cards = hand_split(hole)
    community_cards = hand_split(community)

    return max(score(''.join(hand)) for hand in combinations(hole_cards + community_cards, 5))


def score_omaha(hole, community):
    hole_cards = hand_split(hole)
    community_cards = hand_split(community)

    return max(score(''.join(hand_two + community_three)) for hand_two in combinations(hole_cards, 2) for community_three in combinations(community_cards, 3))


def icm(prizes, chips):
    COMBOS = [1, 2, 6, 24, 120, 720, 5040, 40320, 362880]

    player_count = len(chips)
    total_chips = sum(chips)
    values = [0.0] * player_count

    for p in permutations(range(player_count)):
        removed = 0
        cum_prob = 1.0

        for x, player in enumerate(p):
            if x == len(prizes):
                break

            probability = chips[player] / (total_chips - removed)
            cum_prob *= probability
            removed += chips[player]
            values[player] += cum_prob * prizes[x] / COMBOS[player_count - x - 2]

    return values


def sim(players, community, game='holdem'):
    SIM_LENGTH = 10000

    if not game == 'holdem':
        return #TODO

    if len(players) != 2:
        return #TODO

    norma = list(map(normalize, hand_split(players[0])))
    normb = list(map(normalize, hand_split(players[1])))
    normcom = [] if not community else list(map(normalize, hand_split(community)))
    
    remaining = [x for x in range(52) if x not in norma and x not in normb and x not in normcom]

    awin = 0
    bwin = 0
    draw = 0

    # runs = 0

    sh = {}

    def helper(hand):
        if hand in sh:
            return sh[hand]

        score = score_high(hand)
        sh[hand] = score

        return score

    # for x in range(SIM_LENGTH):
    for board in combinations(remaining, 5):
        # runs += 1
        # if runs % 10000 == 0:
        #     print(runs)
        lboard = list(board)
        # shuffle(remaining)
        # shufcom = normcom + remaining[:5 - len(normcom)]

        # ascore = max(score_high(c) for c in combinations(norma + shufcom, 5))
        # bscore = max(score_high(c) for c in combinations(normb + shufcom, 5))
        ascore = max(helper(c) for c in combinations(norma + lboard, 5))
        bscore = max(helper(c) for c in combinations(normb + lboard, 5))

        if ascore == bscore:
            draw += 1
        elif ascore > bscore:
            awin += 1
        else:
            bwin += 1
    # print(runs)
    return awin, bwin, draw, awin / SIM_LENGTH, bwin / SIM_LENGTH, draw / SIM_LENGTH, (awin + draw / 2.0) / SIM_LENGTH, (bwin + draw / 2.0) / SIM_LENGTH
# print(sim(['AdKc', '7d8s'], []))
for _ in range(3):
    import time
    now = time.time()
    print(sim(['QcJc', '4d4c'], []))
    print(time.time() - now)
    print()

def classify_two_player_matchup(a, b):
    a0rank = a[0] % 13
    a0suit = a[0] // 13
    a1rank = a[1] % 13
    a1suit = a[1] // 13
    b0rank = b[0] % 13
    b0suit = b[0] // 13
    b1rank = b[1] % 13
    b1suit = b[1] // 13

    return (
        a0rank == b0rank,
        a0suit == b0suit,
        a1rank == b1rank,
        a1suit == b1suit,
        a0rank == b1rank,
        a1rank == b0rank,
        a0suit == b1suit,
        a1suit == b0suit,
        a0rank,
        a1rank,
        b0rank,
        b1rank
        )
    # apair = a[0] == a[2]
    # bpair = b[0] == b[2]
    # asuited = a[1] == a[3]
    # bsuited = b[1] == b[3]

    # if apair:

    a, b = sorted((a, b))

    apair = a[0] % 13 == a[1] % 13
    asuits = {x // 13 for x in a}
    bpair = b[0] % 13 == b[1] % 13
    bsuits = {x // 13 for x in b}

    if apair:
        if bpair:
            if a[0] % 13 == b[0] % 13:
                return (0, a[0] % 13)
            return (1, a[0] % 13, b[0] % 13, len(asuits & bsuits))
        return (2, a[0] % 13, b[0] % 13, b[1] % 13, len(asuits & bsuits))
    if bpair:
        return (3, a[0] % 13, a[1] % 13, b[0] % 13, len(asuits & bsuits))
    if len(asuits) == 2:
        if len(bsuits) == 2:
            if len(asuits & bsuits) == 2:
                return (4, a[0] % 13, a[1] % 13, b[0] % 13, b[1] % 13)
            if len(asuits & bsuits) == 1:
                if a[0] // 13 == b[0] // 13:
                    return (5, a[0] % 13, a[1] % 13, b[0] % 13, b[1] % 13)
                if a[0] // 13 == b[1] // 13:
                    return (6, a[0] % 13, a[1] % 13, b[0] % 13, b[1] % 13)
                if a[1] // 13 == b[0] // 13:
                    return (7, a[0] % 13, a[1] % 13, b[0] % 13, b[1] % 13)
                return (8, a[0] % 13, a[1] % 13, b[0] % 13, b[1] % 13)
            return (9, a[0] % 13, a[1] % 13, b[0] % 13, b[1] % 13)
        if len(asuits & bsuits) == 1:
            if a[0] // 13 == b[0] // 13:
                return (10, a[0] % 13, a[1] % 13, b[0] % 13, b[1] % 13)
            return (11, a[0] % 13, a[1] % 13, b[0] % 13, b[1] % 13)
        return (12, a[0] % 13, a[1] % 13, b[0] % 13, b[1] % 13)
    if len(bsuits) == 2:
        if len(asuits & bsuits) == 1:
            if a[0] // 13 == b[0] // 13:
                return (13, a[0] % 13, a[1] % 13, b[0] % 13, b[1] % 13)
            return (14, a[0] % 13, a[1] % 13, b[0] % 13, b[1] % 13)
        return (15, a[0] % 13, a[1] % 13, b[0] % 13, b[1] % 13)
    if len(asuits & bsuits) == 1:
        return (16, a[0] % 13, a[1] % 13, b[0] % 13, b[1] % 13)
    return (17, a[0] % 13, a[1] % 13, b[0] % 13, b[1] % 13)

# classes = set()
# matchups = 0

# for c in combinations(range(52), 4):
#     for p in permutations(c, 2):
#         matchups += 1
#         a = list(p)
#         b = [n for n in c if n not in a]
#         # classes.add(classify_two_player_matchup(denormalize(a[0]) + denormalize(a[1]), denormalize(b[0]) + denormalize(b[1])))
#         classes.add(classify_two_player_matchup(sorted(a), sorted(b)))

# # print('\n'.join([str(c) for c in sorted(classes) if c[0] == 0]))
# print(len(classes))
# print(matchups)