from rules import score_high


def test_straigh_flushes():
    royal_clubs = 'AcJcTcQcKc'
    royal_diamonds = 'AdKdQdTdJd'
    middle_sflush = '9s8s7s6s5s'
    wheel_sflush = 'Ah2h4h5h3h'

    assert(score_high(royal_clubs) == score_high(royal_diamonds))
    assert(score_high(royal_clubs) > score_high(middle_sflush))
    assert(score_high(middle_sflush) > score_high(wheel_sflush))
    assert(score_high(royal_diamonds) > score_high(wheel_sflush))