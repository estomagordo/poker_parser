import sqlite3

class Db:
    def __init__(self, connstring=''):
        if connstring:
            self.connection = sqlite3.connect(connstring)
        else:
            self.connection = sqlite3.connect('db//poker.db')

        self.cursor = self.connection.cursor()

    def commmit_and_close(self):
        self.connection.commit()
        self.connection.close()

    def upsert_tournament(self, tournament):
        data = (
            tournament.id,
            tournament.buyin_cents,
            tournament.rake_cents,
            tournament.start_time,
            tournament.end_time,
            tournament.hero_result_cents
        )

        self.cursor.execute('INSERT OR REPLACE INTO tournament VALUES (?, ?, ?, ?, ?, ?)', data)
        self.connection.commit()        

    def upsert_hand(self, hand):
        data = (
            hand.id,
            hand.time,
            hand.tournament_id,
            hand.sb,
            hand.bb,
            hand.ante,
            hand.hero_pos,
            hand.player_count,
            hand.hero_before,
            hand.villains[0][0],
            hand.villains[1][0],
            hand.villains[2][0],
            hand.villains[3][0],
            hand.villains[4][0],
            hand.villains[5][0],
            hand.villains[6][0],
            hand.villains[7][0],
            hand.villains[8][0],
            hand.hero_after,
            hand.villains[0][1],
            hand.villains[1][1],
            hand.villains[2][1],
            hand.villains[3][1],
            hand.villains[4][1],
            hand.villains[5][1],
            hand.villains[6][1],
            hand.villains[7][1],
            hand.villains[8][1],
            hand.hero_cards,
            hand.villains[0][2],
            hand.villains[1][2],
            hand.villains[2][2],
            hand.villains[3][2],
            hand.villains[4][2],
            hand.villains[5][2],
            hand.villains[6][2],
            hand.villains[7][2],
            hand.villains[8][2],
            hand.flop,
            hand.turn,
            hand.river,
            hand.full
        )

        self.cursor.execute('INSERT OR REPLACE INTO hand VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)

    def create_if_needed(self):
        create_tournament_statement = '''
            CREATE TABLE IF NOT EXISTS tournament (
                id TEXT PRIMARY KEY,
                buyin_cents INTEGER NOT NULL,
                rake_cents INTEGER NOT NULL,
                start_time INTEGER NOT NULL,
                end_time INTEGER NOT NULL,
                hero_result_cents INTEGER NOT NULL
            );'''

        create_hand_statement = '''
            CREATE TABLE IF NOT EXISTS hand (
                id TEXT PRIMARY KEY,
                time INTEGER NOT NULL,
                tournament_id TEXT NOT NULL,
                small_blind INTEGER NOT NULL,
                big_blind INTEGER NOT NULL,
                ante INTEGER,
                hero_position INTEGER NOT NULL,
                player_count INTEGER NOT NULL,
                hero_before INTEGER NOT NULL,
                villain_0_before INTEGER NOT NULL,
                villain_1_before INTEGER,
                villain_2_before INTEGER,
                villain_3_before INTEGER,
                villain_4_before INTEGER,
                villain_5_before INTEGER,
                villain_6_before INTEGER,
                villain_7_before INTEGER,
                villain_8_before INTEGER,
                hero_after INTEGER NOT NULL,
                villain_0_after INTEGER NOT NULL,
                villain_1_after INTEGER,
                villain_2_after INTEGER,
                villain_3_after INTEGER,
                villain_4_after INTEGER,
                villain_5_after INTEGER,
                villain_6_after INTEGER,
                villain_7_after INTEGER,
                villain_8_after INTEGER,
                hero_hole_cards TEXT NOT NULL,
                villain_0_hole_cards TEXT,
                villain_1_hole_cards TEXT,
                villain_2_hole_cards TEXT,
                villain_3_hole_cards TEXT,
                villain_4_hole_cards TEXT,
                villain_5_hole_cards TEXT,
                villain_6_hole_cards TEXT,
                villain_7_hole_cards TEXT,
                villain_8_hole_cards TEXT,
                flop TEXT,
                turn TEXT,
                river TEXT,
                full TEXT NOT NULL,
                FOREIGN KEY(tournament_id) REFERENCES tournament(id)
            );'''

        self.cursor.execute(create_tournament_statement)
        self.cursor.execute(create_hand_statement)