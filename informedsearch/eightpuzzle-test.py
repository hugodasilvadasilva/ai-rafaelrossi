'''
This block of code implements a GPS to find a route between 2 cities by using Greedy Best First algorithm,
which uses the least estimated distance to destination to choose the next node to be analysed.
At Search 4, there is a example where this algorithm fails to find a solution, as closer city to destination
has no route to there.
This problem is solved by using BestFirst.
'''

import enum
from os import sched_rr_get_interval
import unittest
import logging
from functools import reduce
from eightpuzzle import EightPuzzle, Strategy

"""
Description
---------
Set log configuration at formmat `dd/mm/aaaa hh:mn:ss am/pm message`.
The log level must be informe at `level` variable.

Levels
----------
Define log level by setting `level` variable with some of the followings
values:
- logging.DEBUG,
- logging.INFO,
- logging.WARNING,
- logging.ERROR,
- logging.CRITICAL.

"""
level = logging.DEBUG

logging.basicConfig(format="%(asctime)s # At %(funcName)s # Line %(lineno)d # %(message)s", level=level, datefmt='%d/%m/%Y %I:%M:%S %p')

logging.debug("Log de debug registrado")
logging.info("Log de info registrado")
logging.warning("Log de warning registrado")
logging.error("Log de error registrado")
logging.critical("Log crítico registrado")

class Test_EightPuzzle_calc_manhattan_distance(unittest.TestCase):

    def test_equals(self):
        '''
        This Test Case calculates the manhattan distance between 0,0 and 0,0
        '''
        dist = EightPuzzle.calc_manhatan_distance((0,0), (0,0))
        self.assertEquals(0, dist)

    def test_negative(self):
        '''
        This Test Case calculates the manhattan distance between -1, -1 and 0, 0
        '''
        dist = EightPuzzle.calc_manhatan_distance((-1,-1), (0,0))
        self.assertEquals(2, dist)

    def test_negative_positive(self):
        '''
        This Test Case calculates the manhattan distance between -1, -1 and 1, 1
        '''
        dist = EightPuzzle.calc_manhatan_distance((-1,-1), (1,1))
        self.assertEquals(4, dist)

class Test_EightPuzzle_calc_heuristic_value(unittest.TestCase):
    
    def test_heuristic_zero(self):
        '''
        This test case calculates the heuristic value between two similar boards
        so heuristic must be zero
        '''

        board = [[0,1,2], [3,4,5], [6,7,8]]
        heuristic_value = EightPuzzle.calc_heuristic_value(board, board)
        self.assertEqual(0, heuristic_value)
    
    def test_heuristic_lines_switched(self):
        '''
        This test case checks if calc_heuristic_value is calculating properly
        when numbers are in different lines.
        '''

        boardA = [[0,1,2], [3,4,5], [6,7,8]]
        boardB = [[6,7,8], [0,1,2], [3,4,5]]
        heuristic_value = EightPuzzle.calc_heuristic_value(boardA, boardB)
        self.assertEqual(12, heuristic_value)

    def test_heuristic_columns_switched(self):
        '''
        This test case checks if calc_heuristic_value is calculating properly
        when number are in different columns but at same line
        '''

        boardA = [[0,1,2], [3,4,5], [6,7,8]]
        boardB = [[1,2,0], [4,5,3], [7,8,6]]
        heuristic_value = EightPuzzle.calc_heuristic_value(boardA, boardB)
        self.assertEqual(12, heuristic_value)

class Strategy_add_state(unittest.TestCase):

    def test_add_one_move(self):
        '''
        This test case checks if add_state is working properly by adding
        one state with one step moved
        '''

        first_board = [[0,1,2], [3,4,5], [6,7,8]]

        stg = Strategy([first_board], 0)

        second_board = [[1,0,2], [3,4,5], [6,7,8]]

        stg.add_state(second_board)

        self.assertEqual(2, stg.cost_value)

class EightPuzzle_move(unittest.TestCase):

    def test_move_up_zero_at_top(self):
        '''
        This test case checks if move_up method returnes None if you try to
        move zero up if zero is at line 0
        '''

        b = [[0,1,2], [3,4,5], [6,7,8]]
        new_b = EightPuzzle.move(b, (-1,0))
        self.assertEqual(None, new_b)
    
    def test_move_up_zero_not_at_top(self):
        '''
        This test case checks if move_up method returnes a new board if
        you try to move zero up, as zero is at line 2
        '''

        b = [[1,2,3], [0,4,5], [6,7,8]]
        new_b = EightPuzzle.move(b, (-1,0))
        self.assertEqual([[0,2,3], [1,4,5], [6,7,8]], new_b)

    def test_move_down_zero_at_bottom(self):
        '''
        This test case checks if move_down method returnes None if you try to
        move zero down if zero is at line 2 (bottom)
        '''

        b = [[6,1,2], [3,4,5], [0,7,8]]
        new_b = EightPuzzle.move(b, (1,0))
        self.assertEqual(None, new_b)
    
    def test_move_down_zero_not_at_bottom(self):
        '''
        This test case checks if move_dowm method returnes a new board if
        you try to move zero down, as zero is at line 1
        '''

        b = [[1,2,3], [0,4,5], [6,7,8]]
        new_b = EightPuzzle.move(b, (1,0))
        self.assertEqual([[1,2,3], [6,4,5], [0,7,8]], new_b)

    def test_move_left_zero_at_left(self):
        '''
        This test case checks if move_left method returnes None if you try to
        move zero left if zero is at column 0 (left)
        '''

        b = [[0,1,2], [3,4,5], [6,7,8]]
        new_b = EightPuzzle.move(b, (0, -1))
        self.assertEqual(None, new_b)
    
    def test_move_left_zero_not_at_left(self):
        '''
        This test case checks if move_left method returnes a new board if
        you try to move zero left, as zero is at column 1
        '''

        b = [[1,2,3], [4,0,5], [6,7,8]]
        new_b = EightPuzzle.move(b, (0,-1))
        self.assertEqual([[1,2,3], [0,4,5], [6,7,8]], new_b)

    def test_move_right_zero_at_right(self):
        '''
        This test case checks if move_right method returnes None if you try to
        move zero right if zero is at column 2 (rightest)
        '''

        b = [[1,2,0], [3,4,5], [6,7,8]]
        new_b = EightPuzzle.move(b, (0,1))
        self.assertEqual(None, new_b)
    
    def test_move_right_zero_not_at_right(self):
        '''
        This test case checks if move_right method returnes a new board if
        you try to move zero right, as zero is at column 1
        '''

        b = [[1,2,3], [4,0,5], [6,7,8]]
        new_b = EightPuzzle.move(b, (0,1))
        self.assertEqual([[1,2,3], [4,5, 0], [6,7,8]], new_b)

class EightPuzzle_get_surroudings(unittest.TestCase):

    def test_get_surroudings_zero_in_the_middle(self):

        b = [[1,2,3], [4,0,5], [6,7,8]]
        b_surroundings = EightPuzzle.get_surroundings(b)
        b_expected = [[[1,0,3], [4,2,5], [6,7,8]], [[1,2,3], [4,7,5], [6,0,8]], [[1,2,3], [0,4,5], [6,7,8]], [[1,2,3], [4,5,0], [6,7,8]]]

        self.assertEqual(b_expected, b_surroundings)


if __name__ == "__main__":
    unittest.main()