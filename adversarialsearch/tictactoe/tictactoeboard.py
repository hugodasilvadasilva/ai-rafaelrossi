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

    @property
    def board(self) -> list:
        return self.__board

if __name__ == "__main__":
    l = [1,2,3,4,5,6,7,8,9]
    s = [l[i:i+3] for i in range(0,3)]
    print(s)

    line = ['1','2','3']
    string_board = "|".join(line) + "\n"
    print(string_board)