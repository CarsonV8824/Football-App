import sqlite3
import os

class Database:
    """put data in from the csv file's into a sqlite database for ease of use."""

    def __init__(self):
        db_dir = r"C:\nfl-app"
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, "fantasy.db")
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    @staticmethod
    def create_tables():
        with Database() as db:
            with open("fantasy schemas/database_tables.sql") as f:
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

if __name__ == "__main__":
    Database.create_tables()
