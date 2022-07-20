'''
This block of code implements the testcase of Tic Tac Toe Game.
'''
import logging
import unittest
import setlog
from tictactoeplayer import TicTacToePlayer as Player
from tictactoeboard import TicTacToeBoard as Board
from tictactoeaction import TicTacToeAction as Action
from tictactoegame import TicTacToeGame as Game

class Test_Game_terminate(unittest.TestCase):
    
    def test_blank(self):
        '''
        This method checks if method terminated() returns false if board
        is blank
        '''
        marks = ['-', '-', '-', '-', '-', '-', '-', '-', '-']

        board = Board(marks)
        terminated = Game.terminated(board)

        self.assertEqual(False, terminated)
    
    def test_lasting_one(self):
        '''
        This method checks if Game.terminate() returns false if board
        last one and no player has won
        '''

        marks = ['X', '0', '0', '0', 'X', 'X', '0', 'X', '-']

        board = Board(marks)
        terminated = Game.terminated(board)

        self.assertEqual(False, terminated)
    
    def test_first_line_terminated(self):
        '''
        This method checks if Game.terminated() method returns true if board
        is terminated with X on first line
        '''

        marks = ['X', 'X', 'X', '0', '-', '0', '0', '-', '-']

        board = Board(marks)
        terminated = Game.terminated(board)

        self.assertEqual(True, terminated)

    def test_second_column_terminated(self):
        '''
        This method checks if terminated() method returns true if board
        is terminated with X on Second  Column
        '''

        marks = ['-', 'X', 'X', '0', 'X', '0', '0', 'X', '-']

        board = Board(marks)
        terminated = Game.terminated(board)

        self.assertEqual(True, terminated)

    def test_up_down_diag_terminated(self):
        '''
        This method checks if terminated() method returns true if board
        is terminated with X on up-down-diagonal.
        '''

        marks = ['X', '-', '0', '-', 'X', '0', '-', '0', 'X']

        board = Board(marks)
        terminated = Game.terminated(board)

        self.assertEqual(True, terminated)

    def test_down_up_diag_terminated(self):
        '''
        This method checks if terminated() method returns true if board
        is terminated with 0 on down-up-diagonal
        '''

        marks = ['-', 'X', '0', '-', '0', 'X', '0', '-', 'X']

        board = Board(marks)
        terminated = Game.terminated(board)

        self.assertEqual(True, terminated)

class Test_Game_final_result(unittest.TestCase):

    def test_not_terminated(self):
        '''
        This method checks if Game.current_result(board) method 
        returns (None, None) if board is note terminated'''

        marks = ['-', 'X', '0', 'X', '-', '0', 'X', '0', '-']
        board = Board(marks)
        curr_result = Game.current_result(board)

        exp_result = (None, None)

        self.assertTupleEqual(exp_result, curr_result)

    def test_X_cross_col0(self):
        '''
        This method checks if Game.current_result(board) method
        returns (X, col1) if board is crossed by X at column 0
        '''

        marks = ['X', '-', '0', 'X', '0', '-', 'X', '0', '-']
        board = Board(marks)
        curr_result = Game.current_result(board)

        exp_result = ('X', 'col0')

        self.assertTupleEqual(exp_result, curr_result)

    def test_0_cross_row1(self):
        '''
        This method checks if Game.current_result(board) method
        returns (0, row1) if board is crossed by 0 at column 1
        '''

        marks = ['-', '-', 'X', '0', '0', '0', 'X', '0', 'X']
        board = Board(marks)
        curr_result = Game.current_result(board)

        exp_result = ('0', 'row1')

        self.assertTupleEqual(exp_result, curr_result)

    def test_X_cross_up_down_diag(self):
        '''
        This method checks if Game.current_result(board) method
        returns (X, updown) if board is crossed by X up-down-diagonal
        '''

        marks = ['X', '-', 'X', '-', 'X', '0', '0', '0', 'X']
        board = Board(marks)
        curr_result = Game.current_result(board)

        exp_result = ('X', 'updown')

        self.assertTupleEqual(exp_result, curr_result)

    def test_0_cross_down_up_diag(self):
        '''
        This method checks if Game.current_result(board) method
        returns (0, downup) if board is crossed by 0 down-up-diagonal
        '''

        marks = ['X', '-', '0', '-', '0', 'X', '0', '-', 'X']
        board = Board(marks)
        curr_result = Game.current_result(board)

        exp_result = ('0', 'downup')

        self.assertTupleEqual(exp_result, curr_result)


if __name__ == "__main__":
    unittest.main()
    #print(TicTacToe_utils.string_board_all_X())