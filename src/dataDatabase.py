import sqlite3
import os
from typing import Generator
from sklearn.preprocessing import StandardScaler

class DataDatabase:
    """put data in from the csv file's into a sqlite database for ease of use."""

    def __init__(self):
        #db_dir = r"C:\nfl-app"
        #os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join("src/player_data.db")
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.ensure_tables()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def ensure_tables(self):
        self.cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'player_week'
        """)

        if self.cursor.fetchone() is not None:
            return

        path = os.path.join("src", "fantasy schemas", "database_tables.sql")
        with open(path) as f:
            schema = f.read()

        self.cursor.executescript(schema)
        self.connection.commit()

    @staticmethod
    def create_tables():
        with DataDatabase() as db:
            db.ensure_tables()

    @staticmethod
    def insert_data(rank:int, name:str, team:str, pos:str, game_week_from:int, game_week_to:int, season_year:int, opp:str, passing_yds:int, passing_td:int, passing_int:int, rushing_yds:int, rushing_td:int, receiving_rec:int, receiving_yds:int, receiving_td:int, defense_sck:int, defense_int:int, defense_ff:int, defense_fr:int, fpts:float) -> None:
        with DataDatabase() as db:
            # Insert into player_week table
            db.cursor.execute("""INSERT INTO player_week 
                (rank, game_week_from, game_week_to, season_year, player_name, team, pos, opp, fantasy_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (rank, game_week_from, game_week_to, season_year, name, team, pos, opp, fpts))
            
            player_week_id = db.cursor.lastrowid
            
            # Insert into passing table
            db.cursor.execute("""INSERT INTO passing 
                (player_week_id, passing_yds, passing_td, passing_int)
                VALUES (?, ?, ?, ?)""",
                (player_week_id, passing_yds, passing_td, passing_int))
            
            # Insert into rushing table
            db.cursor.execute("""INSERT INTO rushing 
                (player_week_id, rushing_yds, rushing_td)
                VALUES (?, ?, ?)""",
                (player_week_id, rushing_yds, rushing_td))
            
            # Insert into receiving table
            db.cursor.execute("""INSERT INTO receiving 
                (player_week_id, receiving_rec, receiving_yds, receiving_td)
                VALUES (?, ?, ?, ?)""",
                (player_week_id, receiving_rec, receiving_yds, receiving_td))
            
            # Insert into defense table
            db.cursor.execute("""INSERT INTO defense 
                (player_week_id, defense_sck, defense_int, defense_ff, defense_fr)
                VALUES (?, ?, ?, ?, ?)""",
                (player_week_id, defense_sck, defense_int, defense_ff, defense_fr))
            
            db.connection.commit()

    @staticmethod
    def get_data() -> Generator[list[tuple]]:
        
        with DataDatabase() as db:
            db.cursor.execute("""
                SELECT p.player_week_id, pw.game_week_from, pw.season_year,
                    p.passing_yds, p.passing_td, p.passing_int
                FROM passing p
                JOIN player_week pw ON p.player_week_id = pw.player_week_id
            """)
            passing_map = {(row[0], row[1], row[2]): row[3:] for row in db.cursor.fetchall()}

            db.cursor.execute("""
                SELECT r.player_week_id, pw.game_week_from, pw.season_year,
                    r.rushing_yds, r.rushing_td
                FROM rushing r
                JOIN player_week pw ON r.player_week_id = pw.player_week_id
            """)
            rushing_map = {(row[0], row[1], row[2]): row[3:] for row in db.cursor.fetchall()}

            db.cursor.execute("""
                SELECT rec.player_week_id, pw.game_week_from, pw.season_year,
                    rec.receiving_rec, rec.receiving_yds, rec.receiving_td
                FROM receiving rec
                JOIN player_week pw ON rec.player_week_id = pw.player_week_id
            """)
            receiving_map = {(row[0], row[1], row[2]): row[3:] for row in db.cursor.fetchall()}

            db.cursor.execute("""
                SELECT d.player_week_id, pw.game_week_from, pw.season_year,
                    d.defense_sck, d.defense_int, d.defense_ff, d.defense_fr
                FROM defense d
                JOIN player_week pw ON d.player_week_id = pw.player_week_id
            """)
            defense_map = {(row[0], row[1], row[2]): row[3:] for row in db.cursor.fetchall()}

            db.cursor.execute("""
                SELECT player_week_id, game_week_from, game_week_to, pos, player_name,
                    fantasy_score, team, opp, season_year
                FROM player_week
            """)
            player_week_data = db.cursor.fetchall()

        # Keep these separate so keys do not collide
        player_history = {}
        week_lookup = {}

        for row in player_week_data:
            player_week_id, week_from, _, _, player_name, _, _, _, season_year = row

            if player_name not in player_history:
                player_history[player_name] = set()

            player_history[player_name].add((season_year, week_from))
            week_lookup[(player_name, season_year, week_from)] = player_week_id

        for row in player_week_data:
            player_week_id, week_from, week_to, position, player_name, fantasy_score, team, opp_team, season_year = row

            if week_from == 1 or season_year < 2015:
                continue

            # Temporary categorical encoding; better replaced with one-hot or embeddings later
            encoded_pos = (sum(ord(char) for char in position) - 65) / 40
            team_encoded = (sum(ord(char) for char in team) - 65) / 40
            opp_encoded = (sum(ord(char) for char in opp_team) - 65) / 40

            past_passing = []
            past_rushing = []
            past_receiving = []
            past_defense = []

            history_weeks = min(4, week_from - 1)

            for offset in range(4, 0, -1):
                past_week = week_from - offset

                if past_week < 1:
                    past_passing.extend((0, 0, 0))
                    past_rushing.extend((0, 0))
                    past_receiving.extend((0, 0, 0))
                    past_defense.extend((0, 0, 0, 0))
                    continue

                prev_week_id = week_lookup.get((player_name, season_year, past_week))

                if prev_week_id is not None:
                    key = (prev_week_id, past_week, season_year)
                    past_passing.extend(passing_map.get(key, (0, 0, 0)))
                    past_rushing.extend(rushing_map.get(key, (0, 0)))
                    past_receiving.extend(receiving_map.get(key, (0, 0, 0)))
                    past_defense.extend(defense_map.get(key, (0, 0, 0, 0)))
                else:
                    past_passing.extend((0, 0, 0))
                    past_rushing.extend((0, 0))
                    past_receiving.extend((0, 0, 0))
                    past_defense.extend((0, 0, 0, 0))

            if history_weeks > 0:
                avg_passing = tuple(
                    sum(past_passing[i::3][-history_weeks:]) / history_weeks for i in range(3)
                )
                avg_rushing = tuple(
                    sum(past_rushing[i::2][-history_weeks:]) / history_weeks for i in range(2)
                )
                avg_receiving = tuple(
                    sum(past_receiving[i::3][-history_weeks:]) / history_weeks for i in range(3)
                )
                avg_defense = tuple(
                    sum(past_defense[i::4][-history_weeks:]) / history_weeks for i in range(4)
                )
            else:
                avg_passing = (0, 0, 0)
                avg_rushing = (0, 0)
                avg_receiving = (0, 0, 0)
                avg_defense = (0, 0, 0, 0)

            feature_vector = (
                [week_from, week_to, season_year, encoded_pos]
                + past_passing
                + past_rushing
                + past_receiving
                + past_defense
                + list(avg_passing)
                + list(avg_rushing)
                + list(avg_receiving)
                + list(avg_defense)
                + [team_encoded, opp_encoded, history_weeks]
            )

            yield feature_vector, fantasy_score

    @staticmethod
    def get_data_for_single_player(name:str, week:int, year:int) -> Generator[list[tuple]]:
        
        with DataDatabase() as db:
            db.create_tables()

            db.cursor.execute("""
                SELECT p.player_week_id, pw.game_week_from, pw.season_year,
                    p.passing_yds, p.passing_td, p.passing_int
                FROM passing p
                JOIN player_week pw ON p.player_week_id = pw.player_week_id
                WHERE pw.player_name = ?
            """, (name,))
            passing_map = {(row[0], row[1], row[2]): row[3:] for row in db.cursor.fetchall()}

            db.cursor.execute("""
                SELECT r.player_week_id, pw.game_week_from, pw.season_year,
                    r.rushing_yds, r.rushing_td
                FROM rushing r
                JOIN player_week pw ON r.player_week_id = pw.player_week_id
                WHERE pw.player_name = ?
            """, (name,))
            rushing_map = {(row[0], row[1], row[2]): row[3:] for row in db.cursor.fetchall()}

            db.cursor.execute("""
                SELECT rec.player_week_id, pw.game_week_from, pw.season_year,
                    rec.receiving_rec, rec.receiving_yds, rec.receiving_td
                FROM receiving rec
                JOIN player_week pw ON rec.player_week_id = pw.player_week_id
                WHERE pw.player_name = ?
            """, (name,))
            receiving_map = {(row[0], row[1], row[2]): row[3:] for row in db.cursor.fetchall()}

            db.cursor.execute("""
                SELECT d.player_week_id, pw.game_week_from, pw.season_year,
                    d.defense_sck, d.defense_int, d.defense_ff, d.defense_fr
                FROM defense d
                JOIN player_week pw ON d.player_week_id = pw.player_week_id
                WHERE pw.player_name = ?
            """, (name, ))
            defense_map = {(row[0], row[1], row[2]): row[3:] for row in db.cursor.fetchall()}

            db.cursor.execute("""
                SELECT player_week_id, game_week_from, game_week_to, pos, player_name,
                    fantasy_score, team, opp, season_year
                FROM player_week
                WHERE player_name = ?
            """, (name, ))
            player_week_data = db.cursor.fetchall()

        # Keep these separate so keys do not collide
        player_history = {}
        week_lookup = {}

        for row in player_week_data:
            player_week_id, week_from, _, _, player_name, _, _, _, season_year = row

            if player_name not in player_history:
                player_history[player_name] = set()

            player_history[player_name].add((season_year, week_from))
            week_lookup[(player_name, season_year, week_from)] = player_week_id

        for row in player_week_data:
            player_week_id, week_from, week_to, position, player_name, fantasy_score, team, opp_team, season_year = row

            if week_from == 1 or season_year < 2015:
                continue

            # Temporary categorical encoding; better replaced with one-hot or embeddings later
            encoded_pos = (sum(ord(char) for char in position) - 65) / 40
            team_encoded = (sum(ord(char) for char in team) - 65) / 40
            opp_encoded = (sum(ord(char) for char in opp_team) - 65) / 40

            past_passing = []
            past_rushing = []
            past_receiving = []
            past_defense = []

            history_weeks = min(4, week_from - 1)

            for offset in range(4, 0, -1):
                past_week = week_from - offset

                if past_week < 1:
                    past_passing.extend((0, 0, 0))
                    past_rushing.extend((0, 0))
                    past_receiving.extend((0, 0, 0))
                    past_defense.extend((0, 0, 0, 0))
                    continue

                prev_week_id = week_lookup.get((player_name, season_year, past_week))

                if prev_week_id is not None:
                    key = (prev_week_id, past_week, season_year)
                    past_passing.extend(passing_map.get(key, (0, 0, 0)))
                    past_rushing.extend(rushing_map.get(key, (0, 0)))
                    past_receiving.extend(receiving_map.get(key, (0, 0, 0)))
                    past_defense.extend(defense_map.get(key, (0, 0, 0, 0)))
                else:
                    past_passing.extend((0, 0, 0))
                    past_rushing.extend((0, 0))
                    past_receiving.extend((0, 0, 0))
                    past_defense.extend((0, 0, 0, 0))

            if history_weeks > 0:
                avg_passing = tuple(
                    sum(past_passing[i::3][-history_weeks:]) / history_weeks for i in range(3)
                )
                avg_rushing = tuple(
                    sum(past_rushing[i::2][-history_weeks:]) / history_weeks for i in range(2)
                )
                avg_receiving = tuple(
                    sum(past_receiving[i::3][-history_weeks:]) / history_weeks for i in range(3)
                )
                avg_defense = tuple(
                    sum(past_defense[i::4][-history_weeks:]) / history_weeks for i in range(4)
                )
            else:
                avg_passing = (0, 0, 0)
                avg_rushing = (0, 0)
                avg_receiving = (0, 0, 0)
                avg_defense = (0, 0, 0, 0)

            feature_vector = (
                [week_from, week_to, season_year, encoded_pos]
                + past_passing
                + past_rushing
                + past_receiving
                + past_defense
                + list(avg_passing)
                + list(avg_rushing)
                + list(avg_receiving)
                + list(avg_defense)
                + [team_encoded, opp_encoded, history_weeks]
            )

            yield feature_vector, fantasy_score

def main():
    count = 0
    for line in DataDatabase.get_data():
        count += 1
        print(line)
    print(f"count: {count}")

if __name__ == "__main__":
    main()
