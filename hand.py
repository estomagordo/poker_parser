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
        hero,
        hero_after,
        hero_cards,
        villains,
        flop,
        turn,
        river,
        full):
        self.id = id
        self.time = time
        self.tournament_id = tournament_id,
        self.sb = sb,
        self.bb = bb,
        self.ante = ante,
        self.hero_pos = hero_pos,
        self.player_count = player_count,
        self.hero = hero,
        self.hero_after = hero_after,
        self.villains = villains,
        self.hero_cards = hero_cards,
        self.flop = flop,
        self.turn = turn,
        self.river = river,
        self.full = full

        self.setup_villains()

    def setup_villains(self):
        for x, villain in enumerate(self.villains):
            if villain[0] == -1:
                break

            before, after, cards = villain

            if x == 0:
                self.villain_0 = before
                self.villain_0_after = after
                if cards:
                    self.villain_0_hole_cards = cards
            if x == 1:
                self.villain_1 = before
                self.villain_1_after = after
                if cards:
                    self.villain_1_hole_cards = cards
            if x == 2:
                self.villain_2 = before
                self.villain_2_after = after
                if cards:
                    self.villain_2_hole_cards = cards
            if x == 3:
                self.villain_3 = before
                self.villain_3_after = after
                if cards:
                    self.villain_3_hole_cards = cards
            if x == 4:
                self.villain_4 = before
                self.villain_4_after = after
                if cards:
                    self.villain_4_hole_cards = cards