import logging
from tictactoeboard import TicTacToeBoard as Board

class TicTacToeGame:

    def __init(self):

        pass
    

    def current_result(board: Board) -> tuple:
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

            row = board.get_row(i)
            if row.count('X') == 3:
                logging.debug(f"At board {board.as_one_line_list()} game is over and X wins by crossing row {str(i)}")
                return ('X', 'row' + str(i))

            if row.count('0') == 3:
                logging.debug(f"At board {board.as_one_line_list()} game is over and 0 wins by crossing row {str(i)}")
                return ('0', 'row' + str(i))

            column = board.get_column(i)
            if column.count('X') == 3:
                logging.debug(f"At board {board.as_one_line_list()} game is over and X wins by crossing col {str(i)}")
                return ('X', 'col' + str(i))
            
            if column.count('0') == 3:
                logging.debug(f"At board {board.as_one_line_list()} game is over and 0 wins by crossing col {str(i)}")
                return ('0', 'col' + str(i))
        
        # Check if diagonals are all X or 0
        diag_up_down = board.get_up_down_diagonnal()
        if diag_up_down.count('X') == 3:
            logging.debug(f"At board {board.as_one_line_list()} game is over and X wins by up-down-diagonal")
            return ('X', 'updown')

        if diag_up_down.count('0') == 3:
            logging.debug(f"At board {board.as_one_line_list()} game is over and 0 wins by up-down-diagonal")
            return ('0', 'updown')

        diag_down_up = board.get_down_up_diagonnal()
        if diag_down_up.count('X') == 3:
            logging.debug(f"At board {board.as_one_line_list()} game is over and X wins by down-up-diagonal")
            return ('X', 'downup')
        
        if diag_down_up.count('0') == 3:
            logging.debug(f"At board {board.as_one_line_list()} game is over and 0 wins by up-down-diagonal")
            return ('0', 'downup')

        # Check if all board is full by searching '-' at each line
        for i in range(3):
            if board.get_row(i).count('-') > 0:
                logging.debug(f"At board {board.as_one_line_list()} game is not over")
                return (None, None)

        logging.debug(f"At board {board.as_one_line_list()} game is over by even")
        return ('-', '-')

    def terminated(board: Board):

        curr_state = TicTacToeGame.current_result(board)
        if curr_state[0] == None:
            return False

        return True

    def new_blank_board():
        tttboard = Board(['-','-','-','-','-','-','-','-','-'])
        return tttboard()