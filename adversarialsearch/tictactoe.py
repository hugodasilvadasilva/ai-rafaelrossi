import copy
import setlog
import logging

setlog.set_log(logging.DEBUG)

class TicTacToeBoard:

    def __init__(self, marks: list):
        self.__board = [marks[i*3 : i*3+3] for i in range(0,3)]

    def __repr__(self) -> str:
        '''
        This method returns the Board as string with 3 lines and 3 columns.
        It will have the form of:
        X|X|X
        X|X|X
        X|X|X
        '''

        # Insert a | between each position and a \n at the end of each line
        string_board = "\n".join(["|".join(line) for line in self.__board])
        return string_board

    def __eq__(self, __o: object) -> bool:
        return self.__board == __o.board 
    
    def as_one_line_list(self) -> list:
        '''
        Return all marks of board as one line list. For instance, if
        board is:
        X|0|-
        X|0|-
        X|0|-
        Then this method must return ['X','0','-','X','0','-','X','0','-']

        ## Parameters
        `- return: list` with one dimension listing all marks
        '''

        one_line = []
        [one_line.extend(line) for line in self.__board]

        return one_line
    
    def get_row(self, n: int) -> list:
        return self.__board[n]
    
    def get_column(self, n:int) -> list:
        col = [self.__board[i][n] for i in range(3)]
        return col

    def get_up_down_diagonnal(self) -> list:
        diag = []
        for i in range(3):
            diag.append(self.board[i][i])        
        return diag
    
    def get_down_up_diagonnal(self) -> list:
        diag = []
        for i in range(2,-1, -1):
            diag.append(self.board[i][2-i])       
        return diag
    
    def get_cel(self, row: int, col: int) -> str:
        return self.__board[row][col]
    
    def set_cel(self, row: int, col:int, value: str):
        self.__board[row][col] = value

    @property
    def board(self) -> list:
        return self.__board


