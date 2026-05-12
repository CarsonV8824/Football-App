import sqlite3

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
    def create_tables(self):
        with Database() as db:
            pass