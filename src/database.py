import sqlite3
import os
from typing import Generator

class Database:
    """put data in from the csv file's into a sqlite database for ease of use."""

    def __init__(self):
        #db_dir = r"C:\nfl-app"
        #os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join("src/fantasy_one_week.db")
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    @staticmethod
    def create_tables():
        with Database() as db:
            path = os.path.join("src", "fantasy schemas", "database_tables.sql")
            with open(path) as f:
                data = f.read()

            print(data)
            
            # I know this is bad. Only used to make tables.
            db.cursor.executescript(data)
            db.connection.commit()

    @staticmethod
    def insert_data(rank:int, name:str, team:str, pos:str, game_week_from:int, game_week_to:int, season_year:int, opp:str, passing_yds:int, passing_td:int, passing_int:int, rushing_yds:int, rushing_td:int, receiving_rec:int, receiving_yds:int, receiving_td:int, defense_sck:int, defense_int:int, defense_ff:int, defense_fr:int, fpts:float) -> None:
        with Database() as db:
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
        with Database() as db:
            db.cursor.execute("""SELECT player_week.game_week_from, player_week.game_week_to, player_week.pos, player_week.fantasy_score, passing.passing_yds, passing.passing_td, passing.passing_int, rushing.rushing_yds, rushing.rushing_td, receiving.receiving_rec, receiving.receiving_yds, receiving.receiving_td, defense.defense_sck, defense.defense_int, defense.defense_ff, defense.defense_fr
                                FROM player_week
                                JOIN passing
                                 on passing.player_week_id = player_week.player_week_id
                                JOIN rushing
                                 on rushing.player_week_id = player_week.player_week_id
                                JOIN receiving
                                 on receiving.player_week_id = player_week.player_week_id
                                JOIN defense
                                 on defense.player_week_id = player_week.player_week_id
                              """)
            data = db.cursor.fetchall()
        for piece in data:
            piece = list(piece)

            piece[2] = sum([ord(char) for char in piece[2]]) # takes the position and sums each chracter ascii into a number for model
            
            fantasy_score:float = piece.pop(3)
            yield piece, fantasy_score

def main():
    count = 0
    for line in Database.get_data():
        count += 1
        print(line)
    print(f"count: {count}")

if __name__ == "__main__":
    main()
