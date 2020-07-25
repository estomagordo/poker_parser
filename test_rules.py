from math import isclose

from rules import icm, score, score_holdem, score_omaha


def test_straight_flushes():
    royal_clubs = 'AcJcTcQcKc'
    royal_diamonds = 'AdKdQdTdJd'
    middle_sflush = '9s8s7s6s5s'
    wheel_sflush = 'Ah2h4h5h3h'

    assert(score(royal_clubs) == score(royal_diamonds))
    assert(score(royal_clubs) > score(middle_sflush))
    assert(score(middle_sflush) > score(wheel_sflush))
    assert(score(royal_diamonds) > score(wheel_sflush))


def test_quads():
    eights_with_ten = '8c8d8h8sTd'
    eights_with_jack = '8c8d8h8sJh'
    aces = 'AdAhAsAc7h'
    aces_same_value_kicker = 'AdAsAhAc7s'

    assert(score(eights_with_ten) < score(eights_with_jack))
    assert(score(aces) > score(eights_with_jack))
    assert(score(aces) == score(aces_same_value_kicker))


def test_boats():
    tens_over_kings = 'TdTsThKdKc'
    deuces_over_aces = '2d2c2hAhAd'
    tens_over_fours = 'TdThTs4s4h'
    tens_over_other_fours = 'TdThTs4d4c'

    assert(score(tens_over_kings) > score(tens_over_fours))
    assert(score(tens_over_fours) > score(deuces_over_aces))
    assert(score(tens_over_fours) == score(tens_over_other_fours))


def test_flushes():
    wheel_sflush = 'Ah2h4h5h3h'
    nutty_hearts = 'AhKhQhJh9h'
    nutty_clubs = 'AcKcQcJc9c'
    king_n_crap = 'Kd7d6d4d2d'
    queen_good = 'QsJsTs8s7s'

    assert(score(wheel_sflush) > score(nutty_hearts))
    assert(score(nutty_hearts) == score(nutty_clubs))
    assert(score(nutty_clubs) > score(king_n_crap))
    assert(score(king_n_crap) > score(queen_good))


def test_straights():
    broadway = 'AcKdQsJhTh'
    other_broadway = 'AcKdQdJcTh'
    middling = 'JsTs9h8d7c'
    six_high = '6h5s4d3d2h'
    wheel = 'Ad2s3s4s5c'

    assert(score(broadway) > score(middling))
    assert(score(broadway) == score(other_broadway))
    assert(score(middling) > score(six_high))
    assert(score(six_high) > score(wheel))


def test_trips():
    trip_queens = 'QdQcQhJd4s'
    trip_jacks = 'JcJdJhAcKd'
    other_trip_jacks = 'JhJdJcAc6d'
    same_other_trip_jacks = 'JsJdJcAs6s'

    assert(score(trip_queens) > score(trip_jacks))
    assert(score(trip_jacks) > score(other_trip_jacks))
    assert(score(other_trip_jacks) == score(same_other_trip_jacks))


def test_two_pair():
    aces_up = 'AhAd7c7d4s'
    other_aces_up = 'AsAc6s6dKc'
    tens_deuces = 'TdTs2h2c4d'
    nines_eights = '9c9d8h8s4s'
    same_nines_eights = '9h9s8d8c4d'

    assert(score(aces_up) > score(other_aces_up))
    assert(score(aces_up) > score(tens_deuces))
    assert(score(tens_deuces) > score(nines_eights))
    assert(score(nines_eights) == score(same_nines_eights))


def test_one_pair():
    jacks = 'JdJc7h3d2h'
    eights = '8d8hAcKdTs'
    same_eights = '8s8cAdKsTd'

    assert(score(jacks) > score(eights))
    assert(score(eights) == score(same_eights))


def test_no_hand():
    royal_sampler = 'AcKdQsJd9h'
    other_royal_sampler = 'AdKhQhJs9d'
    meh = 'Jd8h7s4s2h'

    assert(score(royal_sampler) == score(other_royal_sampler))
    assert(score(royal_sampler) > score(meh))


def test_between_hand_types():
    worst_sflush = 'As2s3s4s5s'
    best_quads = 'AdAhAcAsKh'
    worst_quads = '2s2d2h2c3c'
    best_boat = 'AcAdAhKcKh'
    worst_boat = '2c2d2h3c3h'
    best_flush = 'AsKsQsJs9s'
    worst_flush = '7d5d4d3d2d'
    best_straight = 'AcKcQdJhTs'
    worst_straight = 'Ah2h3c4h5d'
    best_trips = 'AcAdAhKhQd'
    worst_trips = '2c2d2h3s4h'
    best_two_pair = 'AhAdKhKsQd'
    worst_two_pair = '2h2s3h3c4s'
    best_one_pair = 'AhAcKhQhJd'
    worst_one_pair = '2h2c3h4d5c'
    best_high_card = 'AhKcQdJs9d'

    assert(score(worst_sflush) > score(best_quads))
    assert(score(worst_quads) > score(best_boat))
    assert(score(worst_boat) > score(best_flush))
    assert(score(worst_flush) > score(best_straight))
    assert(score(worst_straight) > score(best_trips))
    assert(score(worst_trips) > score(best_two_pair))
    assert(score(worst_two_pair) > score(best_one_pair))
    assert(score(worst_one_pair) > score(best_high_card))


