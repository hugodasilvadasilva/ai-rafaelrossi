import logging
from tictactoeboard import TicTacToeBoard as Board
from tictactoeaction import TicTacToeAction as Action


class TicTacToePlayer:

    def __init__(self, symbol: str):
        self.__symbol = symbol

    def __repr__(self) -> str:
        return f"Player '{self.__symbol}'"

    @property
    def symbol(self) -> str:
        return self.__symbol
            
        
    def actions(board: Board, player: str) -> list:
        '''
        This method analyse all possible subsequence moves at `board` for `player`.
        
        ## Parameters
        `- board: Board` representing the current board state;
        `- player: str` symbol that represents the player. It must be 'X' or '0';
        `- return: list` of TicTacToeActions where each one of them is a possible subsequente
        state. Those actions have `board` and `move` property setted, but `cost` equals to `None`.        
        '''

        states = []
        for n_row, row in enumerate(board.board):
            for n_col, cell in enumerate(row):
                if cell == "-":
                    new_board = Board(board.as_one_line_list())
                    new_board.set_cel(n_row, n_col, player)
                    new_action = Action(new_board, (n_row, n_col), None)
                    states.append(new_action)
                    logging.debug(f"New {new_action} created for board {board.as_one_line_list()}")
        
        logging.debug(f"{len(states)} states found for board {board.as_one_line_list()}")
        return states
    
    def calc_utility(board: Board, player: str) -> int:
        '''
        Calculate the utility of `board` for `player`.
        
        ## Parameters
        `- board: Board` which utility is been analised;
        `- player: str` having `X` or `0` to identifying which player
        the utility is been calculated;
        `- return: int` -1, if player looses, 0 if even and +1 if wins.
        If `board` is not terminated, returns None'''

        opponent = 'X'
        if player == opponent:
            opponent = '0'

        curr_result = board.current_result()
        
        if curr_result[0] == player:
            final_result = 1
        elif curr_result[0] == opponent:
            final_result = -1
        elif curr_result[0] == '-':
            final_result = 0
        else:
            final_result = curr_result[0]
        
        logging.debug(f"Utility of {board.as_one_line_list()} for player {player} is {final_result}")
        return final_result


    def max_value(board: Board, player: str) -> int:

        utility = TicTacToePlayer.calc_utility(board, player)

        # If board is terminated, return its utility for player
        if  utility != None:
            logging.debug(f"Max value for player {player} at board {board.as_one_line_list()} is {utility}")
            return utility

        # if board is not terminated check subsequente actions
        actions = TicTacToePlayer.actions(board, player)

        max_value = -1000

        for action in actions:

            action_value = TicTacToePlayer.min_value(action.board, player)

            if action_value > max_value:
                max_value = action_value
                logging.debug(f"New max_value set equals to {max_value}")
        
        logging.debug(f"Max value for player {player} at board {board.as_one_line_list()} is {max_value}")
        return max_value


    def min_value(board: Board, player: str) -> int:

        utility = TicTacToePlayer.calc_utility(board, player)

        # If board is terminated, return its utility for player
        if  utility != None:
            logging.debug(f"At board {board.as_one_line_list()} min_value for {player} is {utility}")
            return utility

        # if board is not terminated check subsequente actions

        opponent = 'X'
        if player == 'X':
            opponent = '0'

        actions = TicTacToePlayer.actions(board, opponent)
        min_value = 1000

        for action in actions:

            action_value = TicTacToePlayer.max_value(action.board, player)

            if action_value < min_value:
                min_value = action_value
                logging.debug(f"New min_value set equals to {min_value}")
        
        return min_value
    
    def minimax_decision(self, board: Board) -> Action:
        '''
        This method trigges the minimax algorithm in order to choose
        the best action on `board`
        
        ## Parameters
        `- board: Board` of current game state
        `- return: Action` that best fits for Player
        '''
        
        logging.debug(f"Starting minimax_decicion for palyer {self.symbol} at board {board.as_one_line_list()}")

        actions = TicTacToePlayer.actions(board, self.symbol)

        max_action = Action(board, ('-', '-'), -1000)

        for action in actions:

            action.utility = TicTacToePlayer.min_value(action.board, self.symbol)

            if action.utility > max_action.utility:
                max_action = action
        
        logging.debug(f"Best action for player {self.symbol} at board {board.as_one_line_list()} is {max_action}")
        return max_action
    
    def minimax_decision_faster(self, board: Board) -> Action:
        '''
        This method trigges the minimax algorithm in order to choose
        the best action on `board`
        
        ## Parameters
        `- board: Board` of current game state
        `- return: Action` that best fits for Player
        '''
        
        logging.debug(f"Starting minimax_decicion for palyer {self.symbol} at board {board.as_one_line_list()}")

        actions = TicTacToePlayer.actions(board, self.symbol)

        max_action = Action(board, ('-', '-'), -1000)

        for action in actions:

            action.utility = TicTacToePlayer.min_value(action.board, self.symbol)

            if action.utility == 1:
                return action

            if action.utility > max_action.utility:
                max_action = action
        
        logging.debug(f"Best action for player {self.symbol} at board {board.as_one_line_list()} is {max_action}")
        return max_action
