# This file contains the Command Line Interface (CLI) for
# the Tic-Tac-Toe game. This is where input and output happens.
# For core game logic, see logic.py.

import random
from logic import Game
from pd import moves
from pd import games_pd
from pd import players
import pandas as pd


class Board:
    def __init__(self):
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
    def print_board(self):
        for i in range(3):
            print(self.board[i])
    def is_valid_move(self, position):
        x = (position + 2) // 3 - 1
        y = (position + 2 ) % 3
        if self.board[x][y] == None:
            return True
        else:
            return False
    def change_board(self, position, type):
        if self.is_valid_move(position):
            x = (position + 2) // 3 - 1
            y = (position + 2 ) % 3
            self.board[x][y] = type
            return self.board


if __name__ == '__main__':
    games_pd = pd.read_csv("/Users/yizhijuan/Documents/006UW/509/TTT/games_pd.csv")
    moves = pd.read_csv("/Users/yizhijuan/Documents/006UW/509/TTT/moves.csv")
    players = pd.read_csv("/Users/yizhijuan/Documents/006UW/509/TTT/players.csv")
    board = Board()
    game = Game()
    game.winner = None
    # a single player or 2 players
    print("Please enter the number of human player:")
    player_number = int(input())
    is_player1_turn = game.pre_set(board, player_number)
        
    while game.winner == None and game.turn < 9:
        game.turn += 1
        if is_player1_turn == 1:
            # Input a move from the player.
            print("Please enter the position(1~9)")
            position = int(input())
            type = 'X'
            moves.loc[len(moves)] = {
                "Game ID":len(games_pd)+1,
                "Turn":game.turn,
                "Player":game.player1_name,
                "Position":position
            }
            is_player1_turn = 0
        elif is_player1_turn == 0:
            # Bot generates a position
            if player_number == 1:
                while board.is_valid_move(position) == False:
                    position = random.randint(1,9)                  
            elif player_number == 2:
                position = int(input()) 
            type = 'O'  
            moves.loc[len(moves)] = {
                "Game ID":len(games_pd)+1,
                "Turn":game.turn,
                "Player":game.player2_name,
                "Position":position
            }
            is_player1_turn = 1
        # Update the board.
        board.change_board(position, type) 
        board.print_board()
        game.winner = game.get_winner(board,is_player1_turn,game)
        
    players = game.record_result(game, players)
    games_pd = game.add_game(games_pd, game.player1_name, game.player2_name, game.winner)
    games_pd.to_csv("games_pd.csv",index=False)
    moves.to_csv("moves.csv",index=False)
    players.to_csv("players.csv",index=False)
    
    exit()