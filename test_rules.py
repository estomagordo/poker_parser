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