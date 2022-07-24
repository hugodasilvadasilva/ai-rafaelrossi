'''
This block of code implements the testcase of Tic Tac Toe Board.
'''
import logging
import unittest
import setlog
from tictactoeboard import TicTacToeBoard as Board

'''class TicTacToe_utils():

    def string_list_all_X() -> list:
        return ['X','X','X','X','X','X','X','X','X']

    def string_list_lasting_one() -> list:
        
        Returns a list with only one cel empty/available.
        The list content is: ['X','X','X','X','X','X','X','X','-']
        
        return ['X','X','X','X','X','X','X','X','-']
    
    def string_list_X_Zero_Blank() -> list:
        
        Returns a list as ['X', '0', '-','X', '0', '-','X', '0', '-']
        
        return ['X', '0', '-','X', '0', '-','X', '0', '-']

    def board_cols_X_Zero_Blank() -> Board:
        
        Returns a `Board` where first column is 'X', the second is '0'
        and the third is '-', as bellow:\n
        X|0|-\n
        X|0|-\n
        X|0|-\n
        
        board = Board(TicTacToe_utils.string_list_X_Zero_Blank())
        return board
    
    def string_board_all_X():
        
        Returns a string representing a board as:\n
        X|X|X\n
        X|X|X\n
        X|X|X
        
        return "X|X|X\nX|X|X\nX|X|X"

    def tictactoe_all_X():
        ttt = Board(TicTacToe_utils.string_list_all_X())
'''

class Test_Board_repr(unittest.TestCase):

    def test_repr_equals(self):
        '''
        This Test Case checks if repr is returning a string as expected.
        '''

        marks = ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
        all_x_board_obj = Board(marks)
        all_x_board_exp = 'X|X|X\nX|X|X\nX|X|X'
        self.assertEqual(all_x_board_exp, all_x_board_obj.__repr__())

class Test_Board_board(unittest.TestCase):
    
    def test_board(self):
        '''
        This Test Case checks if board.board() method is returning a 
        3x3 list'''

        list_template = ['X', '0', '-','X', '0', '-','X', '0', '-']

        board = Board(list_template)

        template_board = []
        template_board.append(list_template[0:3])
        template_board.append(list_template[3:6])
        template_board.append(list_template[6:9])

        self.assertEqual(template_board, board.board)

class Test_Board_as_one_line_list(unittest.TestCase):
    
    def test_equals(self):
        '''
        This Test Case checks if as_one_line_list returns all marks as one line list.
        I.e.:
        If Board is [[X,X,X], [X,X,X], [X,X,X]] it must return [X,X,X,X,X,X,X,X,X]
        '''

        template = ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
        board = Board(template)
        expected = template

        self.assertEqual(expected, board.as_one_line_list())

class Test_Board_get_column(unittest.TestCase):

    def test_get_column(self):
        '''
        This Test Case checks if get_column method is returning a column correctly.
        It creates a board instance as [['X','0','-'], ['X','0','-'], ['X','0','-']]
        and get column 0 (first column that has 'X' only).
        '''
        board = Board(['X', '0', '-','X', '0', '-','X', '0', '-'])
        col0 = ['X', 'X', 'X']
        col1 = ['0', '0', '0']
        col2 = ['-', '-', '-']

        self.assertEqual(board.get_column(0), col0)
        self.assertEqual(board.get_column(1), col1)
        self.assertEqual(board.get_column(2), col2)

class Test_Board_get_down_up_diagonnal(unittest.TestCase):

    def test_get_empty_diagonal(self):
        '''
        This method checks if the method Tictactoeplayer.get_down_up_diagonnal()
        is returning the diagonal properly
        '''

        template = ['X', '0', '-', 'X', '-', '0', '-', '0', 'X']

        board = Board(template)
        diagonal = board.get_down_up_diagonnal()

        expected_diagonal = ['-', '-', '-']

        self.assertListEqual(expected_diagonal, diagonal)

