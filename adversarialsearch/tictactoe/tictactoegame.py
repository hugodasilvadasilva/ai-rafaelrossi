import logging
from os import symlink
from symtable import Symbol
from tictactoeboard import TicTacToeBoard as Board
from tictactoeplayer import TicTacToePlayer as Player

class TicTacToeGame:
    
    def start(board: Board, player1: Player, player2: Player):

        print(f"## Starting game ##")
        print(f"Player 1 as {player1}")
        print(f"Player 2 as {player2}")
        print(f"Board")
        print(board)

        player_turn = player1
        while not(board.terminated()):

            action = player_turn.minimax_decision(board)
            row, col = action.row_col
            board.set_cel(row, col, player_turn.symbol)
            print(f"Player {player_turn.symbol} play at row {row}, col {col}")
            print(board)
            
            if player_turn.symbol == player1.symbol:
                player_turn = player2
            else:
                player_turn = player1
        
        curr_state = board.current_result()
        print(f"## Game Over. Player '{curr_state[0]}' is the winner!!! ##")
        
        return board
        
            