import os

import pandas as pd

def main():

    path = "nfl_data.csv"
    data = pd.read_csv(path, sep=";")
    print(data.describe())

if __name__ == "__main__":
    main()