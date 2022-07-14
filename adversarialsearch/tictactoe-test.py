'''
This block of code implements the testcase of Tic Tac Toe game.
'''
import logging
import unittest
import setlog
from tictactoe import TicTacToePlayer as Player
from tictactoe import TicTacToeBoard as Board

class TicTacToe_utils():

    def string_list_all_X() -> list:
        return ['X','X','X','X','X','X','X','X','X']

    def string_list_lasting_one() -> list:
        '''
        Returns a list with only one cel empty/available.
        The list content is: ['X','X','X','X','X','X','X','X','-']
        '''
        return ['X','X','X','X','X','X','X','X','-']
    
    def string_list_X_Zero_Blank() -> list:
        '''
        Returns a list as ['X', '0', '-','X', '0', '-','X', '0', '-']
        '''
        return ['X', '0', '-','X', '0', '-','X', '0', '-']

    def board_cols_X_Zero_Blank() -> Board:
        '''
        Returns a `Board` where first column is 'X', the second is '0'
        and the third is '-', as bellow:\n
        X|0|-\n
        X|0|-\n
        X|0|-\n
        '''
        board = Board(TicTacToe_utils.string_list_X_Zero_Blank())
        return board
    
    def string_board_all_X():
        '''
        Returns a string representing a board as:\n
        X|X|X\n
        X|X|X\n
        X|X|X
        '''
        return "X|X|X\nX|X|X\nX|X|X"

    def tictactoe_all_X():
        ttt = Board(TicTacToe_utils.string_list_all_X())
    

class Test_TictactoeBoard_repr(unittest.TestCase):

    def test_repr_equals(self):
        '''
        This Test Case checks if repr is returning a string as expected.
        '''

        all_x_board_obj = Board(TicTacToe_utils.string_list_all_X())
        all_x_board_str = TicTacToe_utils.string_board_all_X()
        self.assertEqual(all_x_board_str, all_x_board_obj.__repr__())

class Test_Tictactoeboard_board(unittest.TestCase):
    
    def test_board(self):

        list_template = TicTacToe_utils.string_list_X_Zero_Blank()

        tttboard = Board(list_template)

        template_board = []
        template_board.append(list_template[0:3])
        template_board.append(list_template[3:6])
        template_board.append(list_template[6:9])

        self.assertEqual(tttboard.board, template_board)

class Test_TictactoeBoard_as_one_line_list(unittest.TestCase):
    
    def test_equals(self):
        '''
        This Test Case checks if as_one_line_list returns all marks as one line list.
        I.e.:
        If Board is [[X,X,X], [X,X,X], [X,X,X]] it must return [X,X,X,X,X,X,X,X,X]
        '''

        all_x_board_obj = Board(TicTacToe_utils.string_list_all_X())
        all_x_list = TicTacToe_utils.string_list_all_X()

        self.assertEqual(all_x_list, all_x_board_obj.as_one_line_list())

class Test_tictactoeBoard_get_column(unittest.TestCase):

    def test_get_column(self):
        '''
        This Test Case checks if get_column method is returning a column correctly.
        It creates a board instance as [['X','0','-'], ['X','0','-'], ['X','0','-']]
        and get column 0 (first column that has 'X' only).
        '''
        board = TicTacToe_utils.board_cols_X_Zero_Blank()
        col0 = ['X', 'X', 'X']
        col1 = ['0', '0', '0']
        col2 = ['-', '-', '-']

        self.assertEqual(board.get_column(0), col0)
        self.assertEqual(board.get_column(1), col1)
        self.assertEqual(board.get_column(2), col2)

class Test_tictactoePlayer_subsequente_actions(unittest.TestCase):

    def test_no_action(self):
        '''
        This method checks TictactoePlayer.subsequente_actions(...), returns a empty list
        when board is fully marked
        '''

        board = Board(TicTacToe_utils.string_list_all_X())
        calculated_actions = Player.subsequente_actions(board, 'X')

        expected_actions = []

        self.assertListEqual(expected_actions, calculated_actions)


    def test_one_action(self):
        '''
        This method checks TictactoePlayer.subsequente_actions(...), returns one action
        when only one cell is available to be marked.
        '''

        board = Board(TicTacToe_utils.string_list_lasting_one())
        calculated_actions = Player.subsequente_actions(board, 'X')

        all_x_board = Board(TicTacToe_utils.string_list_all_X())
        expected_actions = [all_x_board]

        self.assertListEqual(expected_actions, calculated_actions)
    
    def test_three_actions(self):
        '''
        This method checks if TicTacToePlayer.subsequente_actions(...), returns a list
        having two actions when only two cels are available.
        '''
        list_marks = ['X', '0', '-', 'X', '-', '0', '-', 'X', '0']
        board = Board(list_marks)
        calculated_actions = Player.subsequente_actions(board, 'X')

        action1 = Board(['X', '0', 'X', 'X', '-', '0', '-', 'X', '0'])
        action2 = Board(['X', '0', '-', 'X', 'X', '0', '-', 'X', '0'])
        action3 = Board(['X', '0', '-', 'X', '-', '0', 'X', 'X', '0'])
        expected_actions = [action1, action2, action3]

        self.assertListEqual(expected_actions, calculated_actions)

