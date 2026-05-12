import sqlite3
import os

class Database:
    """put data in from the csv file's into a sqlite database for ease of use."""

    def __init__(self):
        self.connection = sqlite3.connect("fantasy.db")
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    @staticmethod
    def create_tables():
        with Database() as db:
            with open("schemas/database_tables.sql") as f:
                data = f.read()

            print(data)
            
            # I know this is bad. Only used to make tables.
            db.cursor.executescript(data)
            db.connection.commit()

if __name__ == "__main__":
    Database.create_tables()
