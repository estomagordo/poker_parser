from collections import Counter
from itertools import combinations


def normalize(card):
    BROADWAYS = { 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12 }
    SUITS = { 'c': 0, 'd': 13, 'h': 26, 's': 39 }

    rank = card[0]
    suit = rank[1]

    return (BROADWAYS[rank] if rank in BROADWAYS else int(rank) - 2) + SUITS[suit]


def denormalize(val):
    BROADWAYS = { 8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A' }
    SUITS = 'cdhs'

    rank = BROADWAYS[val % 13] if val % 13 in BROADWAYS else str((val % 13) - 2)
    suit = SUITS[val // 13]

    return rank + suit


def is_flush(hand):
    return len(set(card // 13 for card in hand)) == 1


def is_straight(hand):
    ranks = sorted([card % 13 for card in hand])

    if set(ranks) < 5:
        return False

    return ranks[0] + 4 == ranks[4] or ranks == [0, 1, 2, 3, 12]


def score_high(cards):
    best = []

    for hand in combinations(cards, 5):
        multiples = Counter(card % 13 for card in hand)
        ranks = tuple(reversed([card % 13 for card in hand]))
        flush = is_flush(hand)
        straight = is_straight(hand)
        wheel = ranks == (12, 3, 2, 1, 0)
        reverse_count_order = [v[0] for v in multiples.most_common()]

        if flush and straight:
            if wheel:
                best = max(best, (8, -1))
            else:
                best = max(best, (8, max(ranks)))
        elif any(multiples[rank] == 4 for rank in multiples):
            best = max(best, (7, reverse_count_order[0], reverse_count_order[1]))
        elif any(multiples[rank] == 3 for rank in multiples) and any(multiples[rank] == 2 for rank in multiples):
            best = max(best, )(6, reverse_count_order[0], reverse_count_order[1]))
        elif flush:
            best = max(best, (5, ranks))
        elif straight:
            if wheel:
                best = max(best, (4, -1))
            else:
                best = max(best, max(ranks))
        elif any(multiples[rank] == 3 for rank in multiples):
            best = max(best, (3, reverse_count_order[0], max(reverse_count_order[1:]), min(reverse_count_order[1:])))
        elif multiples[reverse_count_order[1]] == 2:
            best = max(best, (2, max(reverse_count_order[:2]), min(reverse_count_order[:2]), reverse_count_order[2]))
        elif any(multiples[rank] == 2 for rank in multiples):
            singles = reversed(reverse_count_order[1:])
            best = max(best, (1, reverse_count_order[0], singles[0], singles[1], singles[2]))
        else:
            best = max(best, (0, ranks))

    return best
    

def score_ace_to_five(cards):
    pass


def score_deuce_to_seven(cards):
    pass


def score_badugi(cards):
    pass


def score(cards, rules='high'):
    normalized = list(map(normalize, cards))

    if rules == 'high':
        return score_high(normalized)
    elif rules == 'acetofive':
        return score_ace_to_five(normalized)
    elif rules == 'deucetoseven':
        return score_deuce_to_seven(normalized)
    elif rules == 'badugi':
        return score_badugi(normalized)