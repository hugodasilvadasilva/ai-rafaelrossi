'''
This block of code implements the testcase of Tic Tac Toe Player.
'''
import logging
import unittest
import setlog
from tictactoeplayer import TicTacToePlayer as Player
from tictactoeboard import TicTacToeBoard as Board
from tictactoeaction import TicTacToeAction as Action
from tictactoegame import TicTacToeGame as Game

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

class Test_Player_actions(unittest.TestCase):

    def test_no_action(self):
        '''
        This method checks TictactoePlayer.actions(...), returns a empty
        list when board is fully marked
        '''

        player = Player('X')
        board = Board(['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'])
        actions = player.actions(board)

        expected_actions = []

        self.assertListEqual(expected_actions, actions)


    def test_one_action(self):
        '''
        This method checks if TictactoePlayer.actions(...),
        returns one action when only one cell is available to be marked.
        '''

        board = Board(['X', '0', '0', 'X', '0', '0', '-', 'X', 'X'])
        player = Player('X')
        actions = player.actions(board)

        expected_board = Board(['X', '0', '0', 'X', '0', '0', 'X', 'X', 'X'])        
        expected_actions = [Action(expected_board, (2, 0), None)]

        [self.assertEqual(expected_actions[i], actions[i]) for i in range(len(actions))]
    
    def test_three_actions(self):
        '''
        This method checks if TicTacToePlayer.actions(...), returns a list
        having three actions when only two cels are available.
        '''
        
        board = Board(['X', '0', '-', 'X', '-', '0', '-', 'X', '0'])
        player = Player('X')
        actions = player.actions(board)

        b1 = Board(['X', '0', 'X', 'X', '-', '0', '-', 'X', '0'])
        a1 = Action(b1, (0,2), None)

        b2 = Board(['X', '0', '-', 'X', 'X', '0', '-', 'X', '0'])
        a2 = Action(b2, (1,1), None)

        b3 = Board(['X', '0', '-', 'X', '-', '0', 'X', 'X', '0'])
        a3 = Action(b3, (2,0), None)
        expected_actions = [a1, a2, a3]

        [self.assertEqual(expected_actions[i], actions[i]) for i in range(2)]

class Test_player_get_down_up_diagonnal(unittest.TestCase):

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

class Test_player_terminate(unittest.TestCase):
    
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
        This method checks if Player.terminate() returns false if board
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

    def est_second_column_terminated(self):
        '''
        This method checks if terminated() method returns true if board
        is terminated with X on Second  Column
        '''

        marks = ['-', 'X', 'X', '0', 'X', '0', '0', 'X', '-']

        board = Board(marks)
        terminated = Player.terminated(board)

        self.assertEqual(True, terminated)

    def est_up_down_diag_terminated(self):
        '''
        This method checks if terminated() method returns true if board
        is terminated with X on up-down-diagonal.
        '''

        marks = ['X', '-', '0', '-', 'X', '0', '-', '0', 'X']

        board = Board(marks)
        terminated = Player.terminated(board)

        self.assertEqual(True, terminated)

    def est_down_up_diag_terminated(self):
        '''
        This method checks if terminated() method returns true if board
        is terminated with 0 on down-up-diagonal
        '''

        marks = ['-', 'X', '0', '-', '0', 'X', '0', '-', 'X']

        board = Board(marks)
        terminated = Player.terminated(board)

        self.assertEqual(True, terminated)

class Test_player_final_result(unittest.TestCase):

    def est_not_terminated(self):
        '''
        This method checks if TicTacToePlayer.current_result(board) method 
        returns (None, None) if board is note terminated'''

        marks = ['-', 'X', '0', 'X', '-', '0', 'X', '0', '-']
        board = Board(marks)
        curr_result = Player.current_result(board)

        exp_result = (None, None)

        self.assertTupleEqual(exp_result, curr_result)

    def est_X_cross_col0(self):
        '''
        This method checks if TicTacToePlayer.current_result(board) method
        returns (X, col1) if board is crossed by X at column 0
        '''

        marks = ['X', '-', '0', 'X', '0', '-', 'X', '0', '-']
        board = Board(marks)
        curr_result = Player.current_result(board)

        exp_result = ('X', 'col0')

        self.assertTupleEqual(exp_result, curr_result)

    def est_0_cross_row1(self):
        '''
        This method checks if TicTacToePlayer.current_result(board) method
        returns (0, row1) if board is crossed by 0 at column 1
        '''

        marks = ['-', '-', 'X', '0', '0', '0', 'X', '0', 'X']
        board = Board(marks)
        curr_result = Player.current_result(board)

        exp_result = ('0', 'row1')

        self.assertTupleEqual(exp_result, curr_result)

    def est_X_cross_up_down_diag(self):
        '''
        This method checks if TicTacToePlayer.current_result(board) method
        returns (X, updown) if board is crossed by X up-down-diagonal
        '''

        marks = ['X', '-', 'X', '-', 'X', '0', '0', '0', 'X']
        board = Board(marks)
        curr_result = Player.current_result(board)

        exp_result = ('X', 'updown')

        self.assertTupleEqual(exp_result, curr_result)

    def est_0_cross_down_up_diag(self):
        '''
        This method checks if TicTacToePlayer.current_result(board) method
        returns (0, downup) if board is crossed by 0 down-up-diagonal
        '''

        marks = ['X', '-', '0', '-', '0', 'X', '0', '-', 'X']
        board = Board(marks)
        curr_result = Player.current_result(board)

        exp_result = ('0', 'downup')

        self.assertTupleEqual(exp_result, curr_result)

