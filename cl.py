import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_champions_league_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    rows = soup.select('#sched_all tbody tr')

    data = []
    for row in rows:
        cells = row.select('td')
        if len(cells) >= 9:
            home_team = cells[4].text.strip()
            score = cells[6].text.strip()
            away_team = cells[8].text.strip()
            data.append({'home_team': home_team, 'score': score, 'away_team': away_team})

    df_champions_league = pd.DataFrame(data)
    return df_champions_league

# Scrape Champions League data
url = 'https://fbref.com/en/comps/8/schedule/Champions-League-Scores-and-Fixtures'
df_champions_league_data = scrape_champions_league_data(url)

# Save data to CSV
df_champions_league_data.to_csv('champions_league_data.csv', index=False)
