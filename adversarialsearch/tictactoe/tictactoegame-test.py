'''
This block of code implements the testcase of Tic Tac Toe Game.
'''
import logging
import unittest
import setlog
from tictactoeplayer import TicTacToePlayer as Player
from tictactoeboard import TicTacToeBoard as Board
from tictactoegame import TicTacToeGame as Game

class Test_Game_start(unittest.TestCase):
    
    def one_move_lasting(self):
        '''
        This method checks how Game.start() returns when there is
        only one move lasting
        '''

        setlog.set_log(logging.WARNING)

        board_list = ['X', '0', 'X', '0', '0', 'X', 'X', '-', '0']
        game_over_board = Game.start(Board(board_list), Player('0'), Player('X') )

        exp_list = board_list.copy()
        exp_list[7] = '0'

        self.assertEqual(exp_list, game_over_board.as_one_line_list())
    
    def one_move_to_win(self):
        '''
        This method checks how Game.start() returns when there is
        only one move to win
        '''

        setlog.set_log(logging.WARNING)

        board_list = ['X', '0', 'X', '0', '0', 'X', '-', '-', '0']
        game_over_board = Game.start(Board(board_list), Player('0'), Player('X') )

        exp_list = board_list.copy()
        exp_list[7] = '0'

        self.assertEqual(exp_list, game_over_board.as_one_line_list())
    
    def two_moves_even(self):
        '''
        This method checks how Game.start() returns when there is
        only two moves lasting and game will even
        '''

        setlog.set_log(logging.WARNING)

        board_list = ['X', '0', 'X', '0', '0', 'X', '-', '-', '0']
        game_over_board = Game.start(Board(board_list), Player('X'), Player('0') )

        exp_list = board_list.copy()
        exp_list[7] = 'X'
        exp_list[6] = '0'

        self.assertEqual(exp_list, game_over_board.as_one_line_list())

    def best_hit(self):
        '''
        This method checks if Game.start() chooses the best option 
        so player will always win
        '''

        setlog.set_log(logging.WARN)

        board_list = ['X', '0', 'X', '0', '-', '-', 'X', '-', '-']
        game_over = Game.start(Board(board_list), Player('0'), Player('X'))

        exp_list = board_list.copy()
        exp_list[4] = '0'
        exp_list[5] = 'X'
        exp_list[7] = '0'

        self.assertListEqual(exp_list, game_over.as_one_line_list())
    
    def test_run(self):

        #self.one_move_lasting()
        #self.one_move_to_win()
        #self.two_moves_even()
        self.best_hit()

if __name__ == "__main__":
    unittest.main()