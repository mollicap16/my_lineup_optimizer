# This grabs the historic draftkings projections from previous years
import pandas as pd
from bs4 import BeautifulSoup 
import requests
import io

pd.options.display.max_columns=999

roto_guru_url="http://rotoguru1.com/cgi-bin/fyday.pl?week=WEEK&year=YEAR&game=dk&scsv=1"

weeks = list(map(str,range(1,18)))
years = list(map(str,range(2014,2019)))

all_games = pd.DataFrame()
for yr in years:
    for wk in weeks:
        base_url = roto_guru_url.replace("WEEK",wk).replace("YEAR",yr)
        page = requests.get(base_url)
        soup=BeautifulSoup(page.text, 'html.parser')
        #print(soup.prettify())
        all_games=pd.concat([all_games,pd.read_csv(io.StringIO(soup.find("pre").text),sep=";")])

all_games.to_csv(r'/home/pete/projects/my_dfs_optimizer/data/historic/drafkings_2014-2018.csv')