def test_holdem_scoring():
    aces = 'AdAh'
    other_aces = 'AsAc'
    jackten = 'JsTc'
    suitdiscon = '9d7d'

    board_a = 'JhKdQc4s4c'
    board_b = '6d5d4d3d2d'
    board_c = 'KsJs9s4s2s'
    board_d = 'JdTs4c4d8h'

    assert(score_holdem(aces, board_a) == score('AdAhKd4s4c'))
    assert(score_holdem(aces, board_a) == score_holdem(other_aces, board_a))
    assert(score_holdem(aces, board_b) == score_holdem(other_aces, board_b))
    assert(score_holdem(aces, board_c) < score_holdem(other_aces, board_c))
    assert(score_holdem(jackten, board_d) == score('JsJdTcTs8h'))
    assert(score_holdem(suitdiscon, board_b) > score_holdem(aces, board_b))
    assert(score_holdem(suitdiscon, board_d) == score('JdTs9d8h7d'))


def test_omaha_scoring():
    aces = 'AdAcKc7c'
    random = 'Jc9d4d4c'
    pizza_special = 'KdKhKcKs'
    low_con = '6d5h4d3h'

    board_a = 'Ah9h9s4s2d'
    board_b = 'Qc8c5c5s5d'
    board_c = 'JdJs7d7h2h'

    assert(score_omaha(aces, board_a) == score('AdAcAh9h9s'))
    assert(score_omaha(aces, board_b) == score('AdAc5c5s5d'))
    assert(score_omaha(aces, board_c) == score('Ad7cJd7d7h'))
    assert(score_omaha(random, board_a) == score('9d4d9h9s4s'))
    assert(score_omaha(random, board_b) == score('4d4c5c5s5d'))
    assert(score_omaha(random, board_c) == score('Jc9dJdJs7d'))
    assert(score_omaha(pizza_special, board_a) == score('KhKsAh9h9s'))
    assert(score_omaha(pizza_special, board_b) == score('KdKs5c5s5d'))
    assert(score_omaha(pizza_special, board_c) == score('KcKdJdJs7d'))
    assert(score_omaha(low_con, board_a) == score('5h3hAh4s2d'))
    assert(score_omaha(low_con, board_b) == score('6d5h5s5c5d'))
    assert(score_omaha(low_con, board_c) == score('6d5hJdJs7d'))


def test_icm():
    prizes_a = [84, 36]
    prizes_b = [50, 30, 20]
    prizes_c = [100]
    prizes_d = [50, 50, 50]
    prizes_e = [50, 50, 50, 50, 50]

    stacks_a = [4500, 2700, 1800]
    stacks_b = [100, 80, 25, 120, 55, 28]
    stacks_c = [52, 13, 35]
    stacks_d = [1200, 250, 220, 1330]
    stacks_e = [2000, 500, 100, 2900, 1400, 2200, 1100]

    icm_a = icm(prizes_a, stacks_a)
    icm_b = icm(prizes_b, stacks_b)
    icm_c = icm(prizes_c, stacks_c)
    icm_d = icm(prizes_d, stacks_d)
    icm_e = icm(prizes_e, stacks_e)

    assert(isclose(icm_a[0], 54.21, abs_tol=0.01))
    assert(isclose(icm_a[1], 38.7, abs_tol=0.01))
    assert(isclose(icm_a[2], 27.09, abs_tol=0.01))

    assert(isclose(icm_b[0], 23.50, abs_tol=0.01))
    assert(isclose(icm_b[1], 20.05, abs_tol=0.01))
    assert(isclose(icm_b[2], 7.21, abs_tol=0.01))
    assert(isclose(icm_b[3], 26.42, abs_tol=0.01))
    assert(isclose(icm_b[4], 14.79, abs_tol=0.01))
    assert(isclose(icm_b[5], 8.03, abs_tol=0.01))

    assert(isclose(icm_c[0], 52.0, abs_tol=0.01))
    assert(isclose(icm_c[1], 13.0, abs_tol=0.01))
    assert(isclose(icm_c[2], 35.0, abs_tol=0.01))

    assert(isclose(icm_d[0], 48.02, abs_tol=0.01))
    assert(isclose(icm_d[1], 28.37, abs_tol=0.01))
    assert(isclose(icm_d[2], 25.22, abs_tol=0.01))
    assert(isclose(icm_d[3], 48.4, abs_tol=0.01))

    assert(isclose(icm_e[0], 46.04, abs_tol=0.01))
    assert(isclose(icm_e[1], 22.54, abs_tol=0.01))
    assert(isclose(icm_e[2], 5.07, abs_tol=0.01))
    assert(isclose(icm_e[3], 48.25, abs_tol=0.01))
    assert(isclose(icm_e[4], 42.41, abs_tol=0.01))
    assert(isclose(icm_e[5], 46.74, abs_tol=0.01))
    assert(isclose(icm_e[6], 38.96, abs_tol=0.01))

    assert(isclose(sum(prizes_a), sum(icm_a), abs_tol=0.01))
    assert(isclose(sum(prizes_b), sum(icm_b), abs_tol=0.01))
    assert(isclose(sum(prizes_c), sum(icm_c), abs_tol=0.01))
    assert(isclose(sum(prizes_d), sum(icm_d), abs_tol=0.01))
    assert(isclose(sum(prizes_e), sum(icm_e), abs_tol=0.01))