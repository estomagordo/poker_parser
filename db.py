import sqlite3

class Db:
    def __init__(self, connstring=''):
        if connstring:
            self.connection = sqlite3.connect(connstring)
        else:
            self.connection = sqlite3.connect('poker.db')

        self.cursor = self.connection.cursor()

    def create_if_needed(self):
        create_tournament_statement = '''
            CREATE TABLE IF NOT EXISTS tournament (
                id TEXT PRIMARY KEY,
                buyin_cents INTEGER NOT NULL,
                rake_cents INTEGER NOT NULL,
                start_time INTEGER NOT NULL,
                end_time INTEGER NOT NULL,
                hero_cashed INTEGER NOT NULL
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
                villain_0 INTEGER NOT NULL,
                villain_1 INTEGER,
                villain_2 INTEGER,
                villain_3 INTEGER,
                villain_4 INTEGER,
                villain_5 INTEGER,
                villain_6 INTEGER,
                villain_7 INTEGER,
                villain_8 INTEGER,
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
        self.connection.commit()


def main():
    db = Db()
    db.create_if_needed()

if __name__ == '__main__':
    main()
