import pandas as pd
import numpy as np

df_home_2013_2016 = pd.read_csv("../5v5_adj_stats/home_2013_2016_counts.csv")
df_home_2016_2020 = pd.read_csv("../5v5_adj_stats/home_2017_2020_counts.csv")
df_away_2013_2016 = pd.read_csv("../5v5_adj_stats/away_2013_2016_counts.csv")
df_away_2016_2020 = pd.read_csv("../5v5_adj_stats/away_2017_2020_counts.csv")


def fix_date(df):
    for index, row in df.iterrows():
        df.at[index, "Date"] = row["Game"].split(" - ")[0]
        team_names = row["Game"].split(" - ")[1].split(", ")
        team_names[0] = team_names[0].split(" ")[:-1]
        team_names[1] = team_names[1].split(" ")[:-1]

        df.at[index, "AwayTeam"] = team_names[0][0] if len(team_names[0]) < 2 else team_names[0][0] + " " + team_names[0][1]
        df.at[index, "HomeTeam"] = team_names[1][0] if len(team_names[1]) < 2 else team_names[1][0] + " " + team_names[1][1]

    return df

df_home_2013_2016 = fix_date(df_home_2013_2016)
df_home_2016_2020 = fix_date(df_home_2016_2020)
df_away_2013_2016 = fix_date(df_away_2013_2016)
df_away_2016_2020 = fix_date(df_away_2016_2020)


df_home = pd.concat([df_home_2013_2016, df_home_2016_2020])
df_away = pd.concat([df_away_2013_2016, df_away_2016_2020])

df_home["Team"] = df_home["Team"].str.replace("Phoenix Coyotes", "Arizona Coyotes")
df_away["Team"] = df_away["Team"].str.replace("Phoenix Coyotes", "Arizona Coyotes")

keep_columns = ["Date", "Team", "HomeTeam", "AwayTeam", "PDO", "SCF", "SCA", "SCF%", "GF", "GA", "GF%", "HDCF", "HDCA", "HDCF%"]

df_home = df_home[keep_columns]
df_away = df_away[keep_columns]
df_home['Date']= pd.to_datetime(df_home['Date'])
df_away['Date']= pd.to_datetime(df_away['Date'])

df_home.replace("-", 0, inplace=True)
df_away.replace("-", 0, inplace=True)

df_home.sort_values("Date")
df_away.sort_values("Date")

df_home.to_csv("home_count.csv", index=False)
df_away.to_csv("away_count.csv", index=False)
