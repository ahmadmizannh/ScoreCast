import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_fa_cup_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', id='sched_all')
    rows = table.find_all('tr')[1:]

    data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 6:
            home_team = cells[3].text.strip()
            score = cells[4].text.strip()
            away_team = cells[5].text.strip()
            data.append({'home_team': home_team, 'score': score, 'away_team': away_team})

    df_fa_cup = pd.DataFrame(data)
    return df_fa_cup

# Scrape FA Cup data
url = 'https://fbref.com/en/comps/514/schedule/FA-Cup-Scores-and-Fixtures'
df_fa_cup_data = scrape_fa_cup_data(url)

# Print the scraped data
print(df_fa_cup_data)
# Save data to CSV
df_fa_cup_data.to_csv('fa_cup_data.csv', index=False)