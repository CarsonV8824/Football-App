import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import time
from src.dataDatabase import DataDatabase

from typing import Generator

# link to data: https://fantasydata.com/nfl/fantasy-football-leaders?scope=game

def get_data(year: int | None = None, week: int | None = None) -> Generator[tuple[list, int, int, int]]:
    if year is None and week is None:
        years = range(2002, 2026)
        weeks = range(1, 19)
    else:
        years = range(year, year + 1)
        weeks = range(1, week + 1)

    for season_year in years:

        print(f"now year: {season_year}")

        for current_week in weeks:
            time.sleep(0.25) # so we don't get banned or flagged
            url = f'https://fantasydata.com/nfl/fantasy-football-leaders?scope=game&sp={season_year}_REG&week_from={current_week}&week_to={current_week}&scoring=fpts_ppr&order_by=fpts_ppr&sort_dir=desc'
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Find data by tag and class
                table_element = soup.find('table')
                if table_element:
                    html_string = StringIO(str(table_element))
                    table = pd.read_html(html_string)
                    table = table[0]

                    lists = table.values.tolist()
                    for item in lists:
                        print(item)
                        yield item, current_week, current_week, season_year
                        
                    # table = table.drop(table.columns[0], axis=1)
                    # print(table.to_csv(f"data/{season_year}_week_{current_week - 1}_to_{current_week}_fantasy.csv"))
                else:
                    print(f"No table found for year {season_year}")
        
            
def insert_data(year: int | None = None, week: int | None = None):
    for line, past_week, current_week, season_year in get_data(year, week):
        
        DataDatabase.insert_data(line[0], line[1], line[2], line[3], past_week, current_week, season_year,
        line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12],
        line[13], line[14], line[15], line[16], line[17], line[18])

if __name__ == "__main__":
    #insert_data()
    pass
