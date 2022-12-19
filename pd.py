import pandas as pd

games_pd = pd.DataFrame(columns = [
    "Game ID",
    "Player1",
    "Player2",
    "Winner"
])

players = pd.DataFrame(columns = [
    "Name",
    "Wins",
    "Losses",
    "Draws"
])
players.loc[0] = {
    "Name":0,
    "Wins":0,
    "Losses":0,
    "Draws":0
}


moves = pd.DataFrame(columns = [
    "Game ID",
    "Turn",
    "Player",
    "Position"
])

players = pd.read_csv("/Users/yizhijuan/Documents/001UW/509/Final/players.csv")
ranking_by_wins = players.sort_values(by="Wins", ascending=False)
#print(ranking_by_wins)