import copy
import setlog
import logging
from tictactoeboard import TicTacToeBoard as Board
from tictactoeaction import TicTacToeAction as Action

setlog.set_log(logging.DEBUG)


class TicTacToePlayer:

    def __init__(self, symbol: str):
        self.__symbol = symbol

    @property
    def symbol(self) -> str:
        return self.__symbol
            
        
    def actions(self, board: Board) -> list:
        '''
        This method analyse all possible subsequence moves at `board` for `player`.
        
        ## Parameters
        `- board: Board` representing the current board state;
        `- player: str` symbol that represents the player. It must be 'X' or '0';
        `- return: list` of TicTacToeActions where each one of them is a possible subsequente
        state. Those actions have `board` and `move` property setted, but `cost` equals to `None`.        
        '''
        states = []
        for n_row, line in enumerate(board.board):
            for n_col, cell in enumerate(line):
                if cell == "-":
                    new_board = Board(board.as_one_line_list())
                    new_board.set_cel(n_row, n_col, self.symbol)
                    new_action = Action(new_board, (n_row, n_col), None)
                    states.append(new_action)
        
        return states
    
    def calc_utility(board: Board, player: str) -> int:
        '''
        Calculate the cost of `board` for `player`.
        
        ## Parameters
        `- board: Board` board wich cost is been analised;
        `- player: str` having `X` or `0` to identifying which player
        the cost is been calculated;
        `- return: int` -1, if player looses, 0 if even and +1 if wins.
        If `board` is not terminated, returns None'''

        final_result = TicTacToePlayer.current_result(board)

        if final_result[0] == None:
            return None
        
        if final_result[0] == '-':
            return 0

        if final_result[0] == player:
            return 1
        
        return -1


    def max_value(board: Board, player: str) -> int:

        logging.debug(f"Calculating max_value of {board.as_one_line_list()} for player {player}")

        curr_result = TicTacToePlayer.current_result(board)
        logging.debug(f"Current result for {board.as_one_line_list()} is {curr_result}")

        # If board is terminated, return its cost for player
        if curr_result[0] != None:
            logging.debug("Board is terminated state")

            cost = TicTacToePlayer.calc_utility(board, player)
            logging.debug(f"Cost of board for {player} is {cost}")
            return cost

        # if board is not terminated check subsequente actions
        actions = TicTacToePlayer.actions(board, player)
        logging.debug(f"Retrieved {len(actions)} subsequent actions")

        max_value = -1000
        opponent = 'X'
        if player == 'X':
            opponent = '0'
        for action in actions:

            if TicTacToePlayer.terminated(action):
                action_cost = TicTacToePlayer.calc_utility(action, player)
            else:                
                action_cost = TicTacToePlayer.min_value(action, opponent)

            if action_cost > max_value:
                max_value = action_cost
                logging.debug(f"New max_value set equals to {max_value}")
        
        return max_value

    def min_value(board: Board, player: str):

        logging.debug(f"Calculating min_value of {board.as_one_line_list()} for player {player}")

        curr_result = TicTacToePlayer.current_result(board)
        logging.debug(f"Current result for {board.as_one_line_list()} is {curr_result}")

        # If board is terminated, return its cost for player
        if curr_result[0] != None:
            logging.debug("Board is terminated state")

            cost = TicTacToePlayer.calc_utility(board, player)
            logging.debug(f"Cost of board for {player} is {cost}")
            return cost

        # if board is not terminated check subsequente actions
        actions = TicTacToePlayer.actions(board, player)
        logging.debug(f"Retrieved {len(actions)} subsequent actions")

        min_value = 1000
        opponent = 'X'
        if player == 'X':
            opponent = '0'
        for action in actions:

            if TicTacToePlayer.terminated(action):
                action_cost = TicTacToePlayer.calc_utility(action, player)
            else:                
                action_cost = TicTacToePlayer.max_value(action, opponent)

            if action_cost < min_value:
                min_value = action_cost
                logging.debug(f"New min_value set as {min_value}")
        
        return min_value


    def max_value(board: Board, player: str) -> Action:
        '''
        This method returns the next move '''

        logging.debug(f"Calculating max_value of {board.as_one_line_list()} for player {player}")

        curr_result = TicTacToePlayer.current_result(board)
        logging.debug(f"Current result for {board.as_one_line_list()} is {curr_result}")

        # If board is terminated, return its cost for player
        if curr_result[0] != None:
            logging.debug("Board is terminated state")

            cost = TicTacToePlayer.calc_utility(board, player)
            logging.debug(f"Cost of board for {player} is {cost}")
            return Action(board, cost)

        max_action = Action(None, -1000)
        opponent = 'X'
        if player == 'X':
            opponent = '0'

        # if board is not terminated check subsequente actions
        possible_moves = TicTacToePlayer.actions(board, player)
        logging.debug(f"Retrieved {len(possible_moves)} possible moves")
        for move in possible_moves:

            if TicTacToePlayer.terminated(move):
                action_cost = TicTacToePlayer.calc_utility(move, player)
            else:                
                action_cost = TicTacToePlayer.min_value(move, opponent)

            if action_cost > max_action.cost:
                max_action.cost = action_cost
                max_action.board = move
                logging.debug(f"New action set as max: {max_action}")
        
        return  max_action


    def min_value(board: Board, player: str) -> Action:

        logging.debug(f"Calculating min_value of {board.as_one_line_list()} for player {player}")

        curr_result = TicTacToePlayer.current_result(board)
        logging.debug(f"Current result for {board.as_one_line_list()} is {curr_result}")

        # If board is terminated, return its cost for player
        if curr_result[0] != None:
            logging.debug("Board is terminated state")

            cost = TicTacToePlayer.calc_utility(board, player)
            logging.debug(f"Cost of board for {player} is {cost}")
            return Action(board, cost)

        max_action = Action(None, (None, None), -1000)
        opponent = 'X'
        if player == 'X':
            opponent = '0'

        # if board is not terminated check subsequente actions
        possible_moves = TicTacToePlayer.actions(board, player)
        logging.debug(f"Retrieved {len(possible_moves)} possible moves")
        for move in possible_moves:

            if TicTacToePlayer.current_result(move)[0] != None:
                move_cost = TicTacToePlayer.calc_utility(move, player)
            else:                
                move_cost = TicTacToePlayer.min_value(move, opponent)

            if move_cost > max_action.cost:
                max_action = Action(move, cost)
                logging.debug(f"New action set as max: {max_action}")
        
        return  max_action