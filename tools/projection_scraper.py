import pandas as pd
from bs4 import BeautifulSoup
import requests
import io
import re

fft_pos_id = {"QB":"10", "RB":"20", "WR":"30", "TE":"40", "K":"80"}
weeks = list(map(str, range(1,2)))
years = list(map(str, range(2018,2019)))
fft_league_id = dict({"FFT Standard":"1", "FFT PPR":"107644", "FFT Half":"193033", "CBS Standard":"26943",
    "ESPN Standard":"26955", "Yahoo Half":"17", "NFL.com Standard":"143908", "FFPC PPR":"107437", "NFFC PPR":"5"}) 

fft_url_path = "https://www.fftoday.com/rankings/playerwkproj.php?Season=SEASON&GameWeek=WEEK&PosID=POS_ID&LeagueID=LEAGUE_ID";

def concat_header_content(html_content, concat_text):
    clean_text = html_content
    print(html_content)    
    print(clean_text)

# Fantasy Football Today loop
for wk in weeks:
    for yr in years:
        for pos in fft_pos_id:
            if (pos == "QB"):
                base_url = fft_url_path.replace("WEEK",wk).replace("SEASON",yr).replace("POS_ID",fft_pos_id[pos]).replace("LEAGUE_ID",fft_league_id["FFT PPR"])
                print(base_url)
                page = requests.get(base_url)
                soup = BeautifulSoup(page.text, 'html.parser')
                table_header = soup.find(class_='tableclmhdr')
                header_content = table_header.find_all('b')
                first_line_csv =""
                concat_header_content(header_content, first_line_csv);
                print(first_line_csv)
#                for columns in header_content:
#                    first_line_csv = pd.concat(first_line_csv, 
#                    print(columns)

