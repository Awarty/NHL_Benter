
import pandas as pd
import numpy as np

team_lookup = {"Blackhawks": "Chicago Blackhawks", "Oilers": "Edmonton Oilers", "Canadiens": "Montreal Canadiens", "Avalanche": "Colorado Avalanche", \
    "Flyers": "Philadelphia Flyers", "Red Wings": "Detroit Red Wings", "Sharks": "San Jose Sharks", "Penguins": "Pittsburgh Penguins", "Capitals": "Washington Capitals", \
    "Wild": "Minnesota Wild", "Bruins": "Boston Bruins", "Stars": "Dallas Stars", "Blues": "St Louis Blues", "Coyotes": "Arizona Coyotes", \
    "Blue Jackets": "Columbus Blue Jackets", "Devils": "New Jersey Devils", "Jets": "Winnipeg Jets", "Hurricanes": "Carolina Hurricanes", \
    "Sabres": "Buffalo Sabres", "Islanders": "New York Islanders", "Canucks": "Vancouver Canucks", "Maple Leafs": "Toronto Maple Leafs", \
    "Flames": "Calgary Flames", "Kings": "Los Angeles Kings", "Predators": "Nashville Predators", "Lightning": "Tampa Bay Lightning", \
    "Ducks": "Anaheim Ducks", "Panthers": "Florida Panthers", "Senators": "Ottawa Senators", "Rangers": "New York Rangers", "Golden Knights": "Vegas Golden Knights"}

df_home = pd.read_csv("../data/home_count.csv")
df_home['Date']= pd.to_datetime(df_home['Date'])
df_away = pd.read_csv("../data/away_count.csv")
df_away['Date']= pd.to_datetime(df_away['Date'])

res = pd.DataFrame()
res["Date"] = df_home["Date"]

for index, row in df_home.iterrows():
    home_team_name = team_lookup[row["HomeTeam"]]
    away_team_name = team_lookup[row["AwayTeam"]]
    res.at[index, "HomeTeam"] = home_team_name
    res.at[index, "AwayTeam"] = away_team_name

    home_team_games_played = df_home[(df_home["Date"] < row["Date"]) & (df_home["Team"]==home_team_name)]
    away_team_games_played = df_away[(df_away["Date"] < row["Date"]) & (df_away["Team"]==away_team_name)]

    tmp = home_team_games_played[home_team_games_played["Date"] == row["Date"]]
    if not tmp.empty:
        print("LEAKING PROBLEM!!!")

    res.at[index, "home_target"] = df_home[(df_home["Date"] == row["Date"]) & (df_home["Team"]==home_team_name)]["GF"].values[0]
    res.at[index, "away_target"] = df_away[(df_away["Date"] == row["Date"]) & (df_away["Team"]==away_team_name)]["GF"].values[0]

    if len(home_team_games_played) > 5:
        for team in ["home", "away"]:
            df = home_team_games_played if team == "home" else away_team_games_played
            last_5_games = df.tail(5)
            for col in df.columns:
                if col not in ["Date", "Team", "HomeTeam", "AwayTeam"]:   
                    res.at[index, f"{team}_" + col + "_mean"] = df[col].mean()
                    res.at[index, f"{team}_" + col + "_mean_5"] = last_5_games[col].mean()

res.dropna(inplace=True)
res.to_csv("../data/dataset_1.csv", index=False)      