class TicTacToePlayer:

    def __init__(self, symbol: str):
        self.__symbol = symbol

    @property
    def symbol(self) -> str:
        return self.__symbol

    def new_blank_board():
        tttboard = TicTacToeBoard(['-','-','-','-','-','-','-','-','-'])
        return tttboard()

    def current_result(board: TicTacToeBoard) -> tuple:
        '''
        Checks the final result of `board` end return the winner, and the
        position that winns.

        ## Parameters
        `- board: TicTacToeBoard` which final result is been analysed.
        `- return: tuple` having the winner and the position of winning.
        
        ### Possible results for return's 0 index
        - 'X': if 'X' wins;
        - '0': if '0' wins;
        - '-': if even;
        - None: if not terminated.

        ### Possible results for return's 1 index 
        - `coln`: if winner crosses column `n` where `n` is the column index
        that goes from 0 to 2; 
        - `rown`: if winner crosses row `n` where `n` is the row index that
        goes from 0 to 2;
        - `updown`: if winner crosses the up-down-diagonal;
        - `downup`: if winner corsses the down-up-diagonal;
        - `-`: if even;
        - None: if not terminated.

        ### Return examples
        - ('X', 'col2'): if 'X' wins by crossing column 2;
        - ('0', 'updown'): if '0' wins by crossing up-down-diagonal;
        - ('-', '-'): if result is even;
        - (None, None): if not terminated
        '''

        # Check if one row or one column is all X or 0
        for i in range(3):

            row = board.get_row(i)
            if row.count('X') == 3:
                return ('X', 'row' + str(i))

            if row.count('0') == 3:
                return ('0', 'row' + str(i))

            column = board.get_column(i)
            if column.count('X') == 3:
                return ('X', 'col' + str(i))
            
            if column.count('0') == 3:
                return ('0', 'col' + str(i))
        
        # Check if diagonals are all X or 0
        diag_up_down = board.get_up_down_diagonnal()
        if diag_up_down.count('X') == 3:
            return ('X', 'updown')

        if diag_up_down.count('0') == 3:
            return ('0', 'updown')

        diag_down_up = board.get_down_up_diagonnal()
        if diag_down_up.count('X') == 3:
            return ('X', 'downup')
        
        if diag_down_up.count('0') == 3:
            return ('0', 'downup')

        # Check if all board is full by searching '-' at each line
        for i in range(3):
            if board.get_row(i).count('-') > 0:
                return (None, None)
        
        return ('-', '-')


    def terminated(board: TicTacToeBoard) -> bool:
        '''
        Check if board is at a terminated state. A terminated state can be find at one
        of the following conditions:
        - one row having all cells with X or 0
        - one column having all cells with X or 0
        - one diagonal having all cells with X or 0
        - all board is marked.
        '''

        final_result = TicTacToePlayer.current_result(board)
        if final_result[0] == None:
            return False
        
        return True
            
        
    def subsequente_actions(board: TicTacToeBoard, player: str) -> list:
        '''
        This method analyse all possible subsequence moves at `board` for `markdown_player`.
        
        ## Parameters
        `- board: TicTacToeBoard` representing the current board state;
        `- player: str` symbol that represents the player. It must be 'X' or '0';
        `- return: list` of TicTacToeBoards where each one of them is a possible subsequente
        action.
        '''
        actions = []
        for n_line, line in enumerate(board.board):
            for n_col, cell in enumerate(line):
                if cell == "-":
                    new_board = TicTacToeBoard(board.as_one_line_list())
                    new_board.set_cel(n_line, n_col, player)
                    actions.append(new_board)
        
        return actions
    
    def cost(board: TicTacToeBoard, player: str) -> int:
        '''
        Calculate the cost of `board` for `player`.
        
        ## Parameters
        `- board: TicTacToeBoard` board wich cost is been analised;
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


    def max_value(board: TicTacToeBoard, player: str) -> int:

        logging.debug(f"Calculating max_value of {board.as_one_line_list()} for player {player}")

        curr_result = TicTacToePlayer.current_result(board)
        logging.debug(f"Current result for {board.as_one_line_list()} is {curr_result}")

        # If board is terminated, return its cost for player
        if curr_result[0] != None:
            logging.debug("Board is terminated state")

            cost = TicTacToePlayer.cost(board, player)
            logging.debug(f"Cost of board for {player} is {cost}")
            return cost

        # if board is not terminated check subsequente actions
        actions = TicTacToePlayer.subsequente_actions(board, player)
        logging.debug(f"Retrieved {len(actions)} subsequent actions")

        max_value = -1000
        opponent = 'X'
        if player == 'X':
            opponent = '0'
        for action in actions:

            if TicTacToePlayer.terminated(action):
                action_cost = TicTacToePlayer.cost(action, player)
            else:                
                action_cost = TicTacToePlayer.min_value(action, opponent)

            if action_cost > max_value:
                max_value = action_cost
                logging.debug(f"New max_value set equals to {max_value}")
        
        return max_value

    def min_value(board: TicTacToeBoard, player: str):

        logging.debug(f"Calculating min_value of {board.as_one_line_list()} for player {player}")

        curr_result = TicTacToePlayer.current_result(board)
        logging.debug(f"Current result for {board.as_one_line_list()} is {curr_result}")

        # If board is terminated, return its cost for player
        if curr_result[0] != None:
            logging.debug("Board is terminated state")

            cost = TicTacToePlayer.cost(board, player)
            logging.debug(f"Cost of board for {player} is {cost}")
            return cost

        # if board is not terminated check subsequente actions
        actions = TicTacToePlayer.subsequente_actions(board, player)
        logging.debug(f"Retrieved {len(actions)} subsequent actions")

        min_value = 1000
        opponent = 'X'
        if player == 'X':
            opponent = '0'
        for action in actions:

            if TicTacToePlayer.terminated(action):
                action_cost = TicTacToePlayer.cost(action, player)
            else:                
                action_cost = TicTacToePlayer.max_value(action, opponent)

            if action_cost < min_value:
                min_value = action_cost
                logging.debug(f"New min_value set as {min_value}")
        
        return min_value
        
    def minimax_decision(board: TicTacToeBoard) -> tuple:
        pass

if __name__ == "__main__":
    l = [1,2,3,4,5,6,7,8,9]
    s = [l[i:i+3] for i in range(0,3)]
    print(s)

    line = ['1','2','3']
    string_board = "|".join(line) + "\n"
    print(string_board)