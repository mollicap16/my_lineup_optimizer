import pandas as pd

fft_pos_id = {"QB":"10", "RB":"20", "WR":"30", "TE":"40", "K":"80"}
weeks = list(map(str, range(1,18)))
years = list(map(str, range(2018,2019)))
fft_league_id = dict({"FFT Standard":"1", "FFT PPR":"107644", "FFT Half":"193033", "CBS Standard":"26943",
    "ESPN Standard":"26955", "Yahoo Half":"17", "NFL.com Standard":"143908", "FFPC PPR":"107437", "NFFC PPR":"5"}) 

fft_url_path = "https://www.fftoday.com/rankings/playerwkproj.php?Season=SEASON&GameWeek=WEEK&PosID=POS_ID&LeagueID=LEAGUE_ID";
fantasy_data_url_path = ""

#for key in fft_league_id:
#    print(key, ": ", fft_league_id[key])


#for key in fft_pos_id:
#    print(key, ": ",fft_pos_id[key])

for wk in weeks:
    for yr in years:
        for id in fft_league_id:
            for pos in fft_pos_id:
                base_url = fft_url_path.replace("WEEK",wk).replace("SEASON",yr).replace("POS_ID",fft_pos_id[pos]).replace("LEAGUE_ID",fft_league_id[id])
                print(base_url)