class Test_player_cost(unittest.TestCase):

    def est_not_terminated(self):
        '''
        This method checks if TicTacToePlayer.cost(board) method returns
        None, when board is not terminated
        '''

        marks = ['X', '-', '-', '0', 'X', '0', '-', 'X', '0']
        board = Board(marks)
        calc_cost = Player.cost(board, 'X')

        exp_cost = None

        self.assertEqual(exp_cost, calc_cost)

    def est_X_win(self):
        '''
        This method checks if TicTacToePlayer.cost(board) method returns
        1, when X wins.
        '''

        marks = ['X', 'X', 'X', '0', 'X', '0', '-', '0', '0']
        board = Board(marks)
        calc_cost = Player.cost(board, 'X')

        exp_cost = 1

        self.assertEqual(exp_cost, calc_cost)

    def est_0_loose(self):
        '''
        This method checks if TicTacToePlayer.cost(board) method returns
        1, when 0 loose.
        '''

        marks = ['-', '0', '0', 'X', 'X', 'X', '-', '0', '0']
        board = Board(marks)
        calc_cost = Player.cost(board, '0')

        exp_cost = -1

        self.assertEqual(exp_cost, calc_cost)

    def est_even(self):
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

    def est_terminated_win(self):
        '''
        This method checks if TicTacToePlayer.max_value(board, player) method
        returns correct action if `board` is terminated and X plawyer won.
        '''

        marks = ['X', 'X', 'X', '0', '0', '-', '0', 'X', '0']
        board = Board(marks)
        action = Player.max_value(board, 'X')
        exp_action = Action(board, (None, None), 'X')

        self.assertEqual(exp_action, action)

    def est_terminated_even(self):
        '''
        This method checks if TicTacToePlayer.max_value(board, player) method
        returns the max value for a terminated board when game is even
        '''
        
        marks = ['X', '0', 'X', '0', '0', 'X', '0', 'X', '0']
        board = Board(marks)
        max_value = Player.max_value(board, 'X')

        exp_value = 0

        self.assertEqual(exp_value, max_value)
    
    def est_max_between_even_win(self):
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

    def est_terminated_loose(self):
        '''
        This method checks if TicTacToePlayer.min_value(board, player) method
        returns the min value for a terminated board where player looses
        '''
        
        marks = ['X', 'X', 'X', '0', '0', '-', '0', 'X', '0']
        board = Board(marks)
        min_value = Player.min_value(board, '0')

        exp_value = -1

        self.assertEqual(exp_value, min_value)

    def est_terminated_even(self):
        '''
        This method checks if TicTacToePlayer.min_value(board, player) method
        returns the min value for a terminated board where the game even
        '''
        
        marks = ['X', '0', 'X', '0', '0', 'X', '0', 'X', '0']
        board = Board(marks)
        min_value = Player.min_value(board, '0')

        exp_value = 0

        self.assertEqual(exp_value, min_value)

class Test_tictactoe_max_value(unittest.TestCase):

    def est_terminated_win(self):
        '''
        This method checks if TicTacToePlayer.max_value(board, player) method
        returns the max value for a terminated board where player wins
        '''

        marks = ['X', 'X', 'X', '0', '0', '-', '0', 'X', '0']
        board = Board(marks)
        max_value = Player.max_value(board, 'X')
        exp_value = 1

        self.assertEqual(exp_value, max_value)

    def est_terminated_even(self):
        '''
        This method checks if TicTacToePlayer.max_value(board, player) method
        returns the max value for a terminated board when game is even
        '''
        
        marks = ['X', '0', 'X', '0', '0', 'X', '0', 'X', '0']
        board = Board(marks)
        max_value = Player.max_value(board, 'X')

        exp_value = 0

        self.assertEqual(exp_value, max_value)
    
    def est_max_between_even_win(self):
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


if __name__ == "__main__":
    unittest.main()
    #print(TicTacToe_utils.string_board_all_X())