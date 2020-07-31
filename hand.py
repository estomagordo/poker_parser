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
        hero_2way_ai,
        hero_2way_ai_street,
        hero_2way_ai_opponent_hand,
        hero_2way_ai_pot_size,
        hero_2way_ai_cevdiff,
        hero_2way_ai_icmevdiff,
        cEV,
        icmEV,
        actual_chips,
        actual_icm,
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
        self.hero_2way_ai = hero_2way_ai
        self.hero_2way_ai_street = hero_2way_ai_street
        self.hero_2way_ai_opponent_hand = hero_2way_ai_opponent_hand
        self.hero_2way_ai_pot_size = hero_2way_ai_pot_size
        self.hero_2way_ai_cevdiff = hero_2way_ai_cevdiff
        self.hero_2way_ai_icmevdiff = hero_2way_ai_icmevdiff
        self.cEV = cEV
        self.icmEV = icmEV
        self.actual_chips = actual_chips
        self.actual_icm = actual_icm
        self.full = full