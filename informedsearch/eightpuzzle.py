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
level = logging.INFO

logging.basicConfig(format="%(asctime)s # At %(funcName)s # Line %(lineno)d # %(message)s", level=level, datefmt='%d/%m/%Y %I:%M:%S %p')

logging.debug("Log de debug registrado")
logging.info("Log de info registrado")
logging.warning("Log de warning registrado")
logging.error("Log de error registrado")
logging.critical("Log crítico registrado")

class Strategy:
    '''
    The strategy is a list of states of EightPuzzle
    resulted by a sequence of moves.
    It also has a `cost_value` which is the sum
    of all move_
    '''

    def __init__(self, states: list, cost_value: int, heuristic_value: int):
        self.__states = states
        self.__cost_value = cost_value
        self.__heuristic_value = heuristic_value

    def __repr__(self) -> str:
        return f"Strategy: states = {self.__states}; cost value = {self.cost_value}; heuristic value = {self.heuristic_value}; evaluation value = {self.evaluation_value}"
    
    def summary(self) -> str:
        return f"Strategy: current_state={self.states[-1]}; cost value = {self.cost_value}; heuristic value = {self.heuristic_value}; evaluation value = {self.evaluation_value}"

    def copy(self):
        logging.debug(f"Creating new Strategy from {self}")
        new_states = [line.copy() for line in [state for state in self.__states]]
        return Strategy(new_states, self.cost_value, self.heuristic_value)

    @property
    def states(self):
        return self.__states

    @property
    def cost_value(self):
        return self.__cost_value

    @property
    def heuristic_value(self):
        return self.__heuristic_value

    @property
    def evaluation_value(self):
        return self.__cost_value + self.__heuristic_value

    def add_state(self, state: list, target_state: list):

        logging.debug(f"Adding state {state} to {self}")

        last_state = self.__states[-1]
        logging.debug(f"Retriving strategy's last state: {last_state}")

        cost = 2
        heuristic = EightPuzzle.calc_heuristic_value(state, target_state)
        
        self.__states.append(state)
        self.__cost_value += cost
        self.__heuristic_value = heuristic
        logging.debug(f"State {state} added to {self}")

                

