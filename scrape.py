import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import time
from database import Database

from typing import Generator

# link to data: https://fantasydata.com/nfl/fantasy-football-leaders?scope=game

def get_data() -> Generator[tuple[list, int, int, int]]:
    years = range(2002, 2026)
    weeks = range(1, 19)

    for year in years:

        print(f"now year: {year}")

        for week in weeks:
            if week == 1:
                # get week 1 to week 2, not week 1 to week 1
                continue
            time.sleep(0.25) # so we don't get banned or flagged
            url = f'https://fantasydata.com/nfl/fantasy-football-leaders?scope=game&sp={year}_REG&week_from={week - 1}&week_to={week}&scoring=fpts_ppr&order_by=fpts_ppr&sort_dir=desc'
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
                        yield item, week-1, week, year
                        
                    # table = table.drop(table.columns[0], axis=1)
                    # print(table.to_csv(f"data/{year}_week_{week - 1}_to_{week}_fantasy.csv"))
                else:
                    print(f"No table found for year {year}")
        
            
def main():
    for line, past_week, week, year in get_data():
        Database.insert_data(line[0], line[1], line[2], line[3], past_week, week, year,
        line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12],
        line[13], line[14], line[15], line[16], line[17], line[18])

if __name__ == "__main__":
    main()