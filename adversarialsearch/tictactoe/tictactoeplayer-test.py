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

setlog.set_log(logging.INFO)

class Test_Player_actions(unittest.TestCase):

    def test_no_action(self):
        '''
        This method checks TictactoePlayer.actions(...), returns a empty
        list when board is fully marked
        '''
        logging.info(f'Testing if Player.actions() returns empty if board is even')

        board = Board(['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'])
        actions = Player.actions(board, 'X')

        expected_actions = []

        self.assertListEqual(expected_actions, actions)


    def test_one_action(self):
        '''
        This method checks if TictactoePlayer.actions(...),
        returns one action when only one cell is available to be marked.
        '''

        logging.info(f"Checking if Player.action() returns one action")

        board = Board(['X', '0', '0', 'X', '0', '0', '-', 'X', 'X'])
        actions = Player.actions(board, 'X')

        expected_board = Board(['X', '0', '0', 'X', '0', '0', 'X', 'X', 'X'])        
        expected_actions = [Action(expected_board, (2, 0), None)]

        [self.assertEqual(expected_actions[i], actions[i]) for i in range(len(actions))]
    
    def test_three_actions(self):
        '''
        This method checks if TicTacToePlayer.actions(...), returns a list
        having three actions when only two cels are available.
        '''

        logging.debug(f"Checking if Player.action() returns three actions")
        
        board = Board(['X', '0', '-', 'X', '-', '0', '-', 'X', '0'])
        actions = Player.actions(board, 'X')

        b1 = Board(['X', '0', 'X', 'X', '-', '0', '-', 'X', '0'])
        a1 = Action(b1, (0,2), None)

        b2 = Board(['X', '0', '-', 'X', 'X', '0', '-', 'X', '0'])
        a2 = Action(b2, (1,1), None)

        b3 = Board(['X', '0', '-', 'X', '-', '0', 'X', 'X', '0'])
        a3 = Action(b3, (2,0), None)
        expected_actions = [a1, a2, a3]

        [self.assertEqual(expected_actions[i], actions[i]) for i in range(2)]

class Test_player_utility(unittest.TestCase):

    def test_not_terminated(self):
        '''
        This method checks if TicTacToePlayer.utility(board) method returns
        None, when board is not terminated
        '''

        logging.info("Checking if Player.calc_utility() returns empty if board is not terminated")

        marks = ['X', '-', '-', '0', 'X', '0', '-', 'X', '0']
        board = Board(marks)
        utility = Player.calc_utility(board, 'X')

        exp_cost = None

        self.assertEqual(exp_cost, utility)

    def test_X_win(self):
        '''
        This method checks if TicTacToePlayer.calc_utility(board) method returns
        1, when X wins.
        '''

        logging.info(f"Checking if Player.calc_utility() returns 1 when player wins")

        marks = ['X', 'X', 'X', '0', 'X', '0', '-', '0', '0']
        board = Board(marks)
        utility = Player.calc_utility(board, 'X')

        exp_utility = 1

        self.assertEqual(exp_utility, utility)

    def test_0_loose(self):
        '''
        This method checks if TicTacToePlayer.calc_utility(board) method returns
        1, when 0 loose.
        '''

        logging.info(f"Checking if Player.calc_utility() returns -1 when player looses")

        marks = ['-', '0', '0', 'X', 'X', 'X', '-', '0', '0']
        board = Board(marks)
        calc_utility = Player.calc_utility(board, '0')

        exp_cost = -1

        self.assertEqual(exp_cost, calc_utility)

    def test_even(self):
        '''
        This method checks if TicTacToePlayer.calc_utility(board) method returns
        0, when even.
        '''

        logging.info(f"Checking if Player.calc_utility() returns 0 when game is even")

        marks = ['X', '0', '0', '0', 'X', 'X', 'X', '0', '0']
        board = Board(marks)
        calc_cost = Player.calc_utility(board, '0')

        exp_cost = 0

        self.assertEqual(exp_cost, calc_cost)

class Test_max_value(unittest.TestCase):

    def test_terminated_win(self):
        '''
        This method checks if TicTacToePlayer.max_value(board) method
        returns +1 if `board` is terminated and X player wins.
        '''

        logging.info(f"Checking if Player.max_value() returns 1 when there is only one move and player wins")

        marks = ['X', 'X', 'X', '0', '0', '-', '0', 'X', '0']
        board = Board(marks)
        max_value = Player.max_value(board, 'X')
        exp_value = 1

        self.assertEqual(exp_value, max_value)

    def test_even(self):
        '''
        This method checks if TicTacToePlayer.max_value(board, player) method
        returns the 0 for a terminated board when game is even
        '''

        logging.info(f"Checking if Player.max_value() returns 0 when game is even")
        
        marks = ['X', '0', 'X', '0', '0', 'X', '0', 'X', '0']
        board = Board(marks)
        max_value = Player.max_value(board, 'X')

        exp_value = 0

        self.assertEqual(exp_value, max_value)
    
    def test_max_between_even_win(self):
        '''
        This method checks if TicTacToePlayer.max_value(board, player) method
        returns the max value for state where subsequente moves are win or even.
        As subsequente is the opponent's turn, for him is a choose between 
        loose (-1) or even (0). In this case, max_value must return 0.
        Current State:\n
        X|0|X\n
        0|X|X\n
         -| - |0\n
        Opponent options are:\n
        X|0|X\n
        0|X|X\n
        0| - |0\n\n
        Then player marks:\n
        X|0|X\n
        0|X|X\n
        0|X|0\n
        \n
        The result is even(0), or opponent hits:\n        
        X|0|X\n
        0|X|X\n
         -|0|0\n
        Then player marks:\n
        X|0|X\n
        0|X|X\n
        X|0|0\n
        The result is X wins, 0 looses (-1).

        In this case, max_value must return 0, which is the better option for opponent
        '''

        logging.info(f"Checking if Player.max_value() returns 0 when there is 2 moves where player wins or even")
        
        marks = ['X', '0', 'X', '0', 'X', 'X', '-', '-', '0']
        board = Board(marks)
        max_value = Player.max_value(board, 'X')

        exp_value = 1

        self.assertEqual(exp_value, max_value)

    def test_player_win(self):
        '''
        This method checks if Player.max_value(...) returns 1 in case where
        player always wins
        '''

        logging.info(f"Checking if Player.max_value() returns 1 when there is 2 moves lasting and on both cases player wins")

        board = Board(['0', 'X', 'X', 'X', 'X', '0', '-', '-', '0'])
        max_value = Player.max_value(board, 'X')

        exp_value = 1

        logging.info(f"max_value={max_value}; expected_value={exp_value}")
        self.assertEqual(exp_value, max_value)

class Test_Player_min_value(unittest.TestCase):

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