class Test_tictactoeplayer_get_left_down_right_up_diagonnal(unittest.TestCase):

    def test_get_empty_diagonal(self):
        '''
        This method checks if the method Tictactoeplayer.get_left_down_right_up_diagonnal()
        is returning the diagonal properly
        '''

        marks = ['X', '0', '-', 'X', '-', '0', '-', '0', 'X']

        board = Board(marks)
        calculated_diagonal = board.get_down_up_diagonnal()

        expected_diagonal = ['-', '-', '-']

        self.assertListEqual(expected_diagonal, calculated_diagonal)

class Test_tictactoeplayer_terminate(unittest.TestCase):
    
    def test_not_terminated(self):
        '''
        This method checks if method terminated() returns false if board
        is not terminated
        '''
        marks = ['-', '-', '-', '-', '-', '-', '-', '-', '-']

        board = Board(marks)
        terminated = Player.terminated(board)

        self.assertEqual(False, terminated)
    
    def test_first_line_terminated(self):
        '''
        This method checks if terminated() method returns true if board
        is terminated with X on first line
        '''

        marks = ['X', 'X', 'X', '0', '-', '0', '0', '-', '-']

        board = Board(marks)
        terminated = Player.terminated(board)

        self.assertEqual(True, terminated)

    def test_second_column_terminated(self):
        '''
        This method checks if terminated() method returns true if board
        is terminated with X on Second  Column
        '''

        marks = ['-', 'X', 'X', '0', 'X', '0', '0', 'X', '-']

        board = Board(marks)
        terminated = Player.terminated(board)

        self.assertEqual(True, terminated)

    def test_up_down_diag_terminated(self):
        '''
        This method checks if terminated() method returns true if board
        is terminated with X on up-down-diagonal.
        '''

        marks = ['X', '-', '0', '-', 'X', '0', '-', '0', 'X']

        board = Board(marks)
        terminated = Player.terminated(board)

        self.assertEqual(True, terminated)

    def test_down_up_diag_terminated(self):
        '''
        This method checks if terminated() method returns true if board
        is terminated with 0 on down-up-diagonal
        '''

        marks = ['-', 'X', '0', '-', '0', 'X', '0', '-', 'X']

        board = Board(marks)
        terminated = Player.terminated(board)

        self.assertEqual(True, terminated)

class Test_tictactoeplayer_final_result(unittest.TestCase):

    def test_not_terminated(self):
        '''
        This method checks if TicTacToePlayer.current_result(board) method 
        returns (None, None) if board is note terminated'''

        marks = ['-', 'X', '0', 'X', '-', '0', 'X', '0', '-']
        board = Board(marks)
        curr_result = Player.current_result(board)

        exp_result = (None, None)

        self.assertTupleEqual(exp_result, curr_result)

    def test_X_cross_col0(self):
        '''
        This method checks if TicTacToePlayer.current_result(board) method
        returns (X, col1) if board is crossed by X at column 0
        '''

        marks = ['X', '-', '0', 'X', '0', '-', 'X', '0', '-']
        board = Board(marks)
        curr_result = Player.current_result(board)

        exp_result = ('X', 'col0')

        self.assertTupleEqual(exp_result, curr_result)

    def test_0_cross_row1(self):
        '''
        This method checks if TicTacToePlayer.current_result(board) method
        returns (0, row1) if board is crossed by 0 at column 1
        '''

        marks = ['-', '-', 'X', '0', '0', '0', 'X', '0', 'X']
        board = Board(marks)
        curr_result = Player.current_result(board)

        exp_result = ('0', 'row1')

        self.assertTupleEqual(exp_result, curr_result)

    def test_X_cross_up_down_diag(self):
        '''
        This method checks if TicTacToePlayer.current_result(board) method
        returns (X, updown) if board is crossed by X up-down-diagonal
        '''

        marks = ['X', '-', 'X', '-', 'X', '0', '0', '0', 'X']
        board = Board(marks)
        curr_result = Player.current_result(board)

        exp_result = ('X', 'updown')

        self.assertTupleEqual(exp_result, curr_result)

    def test_0_cross_down_up_diag(self):
        '''
        This method checks if TicTacToePlayer.current_result(board) method
        returns (0, downup) if board is crossed by 0 down-up-diagonal
        '''

        marks = ['X', '-', '0', '-', '0', 'X', '0', '-', 'X']
        board = Board(marks)
        curr_result = Player.current_result(board)

        exp_result = ('0', 'downup')

        self.assertTupleEqual(exp_result, curr_result)

