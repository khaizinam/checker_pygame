from config import *
from Board import *
class Tranfer:
    def __init__(self):
        pass
    def ob_arr(self, matrix):
        arr = []
        for x in range(8):
            for y in range(8):
                if matrix[x][y].occupant is not None:
                    if matrix[x][y].occupant.color == BLUE:
                        if matrix[x][y].occupant.value == 2:
                            arr.append('2')
                        else:
                            arr.append('1')   
                    elif matrix[x][y].occupant.color == RED:
                        if matrix[x][y].occupant.value == 2:
                            arr.append('4')
                        else:
                            arr.append('3')
                else:
                   arr.append('0') 
        return arr
    
    def str_arr(self, str):
        return str.split()
    def arr_matrix(self, arr):
        matrix = [[None] * 8 for i in range(8)]
        # set up BlACK and WHITE
        for x in range(8):
            for y in range(8):
                if (x % 2 != 0) and (y % 2 == 0):
                    matrix[y][x] = Square(WHITE)
                elif (x % 2 != 0) and (y % 2 != 0):
                    matrix[y][x] = Square(BLACK)
                elif (x % 2 == 0) and (y % 2 != 0):
                    matrix[y][x] = Square(WHITE)
                elif (x % 2 == 0) and (y % 2 == 0):
                    matrix[y][x] = Square(BLACK)
                    
        
		# initialize the pieces and put them in the appropriate squares
        x = 0
        y = 0
        for elem in arr:
            # init
            if elem == '1' or elem == '2':
                matrix[x][y].occupant = Piece(BLUE)
                if elem == '2':
                    matrix[x][y].occupant.crown()
            elif elem == '3' or elem == '4':
                matrix[x][y].occupant = Piece(RED)
                if elem == '4':
                    matrix[x][y].occupant.crown()
            # print(x,y,type(elem))
            y += 1
            if y == 8:
                y = 0
                x +=1
        return matrix
    
    # encode matrix to str to send server
    def matrix_str(self, matrix):
        arr = self.ob_arr(matrix)
        return ' '.join([elem for elem in arr])
    
    # decode string to matrix from server 
    def str_matrix(self, str):
        arr = self.str_arr(str)
        matrix = self.arr_matrix(arr)
        return matrix
            
class DataSend:
    def __init__(self, id , method, data):
        self.id = id
        # get, put, update
        self.method = method
        self.data = data
    def _str(self):
        return f'{self.id},{self.method},{self.data}'
# board = Board()
# makeBoard = Tranfer()
# str = makeBoard.matrix_str(board.matrix)
# matrix = makeBoard.str_matrix(str)
# str2 = makeBoard.matrix_str(matrix)
# print(str)
# print(str2)
# str_2 = makeBoard._str(matrix)
# print(str)
# print(matrix)
# print(str_2)

