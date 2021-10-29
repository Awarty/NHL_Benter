from keras import callbacks
from keras.callbacks import EarlyStopping
import pandas as pd
from tqdm import tqdm
from pandas.core.frame import DataFrame

from sklearn.model_selection import train_test_split
from poisson_outcome_dist import prob_outcome
import datetime

from NN_v1 import create_network

def eval_bets(df):
    df_bets = pd.read_csv("../data/NHL_odds_and_results_new.csv", sep=";")
    df_bets["Date"] = pd.to_datetime(df_bets["Date"])
    df_bets["Date"] = df_bets["Date"].dt.strftime("%Y-%m-%d")
    df["Date"] = pd.to_datetime(df["Date"])
    
    for index, row in tqdm(df.iterrows()):
        date = row["Date"].strftime("%Y-%m-%d")
        tmp = df_bets[(df_bets["Date"]==date) & (df_bets["HomeTeam"]==row["HomeTeam"]) & (df_bets["AwayTeam"]==row["AwayTeam"])]
        if tmp.empty:
            date = (row["Date"] + datetime.timedelta(1)).strftime("%Y-%m-%d")
            tmp = df_bets[(df_bets["Date"]==date) & (df_bets["HomeTeam"]==row["HomeTeam"]) & (df_bets["AwayTeam"]==row["AwayTeam"])]

        else:
            df.at[index, "HomeOdds"] = tmp["OddsHome"].values[0]
            df.at[index, "DrawOdds"] = tmp["OddsDraw"].values[0]
            df.at[index, "AwayOdds"] = tmp["OddsAway"].values[0]
            df.at[index, "Result"] = tmp["Result"].values[0]

            home_EV = (row["HomeProb"]*(tmp["OddsHome"].values[0]-1)) - (1-row["HomeProb"])
            draw_EV = (row["DrawProb"]*(tmp["OddsDraw"].values[0]-1)) - (1-row["DrawProb"])
            away_EV = (row["AwayProb"]*(tmp["OddsAway"].values[0]-1)) - (1-row["AwayProb"])
            tmp_EV = [home_EV, draw_EV, away_EV]
            bet = tmp_EV.index(max(tmp_EV))
            if tmp_EV[bet] > 0.2:
                df.at[index, "Bet"] = "HOME" if bet==0 else ( "DRAW" if bet==1 else "AWAY")
                df.at[index, "BetSize"] = tmp_EV[bet]
                if bet==0:
                    df.at[index, "BetWon"] = tmp["OddsHome"].values[0]*tmp_EV[bet] if tmp["Result"].values[0]=="HOME" else 0
                elif bet==1:
                    df.at[index, "BetWon"] = tmp["OddsDraw"].values[0]*tmp_EV[bet] if tmp["Result"].values[0]=="DRAW" else 0
                elif bet==2:
                    df.at[index, "BetWon"] = tmp["OddsAway"].values[0]*tmp_EV[bet] if tmp["Result"].values[0]=="AWAY" else 0
            else:
                df.at[index, "Bet"] = "NO BET"
                df.at[index, "BetSize"] = 0
                df.at[index, "BetWon"] = 0
    return df

def eval_model(df, CV):
    score = []
    for i in range(CV):
        df_res = pd.DataFrame()
        y = df[["home_target", "away_target"]]
        X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.3)

        y_home_train = y_train["home_target"]
        y_away_train = y_train["away_target"]
        y_home_test = y_test["home_target"]
        y_away_test = y_test["away_target"]

        df_res["Date"] = X_test["Date"]
        df_res["HomeTeam"] = X_test["HomeTeam"]
        df_res["AwayTeam"] = X_test["AwayTeam"]
        
        X_train = X_train.drop(["Date", "HomeTeam", "AwayTeam", "home_target", "away_target"], axis=1)
        X_test = X_test.drop(["Date", "HomeTeam", "AwayTeam", "home_target", "away_target"], axis=1)

        mean =  X_train.mean(axis=0)
        std = X_train.std(axis=0)
        X_train = (X_train - mean) / std
        X_test = (X_test - mean) / std

        es = EarlyStopping(monitor="loss", patience=3, verbose=0)
        home_model = create_network(X_train.shape[1])
        away_model = create_network(X_train.shape[1])
        home_model.fit(X_train, y_home_train, batch_size=16, callbacks=[es], epochs=500, verbose=0)
        df_res["home_pred"] = home_model.predict(X_test)
        away_model.fit(X_train, y_away_train, batch_size=16, callbacks=[es], epochs=500, verbose=0)
        df_res["away_pred"] = away_model.predict(X_test)

        for index, row in df_res.iterrows():
            prob = prob_outcome(row["home_pred"], row["away_pred"])
            df_res.at[index, "HomeProb"] = prob["HomeProb"]
            df_res.at[index, "DrawProb"] = prob["DrawProb"]
            df_res.at[index, "AwayProb"] = prob["AwayProb"]
        
        print("#####"*5)
        print(f"Iteration {i}:")
        df_res = eval_bets(df_res)
        print(f"Betted: {df_res['BetSize'].sum()}\nWon: {df_res['BetWon'].sum()}\nROI: {df_res['BetWon'].sum()/df_res['BetSize'].sum()}")
        print("#####"*5)
        df_res.dropna(inplace=True)
        df_res.to_csv(f"./eval/eval_{i}.csv", index=False)
        #break