class Test_Board_terminate(unittest.TestCase):
    
    def test_blank(self):
        '''
        This method checks if method Board.terminated() returns false if board
        is blank
        '''
        marks = ['-', '-', '-', '-', '-', '-', '-', '-', '-']

        board = Board(marks)
        terminated = board.terminated()

        self.assertEqual(False, terminated)
    
    def test_lasting_one(self):
        '''
        This method checks if Board.terminate() returns false if board
        last one and no player has won
        '''

        marks = ['X', '0', '0', '0', 'X', 'X', '0', 'X', '-']

        board = Board(marks)
        terminated = board.terminated()

        self.assertEqual(False, terminated)
    
    def test_first_line_terminated(self):
        '''
        This method checks if Board.terminated() method returns true if board
        is terminated with X on first line
        '''

        marks = ['X', 'X', 'X', '0', '-', '0', '0', '-', '-']

        board = Board(marks)
        terminated = board.terminated()

        self.assertEqual(True, terminated)

    def test_second_column_terminated(self):
        '''
        This method checks if terminated() method returns true if board
        is terminated with X on Second  Column
        '''

        marks = ['-', 'X', 'X', '0', 'X', '0', '0', 'X', '-']

        board = Board(marks)
        terminated = board.terminated()

        self.assertEqual(True, terminated)

    def test_up_down_diag_terminated(self):
        '''
        This method checks if terminated() method returns true if board
        is terminated with X on up-down-diagonal.
        '''

        marks = ['X', '-', '0', '-', 'X', '0', '-', '0', 'X']

        board = Board(marks)
        terminated = board.terminated()

        self.assertEqual(True, terminated)

    def test_down_up_diag_terminated(self):
        '''
        This method checks if terminated() method returns true if board
        is terminated with 0 on down-up-diagonal
        '''

        marks = ['-', 'X', '0', '-', '0', 'X', '0', '-', 'X']

        board = Board(marks)
        terminated = board.terminated()

        self.assertEqual(True, terminated)

class Test_Board_final_result(unittest.TestCase):

    def test_not_terminated(self):
        '''
        This method checks if Board.current_result() method 
        returns (None, None) if board is note terminated'''

        marks = ['-', 'X', '0', 'X', '-', '0', 'X', '0', '-']
        board = Board(marks)
        curr_result = board.current_result()

        exp_result = (None, None)

        self.assertTupleEqual(exp_result, curr_result)

    def test_X_cross_col0(self):
        '''
        This method checks if Board.current_result() method
        returns (X, col1) if board is crossed by X at column 0
        '''

        marks = ['X', '-', '0', 'X', '0', '-', 'X', '0', '-']
        board = Board(marks)
        curr_result = board.current_result()

        exp_result = ('X', 'col0')

        self.assertTupleEqual(exp_result, curr_result)

    def test_0_cross_row1(self):
        '''
        This method checks if Board.current_result() method
        returns (0, row1) if board is crossed by 0 at column 1
        '''

        marks = ['-', '-', 'X', '0', '0', '0', 'X', '0', 'X']
        board = Board(marks)
        curr_result = board.current_result()

        exp_result = ('0', 'row1')

        self.assertTupleEqual(exp_result, curr_result)

    def test_X_cross_up_down_diag(self):
        '''
        This method checks if Board.current_result() method
        returns (X, updown) if board is crossed by X up-down-diagonal
        '''

        marks = ['X', '-', 'X', '-', 'X', '0', '0', '0', 'X']
        board = Board(marks)
        curr_result = board.current_result()

        exp_result = ('X', 'updown')

        self.assertTupleEqual(exp_result, curr_result)

    def test_0_cross_down_up_diag(self):
        '''
        This method checks if Board.current_result() method
        returns (0, downup) if board is crossed by 0 down-up-diagonal
        '''

        marks = ['X', '-', '0', '-', '0', 'X', '0', '-', 'X']
        board = Board(marks)
        curr_result = board.current_result()

        exp_result = ('0', 'downup')

        self.assertTupleEqual(exp_result, curr_result)

if __name__ == "__main__":
    unittest.main()
    #print(TicTacToe_utils.string_board_all_X())