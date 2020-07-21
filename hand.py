class Hand:
    def __init__(
        self,
        id,
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
        full):
        self.id = id
        self.time = time
        self.tournament_id = tournament_id
        self.sb = sb
        self.bb = bb
        self.ante = ante
        self.hero_pos = hero_pos
        self.player_count = player_count
        self.hero_before = hero_before
        self.hero_after = hero_after
        self.villains = villains
        self.hero_cards = hero_cards
        self.flop = flop
        self.turn = turn
        self.river = river
        self.full = full