import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import time

# link to data: https://fantasydata.com/nfl/fantasy-football-leaders?scope=game

def get_data():
    years = range(2002, 2003)
    weeks = range(1, 5)

    for year in years:
        for week in weeks:
            if week == 1:
                # get week 1 to week 2, not week 1 to week 1
                continue
            time.sleep(1)
            url = f'https://fantasydata.com/nfl/fantasy-football-leaders?scope=game&sp=2025_REG&week_from={week - 1}&week_to={week}&scoring=fpts_ppr&order_by=fpts_ppr&sort_dir=desc'
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Find data by tag and class
                table_element = soup.find('table')
                if table_element:
                    html_string = StringIO(str(table_element))
                    table = pd.read_html(html_string)
                    table = table[0]
                    # table = table.drop(table.columns[0], axis=1)
                    print(table.to_csv(f"data/{year}_week_{week - 1}_to_{week}_fantasy.csv"))
                else:
                    print(f"No table found for year {year}")
            

if __name__ == "__main__":
    get_data()