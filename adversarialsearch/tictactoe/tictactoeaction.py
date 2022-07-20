import copy
import setlog
import logging
from tictactoeboard import TicTacToeBoard as Board

setlog.set_log(logging.DEBUG)

class TicTacToeAction:
    '''
    This class represents one action over Board, which
    means any  next move that can be done
    '''

    def __init__(self, action_board: Board, row_col_action: tuple, utility_value: int):
        '''
        Initialize the class `TicTacToeAction` class.
        
        ## Parameters
        `- action_board: Board` having the board state if player moves 
        as suggested by this action.
        `- row_col_action: tuple` having the `row, column` of action
        `- cost: int` the cost of the action. If is not determined
        yet, `cost` must be `None`
        '''
        self.__action_board = action_board
        self.__row_col_action = row_col_action
        self.__utility_value = utility_value
    
    def __repr__(self) -> str:
        return f"Action: board={self.__action_board.as_one_line_list()}; row_col={self.__row_col_action}; utility={self.__utility_value}"
    
    def __eq__(self, __o: object) -> bool:
        return self.board == __o.board and self.row_col == __o.row_col and self.utility == __o.utility
    

    @property
    def board(self) -> Board:
        '''
        Returns the board state if action is executed
        '''
        return self.__action_board
    
    @property
    def utility(self) -> int:
        '''
        Returns the utility of action.
        If utility has not been 
        '''
        return self.__utility_value

    @property
    def row_col(self) -> tuple:
        '''
        Returns the row_col of action
        If actions has not been defined yet, return (None, None)
        '''
        return self.__row_col_action

    @utility.setter
    def utility(self, utility: int):
        self.__utility_value = utility    