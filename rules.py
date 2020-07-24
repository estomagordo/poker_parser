from collections import Counter


def normalize(card):
    BROADWAYS = { 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12 }
    SUITS = { 'c': 0, 'd': 13, 'h': 26, 's': 39 }

    rank = card[0]
    suit = card[1]

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