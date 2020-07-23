from rules import score


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