class Test_tictactoeplayer_cost(unittest.TestCase):

    def test_not_terminated(self):
        '''
        This method checks if TicTacToePlayer.cost(board) method returns
        None, when board is not terminated
        '''

        marks = ['X', '-', '-', '0', 'X', '0', '-', 'X', '0']
        board = Board(marks)
        calc_cost = Player.cost(board, 'X')

        exp_cost = None

        self.assertEqual(exp_cost, calc_cost)

    def test_X_win(self):
        '''
        This method checks if TicTacToePlayer.cost(board) method returns
        1, when X wins.
        '''

        marks = ['X', 'X', 'X', '0', 'X', '0', '-', '0', '0']
        board = Board(marks)
        calc_cost = Player.cost(board, 'X')

        exp_cost = 1

        self.assertEqual(exp_cost, calc_cost)

    def test_0_loose(self):
        '''
        This method checks if TicTacToePlayer.cost(board) method returns
        1, when 0 loose.
        '''

        marks = ['-', '0', '0', 'X', 'X', 'X', '-', '0', '0']
        board = Board(marks)
        calc_cost = Player.cost(board, '0')

        exp_cost = -1

        self.assertEqual(exp_cost, calc_cost)

    def test_even(self):
        '''
        This method checks if TicTacToePlayer.cost(board) method returns
        0, when even.
        '''

        marks = ['X', '0', '0', '0', 'X', 'X', 'X', '0', '0']
        board = Board(marks)
        calc_cost = Player.cost(board, '0')

        exp_cost = 0

        self.assertEqual(exp_cost, calc_cost)

class Test_tictactoe_max_value(unittest.TestCase):

    def test_terminated_win(self):
        '''
        This method checks if TicTacToePlayer.max_value(board, player) method
        returns the max value for a terminated board where player wins
        '''

        marks = ['X', 'X', 'X', '0', '0', '-', '0', 'X', '0']
        board = Board(marks)
        max_value = Player.max_value(board, 'X')
        exp_value = 1

        self.assertEqual(exp_value, max_value)

    def test_terminated_even(self):
        '''
        This method checks if TicTacToePlayer.max_value(board, player) method
        returns the max value for a terminated board when game is even
        '''
        
        marks = ['X', '0', 'X', '0', '0', 'X', '0', 'X', '0']
        board = Board(marks)
        max_value = Player.max_value(board, 'X')

        exp_value = 0

        self.assertEqual(exp_value, max_value)
    
    def test_max_between_even_win(self):
        '''
        This method checks if TicTacToePlayer.max_value(board, player) method
        returns the max value for board where player X wins or even.
        The board is:\n
        X|0|X\n
        0|X|X\n
         -| - |0\n
         The following options are:\n
        X|0|X\n
        0|X|X\n
        X| - |0\n\n
        Then, X wins, or:
        X|0|X\n
        0|X|X\n
         -|X|0\n
         ...\n
         X|0|X\n
        0|X|X\n
        0|X|0\n
        Where the game even.
        In this case, max_valu must return 1, which is the option where X wins
        '''
        
        marks = ['X', '0', 'X', '0', 'X', 'X', '-', '-', '0']
        board = Board(marks)
        max_value = Player.max_value(board, 'X')

        exp_value = 1

        self.assertEqual(exp_value, max_value)

class Test_tictactoe_min_value(unittest.TestCase):

    def test_terminated_loose(self):
        '''
        This method checks if TicTacToePlayer.min_value(board, player) method
        returns the min value for a terminated board where player looses
        '''
        
        marks = ['X', 'X', 'X', '0', '0', '-', '0', 'X', '0']
        board = Board(marks)
        min_value = Player.min_value(board, '0')

        exp_value = -1

        self.assertEqual(exp_value, min_value)

    def test_terminated_even(self):
        '''
        This method checks if TicTacToePlayer.min_value(board, player) method
        returns the min value for a terminated board where the game even
        '''
        
        marks = ['X', '0', 'X', '0', '0', 'X', '0', 'X', '0']
        board = Board(marks)
        min_value = Player.min_value(board, '0')

        exp_value = 0

        self.assertEqual(exp_value, min_value)


if __name__ == "__main__":
    unittest.main()
    #print(TicTacToe_utils.string_board_all_X())