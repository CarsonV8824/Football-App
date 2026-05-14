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
            
            db.cursor.execute("""SELECT p.player_week_id, pw.game_week_from, p.passing_yds, p.passing_td, p.passing_int 
                                FROM passing p 
                                JOIN player_week pw ON p.player_week_id = pw.player_week_id""")
            passing_map = {(row[0], row[1]): row[2:] for row in db.cursor.fetchall()}
            
            db.cursor.execute("""SELECT r.player_week_id, pw.game_week_from, r.rushing_yds, r.rushing_td 
                                FROM rushing r 
                                JOIN player_week pw ON r.player_week_id = pw.player_week_id""")
            rushing_map = {(row[0], row[1]): row[2:] for row in db.cursor.fetchall()}
            
            db.cursor.execute("""SELECT rec.player_week_id, pw.game_week_from, rec.receiving_rec, rec.receiving_yds, rec.receiving_td 
                                FROM receiving rec 
                                JOIN player_week pw ON rec.player_week_id = pw.player_week_id""")
            receiving_map = {(row[0], row[1]): row[2:] for row in db.cursor.fetchall()}
            
            db.cursor.execute("""SELECT d.player_week_id, pw.game_week_from, d.defense_sck, d.defense_int, d.defense_ff, d.defense_fr 
                                FROM defense d 
                                JOIN player_week pw ON d.player_week_id = pw.player_week_id""")
            defense_map = {(row[0], row[1]): row[2:] for row in db.cursor.fetchall()}
            
            db.cursor.execute("""SELECT player_week_id, game_week_from, game_week_to, pos, ,fantasy_score
                                FROM player_week
                              """)
            player_week_data = db.cursor.fetchall()
        
        for row in player_week_data:
            player_week_id, week_from, week_to, position, fantasy_score = row
            
            # Encode position as ASCII sum
            encoded_pos = sum([ord(char) for char in position])
            
           # bad
            passing_stats = passing_map.get((player_week_id, week_from-1), (0, 0, 0))
            rushing_stats = rushing_map.get((player_week_id, week_from-1), (0, 0))
            receiving_stats = receiving_map.get((player_week_id, week_from-1), (0, 0, 0))
            defense_stats = defense_map.get((player_week_id, week_from-1), (0, 0, 0, 0))
            
            # Combine into feature vector
            feature_vector = [week_from, week_to, encoded_pos] + list(passing_stats) + list(rushing_stats) + list(receiving_stats) + list(defense_stats)
            
            yield feature_vector, fantasy_score

def main():
    count = 0
    for line in Database.get_data():
        count += 1
        print(line)
    print(f"count: {count}")

if __name__ == "__main__":
    main()
