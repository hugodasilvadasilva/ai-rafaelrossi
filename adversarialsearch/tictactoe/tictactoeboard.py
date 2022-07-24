import copy
import logging

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

    def current_result(self) -> tuple:
        '''
        Checks the final result of `board` end return the winner, and the
        position that winns.

        ## Parameters
        `- board: Board` which final result is been analysed.
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

            row = self.get_row(i)
            if row.count('X') == 3:
                logging.debug(f"At board {self.as_one_line_list()} game is over and X wins by crossing row {str(i)}")
                return ('X', 'row' + str(i))

            if row.count('0') == 3:
                logging.debug(f"At board {self.as_one_line_list()} game is over and 0 wins by crossing row {str(i)}")
                return ('0', 'row' + str(i))

            column = self.get_column(i)
            if column.count('X') == 3:
                logging.debug(f"At board {self.as_one_line_list()} game is over and X wins by crossing col {str(i)}")
                return ('X', 'col' + str(i))
            
            if column.count('0') == 3:
                logging.debug(f"At board {self.as_one_line_list()} game is over and 0 wins by crossing col {str(i)}")
                return ('0', 'col' + str(i))
        
        # Check if diagonals are all X or 0
        diag_up_down = self.get_up_down_diagonnal()
        if diag_up_down.count('X') == 3:
            logging.debug(f"At board {self.as_one_line_list()} game is over and X wins by up-down-diagonal")
            return ('X', 'updown')

        if diag_up_down.count('0') == 3:
            logging.debug(f"At board {self.as_one_line_list()} game is over and 0 wins by up-down-diagonal")
            return ('0', 'updown')

        diag_down_up = self.get_down_up_diagonnal()
        if diag_down_up.count('X') == 3:
            logging.debug(f"At board {self.as_one_line_list()} game is over and X wins by down-up-diagonal")
            return ('X', 'downup')
        
        if diag_down_up.count('0') == 3:
            logging.debug(f"At board {self.as_one_line_list()} game is over and 0 wins by up-down-diagonal")
            return ('0', 'downup')

        # Check if all board is full by searching '-' at each line
        for i in range(3):
            if self.get_row(i).count('-') > 0:
                logging.debug(f"At board {self.as_one_line_list()} game is not over")
                return (None, None)

        logging.debug(f"At board {self.as_one_line_list()} game is over by even")
        return ('-', '-')

    def terminated(self):

        curr_state = self.current_result()
        if curr_state[0] == None:
            return False

        return True

    @property
    def board(self) -> list:
        return self.__board

class TicTacToeBoardFabric():

    def blank_board() -> TicTacToeBoard:        
        return TicTacToeBoard(['-','-','-','-','-','-','-','-','-'])

if __name__ == "__main__":
    l = [1,2,3,4,5,6,7,8,9]
    s = [l[i:i+3] for i in range(0,3)]
    print(s)

    line = ['1','2','3']
    string_board = "|".join(line) + "\n"
    print(string_board)