class EightPuzzle:
    '''
    This class represents a 8 puzzle board.
    '''

    def __init__(self, list_of_numbers: list):

        #Stores list_of_numbers in form of a 3x3 matrix
        self.__initial_state = [list_of_numbers[i*3:i*3+3] for i in range(0,3)]
        logging.debug(f"Board created: {self.__initial_state}")

        #Solution
        self.__solution = [[1,2,3], [4,0,5],[6,7,8]]

        #Stores all tried states to solve the problme
        self.__tried = []

        # stores moves to be tried
        self.__fringe = []

    def __repr__(self) -> str:
        return str(self.__initial_state)

    def copy_board(board: list) -> list:
        '''
        This method creates a copy) of a board, in other words, another object having
        the same list of items (integers). For some reason, the method list.copy()
        doesn't work properly for a list of lists, so this method was created to solve
        this problem.
        '''
        new_board = [sublist.copy() for sublist in board]
        return new_board


    def number_position(number: int, board: list) -> tuple:
        '''
        This method returns a tuple containing the line and row number of `number`
        into `board`.
        `- number: int` which is the number that is been searched;
        `- board: list` of 3x3 where `number` is been searched and you want
        `number`'s position
        `- return: tuple` as (lin, col) where lin is the line number and col is
        the column number of `number`. If `number` is not find, returns `None`.
        '''

        logging.debug(f"Finding position of number {number} at board {board}")
        # TODO: erro aqui
        x = -1
        for line in board:
            x += 1
            if number in line:
                y = line.index(number)
                logging.debug(f"Number {number} found at position {x,y}")
                return (x, y)
        else:
            logging.debug(f"Number {number} was not found at board {board}")
            return None
    
    def calc_manhatan_distance(posA: tuple, posB: tuple) -> int:
        '''
        Calculates the manhathan distance between `posA` and `posB`.

        ## Parameters
        `- posA: tuple` as (x, y) position where x is the line number and y is the 
        column number;
        `- posB: tuple` as (x, y) position where x is the line number and y is the 
        column number;
        `- return: int` having the manhatan distance between `posA` and `posB`.
        '''

        logging.debug(f"Calculating Manhathan Distance between {posA} and {posB}")

        x_dist = abs(posA[0] - posB[0])
        y_dist = abs(posA[1] - posB[1])
        logging.debug(f"Manhathan Distance between {posA} and {posB} calculated: x_distance = {x_dist}, y_distance = {y_dist}, total_distance = {x_dist + y_dist}.")
        return x_dist + y_dist

    def calc_heuristic_value(stateA: list, stateB: list) -> int:
        '''
        Calculates the cost value between `stateA` and `stateB` which is 
        manhatan distance between each number.
        
        ## Parameters
        `- stateA: list` of 3x3 having numbers from 0 to 8;
        `- stateB: list` of 3x3 having numbers from 0 to 8;
        `- return: int` having the manhatan distance between stateA and
        stateB
        '''

        logging.debug(f"Starting to calculate the cost between {stateA} and {stateB}")

        total_cost = 0
        for i in range(3):
            for j in range(3):
                curr_number = stateA[i][j]
                logging.debug(f"Calculanting the cost of {curr_number}")
                logging.debug(f"Number {curr_number} is at position {(i,j)} in {stateA}")

                position_at_B = EightPuzzle.number_position(curr_number, stateB)
                logging.debug(f"Number {curr_number} is at position {position_at_B} in {stateB}")

                if(position_at_B != None):
                    curr_cost = EightPuzzle.calc_manhatan_distance((i,j), position_at_B)
                    logging.debug(f"Cost of number {curr_number} is {curr_cost}")

                    total_cost += curr_cost
        
        logging.debug(f"Total cost between {stateA} and {stateB} is {total_cost}")
        return total_cost


    def add_strategy_to_fringe(self, strategy: Strategy):
        
        logging.debug(f"Adding {strategy} to fringe")
        
        for index, curr_strategy in enumerate(self.__fringe):

            if strategy.heuristic_value > curr_strategy.heuristic_value:
                logging.debug(f"{strategy} added at position {index}")
                self.__fringe.insert(index, strategy)
                logging.debug(f"New Fringe: {strategy.states[-1]} ")
                return
        else:
            logging.debug(f"{strategy} added at position 0")
            self.__fringe.append(strategy)
    
    def move(board: list, rel_coord: tuple) -> list:
        '''
        Moves 0 at `board` to right, left, up or down. You can specify directions
        at parameter `rel_coord`.
        
        ## Parameters
        `- board: list` board where 0 will be moved;
        `- rel_coord: tuple` as (`int`, `int`) having the relative position. The direction's value are bellow:
         > `left`: (0, -1);
         > `right`: (0, 1);
         > `up`: (-1, 0);
         > `down`: (1, 0).
        `- return: list` having a new board (new object) with zero moved to new position.
        '''

        logging.debug(f"Moving number 0 at board {board} on to {rel_coord}")

        new_board = EightPuzzle.copy_board(board=board)

        zero_position = EightPuzzle.number_position(0, new_board)

        zero_line = zero_position[0]
        new_line = zero_line + rel_coord[0]
        if new_line > 2 or new_line < 0:
            logging.debug(f"Number 0 can not be moved to line {new_line}")
            return None

        zero_column = zero_position[1]
        new_column = zero_column + rel_coord[1]
        if new_column > 2 or new_column < 0:
            logging.debug(f"Number 0 can not be moved to column {new_column}")
            return None
        
        new_board[zero_line][zero_column] = new_board[new_line][new_column]
        new_board[new_line][new_column] = 0
        logging.debug(f"Number 0 moved. New board is {new_board}")

        return new_board


    def get_surroundings(board: list) -> list:
        '''
        Returns a list of boards where each one of them is a zero
        moved onto certain direction.
        The list of boards will follow this order or zero moved
        directions: up, down, left, right'''

        next_step_boards = []
        for direction in [(-1,0), (1,0), (0,-1), (0,1)]:

            moved_board = EightPuzzle.move(board, direction)
            if moved_board != None:
                next_step_boards.append(moved_board.copy())
        
        return next_step_boards



    def solve_using_a_star(self):

        logging.info(f"Starting Eight Puzzle solution by using A-Star algorithm")
        
        # add current state to fringe
        curr_state = EightPuzzle.copy_board(self.__initial_state)

        heuristic_value = EightPuzzle.calc_heuristic_value(curr_state, self.__solution)

        stg = Strategy([curr_state], 0, heuristic_value)
        self.add_strategy_to_fringe(stg)
        move_num = 0

        while self.__fringe:

            # get next strategy to be tried
            move_num += 1
            logging.debug(f"\nCurrent Fringe State\n {[s.summary() for s in self.__fringe]}")

            curr_strategy = self.__fringe.pop(-1)
            logging.debug(f"\nStrategy picked={curr_strategy.summary()}")

            logging.info(f"### Move {move_num} ###")
            [print(l) for l in curr_strategy.states[-1]]

            # check if is solution
            logging.debug(f"Checking if {curr_strategy.states[-1]} is equal to {self.__solution}")
            if curr_strategy.states[-1] == self.__solution:
                return curr_strategy

            # if not solution, add to list of tried states
            logging.debug(f"{curr_strategy.states[-1]} added to list of tried positions")
            self.__tried.append(curr_strategy.states[-1])
            
            # get next moves
            next_moves = EightPuzzle.get_surroundings(curr_strategy.states[-1])

            for move in next_moves:

                logging.debug(f"Checking if {move} has already been tried")
                if move in self.__tried:
                    continue

                new_strategy = curr_strategy.copy()
                new_strategy.add_state(move, self.__solution)
                self.add_strategy_to_fringe(new_strategy)

if __name__ == "__main__":
    puzzle = EightPuzzle([1,3,2,6,4,5,8,7,0])
    strategy = puzzle.solve_using_a_star()

    print(f"Puzzle solved")