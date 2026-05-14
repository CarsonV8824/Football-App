import sqlite3
import os
from typing import Generator
from sklearn.preprocessing import StandardScaler

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
            
            db.cursor.execute("""SELECT player_week_id, game_week_from, game_week_to, pos, player_name, fantasy_score, team, opp, season_year
                                FROM player_week
                              """)
            player_week_data = db.cursor.fetchall()
        
        # Build player lookup map: (player_name, week) -> player_week_id for previous week lookups
        player_id_map = {}
        for row in player_week_data:
            player_week_id, week_from, _, _, player_name, _, _, _,season_year = row
            player_id_map[player_name] = set()
            player_id_map[(player_name, week_from)] = player_week_id
        
        for row in player_week_data:
            player_week_id, week_from, week_to, position, player_name, fantasy_score, team, opp_team, season_year = row
            player_id_map[player_name].add((player_name, season_year))
            if week_from == 1:
                continue
            if season_year < 2015:
                continue
            
            # Encode position as ASCII sum
            encoded_pos = (sum([ord(char) for char in position]) - 65) / 40
            team_encoded = (sum([ord(char) for char in team]) - 65) / 40
            opp_encoded = (sum([ord(char) for char in opp_team]) -  65) / 40
            
            # Collect stats from past 4 weeks (pad with zeros if fewer weeks available)
            past_passing = []
            past_rushing = []
            past_receiving = []
            past_defense = []
            
            for past_week in range(max(1, week_from - 4), week_from):
                prev_week_id = player_id_map.get((player_name, past_week))
                if prev_week_id is not None:
                    past_passing.extend(passing_map.get((prev_week_id, past_week), (0, 0, 0)))
                    past_rushing.extend(rushing_map.get((prev_week_id, past_week), (0, 0)))
                    past_receiving.extend(receiving_map.get((prev_week_id, past_week), (0, 0, 0)))
                    past_defense.extend(defense_map.get((prev_week_id, past_week), (0, 0, 0, 0)))
                else:
                    past_passing.extend((0, 0, 0))
                    past_rushing.extend((0, 0))
                    past_receiving.extend((0, 0, 0))
                    past_defense.extend((0, 0, 0, 0))
            
            # Pad to always have exactly 4 weeks of data (4*3=12 passing, 4*2=8 rushing, etc.)
            num_weeks_available = min(4, week_from - 1)
            weeks_to_pad = 4 - num_weeks_available
            past_passing.extend([0] * (weeks_to_pad * 3))
            past_rushing.extend([0] * (weeks_to_pad * 2))
            past_receiving.extend([0] * (weeks_to_pad * 3))
            past_defense.extend([0] * (weeks_to_pad * 4))
            
            # Calculate rolling averages across past weeks
            if num_weeks_available > 0:
                avg_passing = tuple(sum(past_passing[i::3][:num_weeks_available]) / num_weeks_available for i in range(3))
                avg_rushing = tuple(sum(past_rushing[i::2][:num_weeks_available]) / num_weeks_available for i in range(2))
                avg_receiving = tuple(sum(past_receiving[i::3][:num_weeks_available]) / num_weeks_available for i in range(3))
                avg_defense = tuple(sum(past_defense[i::4][:num_weeks_available]) / num_weeks_available for i in range(4))
            else:
                avg_passing = (0, 0, 0)
                avg_rushing = (0, 0)
                avg_receiving = (0, 0, 0)
                avg_defense = (0, 0, 0, 0)

            # Combine into fixed-length feature vector
            feature_vector = [week_from, week_to, encoded_pos] + past_passing + past_rushing + past_receiving + past_defense + list(avg_passing) + list(avg_rushing) + list(avg_receiving) + list(avg_defense) + [team_encoded, opp_encoded, len(player_id_map[player_name])]
            
            yield feature_vector, fantasy_score

def main():
    count = 0
    for line in Database.get_data():
        count += 1
        print(line)
    print(f"count: {count}")

if __name__ == "__main__":
    main()
