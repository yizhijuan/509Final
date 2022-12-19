# This file is where game logic lives. No input
# or output happens here. The logic in this file
# should be unit-testable.
from pd import games_pd
from pd import players
import pandas as pd

class Game:
    def __init__(self):
        self.winner = None
        self.turn = 0 #轮次数
        self.player1_name = None
        self.player2_name = None
        self.player_number = 0
        self.player1_turn = 1 #1 means player1's turn, 0 means player2's turn
    def pre_set(self, board, player_number):
        if player_number == 1:
            self.player1_turn = 1
            print("Enter player's name:")
            self.player1_name = str(input())
            self.player2_name = 'Bot'
        elif player_number == 2:
            self.player1_turn = 1
            print("Enter player1's name:")
            self.player1_name = str(input())
            print("Enter player2's name:")
            self.player2_name = str(input())
        board.print_board()
        print("This is X's turn")
        return self.player1_turn

    def add_game(self, games_pd, player1_name, player2_name, winner):   
        games_pd.loc[len(games_pd)] = {
            "Game ID":len(games_pd) + 1,
            "Player1":player1_name,
            "Player2":player2_name,
            "Winner":winner
        }
        return games_pd
    

    def other_player(self,is_player1_turn, game):
        """Given the character for a player, returns the other player."""
        if is_player1_turn == 1:
            return game.player2_name
        else:
            return game.player1_name
        
    def get_winner(self,board,is_player1_turn,game):
        for key in('O','X'):
            for i in range(3):
                if board.board[i][0] == key and board.board[i][1] == key and board.board[i][2] == key:
                    self.winner = key
                    break
                elif board.board[0][i] == key and board.board[1][i] == key and board.board[2][i] == key:
                    self.winner = key
                    break  
            if (board.board[0][0] == key and board.board[1][1] == key and board.board[2][2] == key) or (board.board[0][2] == key and board.board[1][1] == key and board.board[2][0] == key):
                self.winner = key
        if self.winner == 'O':
            print(self.player2_name, "wins!")
            return self.player2_name
        elif self.winner == 'X':
            print(self.player1_name, "wins!")
            return self.player1_name
        else:
            print("\n") 
            if game.turn == 9:
                print("Draw!")
                return self.winner
            if is_player1_turn == 1:
                print("This is X's turn")
            else:
                print("This is O's turn")
        return self.winner

    def record_result(self, game, players):
        for name in [game.player1_name,game.player2_name]:
            exist = players.loc[players['Name'] == name]
            #player'name do not exist, create a new one
            if exist.empty:  
                players.loc[len(players)] = {
                    "Name":name,
                    "Wins":0,
                    "Losses":0,
                    "Draws":0
                }
                exist = players.loc[len(players)-1]
                players.to_csv("players.csv",index=False)
                players = pd.read_csv("/Users/yizhijuan/Documents/001UW/509/Final/players.csv")

            if game.winner == name:
                players.loc[players[players["Name"] == name].index, "Wins"] += 1
            elif game.winner == None:
                players.loc[players[players["Name"] == name].index, "Draws"] += 1
            else:
                players.loc[players[players["Name"] == name].index, "Losses"] += 1
        return players
        
                
