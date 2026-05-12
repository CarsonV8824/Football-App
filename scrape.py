import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def get_data():
    years = range(2001, 2026)

    for year in years:
        url = f'https://fantasydata.com/nfl/fantasy-football-leaders?scope=season&sp={year}_REG&scoring=fpts_ppr&order_by=fpts_ppr&sort_dir=desc'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find data by tag and class
            table_element = soup.find('table')
            if table_element:
                html_string = StringIO(str(table_element))
                table = pd.read_html(html_string)
                table = table[0]
                print(table.to_csv(f"data/{year}_fantasy.csv"))
            else:
                print(f"No table found for year {year}")
            

if __name__ == "__main__":
    get_data()