class Tournament:
    def __init__(self, id, buyin_cents, rake_cents):
        self.id = id
        self.buyin_cents = buyin_cents
        self.rake_cents = rake_cents
        self.hands = []

    def add_hand(self, hand):
        self.hands.append(hand)

    def finalize(self):
        self.hands.sort(key=lambda hand: hand.time)
        self.start_time = self.hands[0].time
        self.end_time = self.hands[-1].time
        self.hero_cashed = self.did_hero_cash()

    def did_hero_cash(self):
        last_hand = self.hands[-1]

        if last_hand.hero_after:
            return True

        if not any(v == 0 for v in last_hand.villains_after):
            return False

        surviving_villain_count = len(v for v in last_hand.villains_after if v)
        eliminated_villain_stacks = sorted([last_hand.villains[x] for x in range(len(last_hand.villains)) if not last_hand.villains_after[x]])

        if surviving_villain_count > 2:
            return False

        if surviving_villain_count == 2:
            return last_hand.hero > eliminated_villain_stacks[-1]
            
        return last_hand.hero > eliminated_villain_stacks[-2]