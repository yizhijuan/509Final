# This file contains the Command Line Interface (CLI) for
# the Tic-Tac-Toe game. This is where input and output happens.
# For core game logic, see logic.py.


from flask import Flask, request, render_template, redirect, url_for
from jinja2 import Template

app = Flask(__name__, template_folder='templates', static_folder='static')


import random
from logic import Game
from pd import moves
from pd import games_pd
from pd import players
import pandas as pd

TTTboard = [
            [None, 'X', 'O'],
            [None, None, None],
            [None, None, None],
]


"""The board positions are numbered as follows:
    1 2 3
    4 5 6
    7 8 9
"""
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


games_pd = pd.read_csv("/Users/yizhijuan/Documents/001UW/509/Final/games_pd.csv")
moves = pd.read_csv("/Users/yizhijuan/Documents/001UW/509/Final/moves.csv")
players = pd.read_csv("/Users/yizhijuan/Documents/001UW/509/Final/players.csv")
board = Board()
game = Game()
game.winner = None


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST': 
        game.player1_name = request.form['player1_name']
        game.player2_name = request.form['player2_name']
        if (game.player2_name == None ): 
            game.player2_name = 'Bot'
            game.player_number = 1
        return redirect('/play')
    else:
        return render_template('index.html')

is_player1_turn = game.pre_set(board, game.player_number)

@app.route('/base')
def base():
    return render_template('base.html', TTTboard = TTTboard)
    
@app.route('/play', methods=['GET','POST'])
def play():
    position = None
    if request.method == 'POST':
        position = int(request.form['position'])
        if( game.winner == None and game.turn < 9):
            game.turn += 1
        run(game, board, position)

    return render_template('play.html', position=position, TTTboard = board.board, game=game)
    
        
def run(game, board, position):
        if game.player1_turn == 1:
            # Input a move from the player.
            type = 'X'
            moves.loc[len(moves)] = {
                "Game ID":len(games_pd)+1,
                "Turn":game.turn,
                "Player":game.player1_name,
                "Position":position
            }
            game.player1_turn = 0
        elif game.player1_turn == 0:
            # Bot generates a position
            if game.player_number == 1:
                while board.is_valid_move(position) == False:
                    position = random.randint(1,9)                  
            #elif game.player_number == 2:
                #position = int(input()) 
            type = 'O'  
            moves.loc[len(moves)] = {
                "Game ID":len(games_pd)+1,
                "Turn":game.turn,
                "Player":game.player2_name,
                "Position":position
            }
            game.player1_turn = 1
        # Update the board.
        board.change_board(position, type) 
        board.print_board()
        game.winner = game.get_winner(board,game.player1_turn,game)
    
players = game.record_result(game, players)
games_pd = game.add_game(games_pd, game.player1_name, game.player2_name, game.winner)
games_pd.to_csv("games_pd.csv",index=False)
moves.to_csv("moves.csv",index=False)
players.to_csv("players.csv",index=False)

#exit()

if __name__ == '__main__':
     app.run(debug=True)