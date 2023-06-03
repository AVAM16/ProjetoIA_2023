# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 29:
# 102503 Artur Martins
# 102938 Francisco Caetano Fortunato

import copy

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
import numpy as np

hints = []

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
    def get_board(self,board):
        self.board = board

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    def __init__(self):
        self.rowtip = np.empty(10)
        self.coltip = np.empty(10)
        self.table = np.full((10,10), "-")
        self.fleet = np.array([1,2,3,4])
        """1 de 4, 2 de 3, 3 de 2, 4 de 1"""

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.table[row][col]

    def adjacent_vertical_values(self, row: int, col: int):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        output = (self.table[row][col-1], self.table[row][col+1])
        return output

    def adjacent_horizontal_values(self, row: int, col: int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        output = (self.table[row-1][col], self.table[row+1][col])
        return output

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        # TODO
        from sys import stdin
        row = stdin.readline().split()
        row.pop(0)
        row = [int(x) for x in row]
        column = stdin.readline().split()
        column.pop(0)
        column = [int(x) for x in column]
        b = Board()
        b.rowtip = row
        b.coltip = column
        for i in range(10):
            if b.rowtip[i] == 0:
                b.table[i] = np.full((1,10), ".") 
        for i in range(10):
            if b.coltip[i] == 0:
                b.table[:, i] = np.full((1,10), ".") 
        n = int(stdin.readline())
        for _ in range(n):
            hint = stdin.readline().split()
            hint.pop(0)
            shape = hint.pop(2)
            hint = [int(x) for x in hint]
            b.get_hint((hint[0],hint[1],shape))
            hints.append((hint[0],hint[1],shape))
        row = 0
        column = 0
        while row < 10:
            while column < 10:
                if b.table[row][column] != "." and b.table[row][column] != "c":
                    b.complete(row,column,b.table[row][column])
                column += 1
            row += 1
        return b


    def fill_corners(self,row,column):
        if row != 9:
            if column != 9:
                self.table[row+1][column+1] = "."
            if column != 0:
                self.table[row+1][column-1] = "."
        if row != 0:
            if column != 9:
                self.table[row-1][column+1] = "."
            if column != 0:
                self.table[row-1][column-1] = "."

    def fill_adj(self,row,column,shape):
        if shape != "t" and shape != "m" and row != 9:
            self.table[row+1][column] = "."
        if shape != "l" and shape != "m" and column != 9:
            self.table[row][column+1] = "."
        if shape != "r" and shape != "m" and column != 0:
            self.table[row][column-1] = "."
        if shape != "b" and shape != "m" and row != 0:
            self.table[row-1][column] = "."
        if shape == "m" and (row == 0 or self.table[row-1][column] == "." or row == 9 or self.table[row+1][column] == ".") and ((column != 0 and self.table[row][column-1] != ".") and  (column != 9 and self.table[row][column+1] != ".")):
            if row != 0:
                self.table[row-1][column] = "."
            if row != 9:
                self.table[row+1][column] = "."
        if shape == "m" and (column == 0 or self.table[row][column-1] == "." or  column == 9 or self.table[row][column+1] == ".") and ((row != 0 and self.table[row-1][column] != ".") and (row != 9 and self.table[row+1][column] != ".")):
            if column != 0:
                self.table[row][column-1] = "."
            if column != 9:
                self.table[row][column+1] = "."


    def fill_corners_and_adj(self,row , column,shape):
        self.fill_corners(row,column)
        self.fill_adj(row,column,shape)


    def complete(self,row,column,shape):
        if shape == "l":
            if (column == 8 or self.table[row][column+2] == ".") and self.table[row][column+1] == "-":
                self.table[row][column+1] = "r"
                self.rowtip[row] -= 1
                self.coltip[column+1] -= 1
            elif self.table[row][column+1] == "-":
                self.table[row][column+1] = "S"
                self.rowtip[row] -= 1
                self.coltip[column+1] -= 1
                self.fill_corners(row,column+1)
        elif shape == "r":
            if (column == 1 or self.table[row][column-2] == ".") and self.table[row][column-1] == "-":
                self.table[row][column-1] = "l"
                self.rowtip[row] -= 1
                self.coltip[column-1] -= 1
            elif self.table[row][column-1] == "-":
                self.table[row][column-1] = "S"
                self.rowtip[row] -= 1
                self.coltip[column-1] -= 1
                self.fill_corners(row,column-1)
        elif shape == "t":
            if (row == 8 or self.table[row+2][column] == ".") and self.table[row+1][column] == "-":
                self.table[row+1][column] = "b"
                self.rowtip[row+1] -= 1
                self.coltip[column] -= 1
            elif self.table[row+1][column] == "-":
                self.table[row+1][column] = "S"
                self.rowtip[row+1] -= 1
                self.coltip[column] -= 1
                self.fill_corners(row+1,column)
        elif shape == "b":
            if (row == 1 or self.table[row-2][column] == ".") and self.table[row-1][column] == "-":
                self.table[row-1][column] = "t"
                self.rowtip[row-1] -= 1
                self.coltip[column] -= 1
            elif self.table[row-1][column] == "-":
                self.table[row-1][column] = "S"
                self.rowtip[row-1] -= 1
                self.coltip[column] -= 1
                self.fill_corners(row-1,column)

    def fill_row(self,row):
        column = 0
        counter = 0
        while column < 10:
            if self.table[row][column] != "." and self.table[row][column] != "t" and self.table[row][column] != "b" and self.table[row][column] != "c":
                if (column == 0 or self.table[row][column-1] == ".") and (column != 9 and self.table[row][column+1] != "."):
                    self.fill_corners_and_adj(row,column,"l")
                    if self.table[row][column] != "S" and self.table[row][column] != "l":
                        self.coltip[column] -= 1
                    self.table[row][column] = "l"
                    counter += 1

                elif  column != 0 and (self.table[row][column-1] != ".") and (column == 9 or self.table[row][column+1] == "."):
                    self.fill_corners_and_adj(row,column,"r")
                    if self.table[row][column] != "S" and self.table[row][column] != "r":
                        self.coltip[column] -= 1
                    self.table[row][column] = "r"
                    counter += 1
                    self.fleet[4-counter] -= 1
                    counter = 0

                elif (column == 0 or self.table[row][column-1] == ".") and (column == 9 or self.table[row][column+1] == ".") and (row == 0 or self.table[row-1][column] == ".") and (row == 9 or self.table[row+1][column] == "."):
                    self.fill_corners(row,column)
                    if self.table[row][column] != "S" and self.table[row][column] != "c":
                        self.coltip[column] -= 1
                    self.table[row][column] = "c"
                    self.fleet[3] -= 1

                elif (column == 0 or self.table[row][column-1] == ".") and (column == 9 or self.table[row][column+1] == ".") and self.table[row][column] != "m":
                    self.fill_corners(row,column)
                    if self.table[row][column] != "S":
                        self.coltip[column] -= 1
                    self.table[row][column] = "S"

                elif  column != 0 and self.table[row][column-1] != "." and column != 9 and self.table[row][column+1] != "." :
                    self.fill_corners(row,column)
                    if row != 0:
                        self.table[row-1][column] = "."
                    if row != 9:
                        self.table[row+1][column] = "."
                    if self.table[row][column] != "S" and self.table[row][column] != "m":
                        self.coltip[column] -= 1
                    self.table[row][column] = "m"
                    counter += 1
            column +=1
        self.rowtip[row] = 0

    def fill_column(self,column):
        row = 0
        counter = 0
        while row < 10:
            if self.table[row][column] != "." and self.table[row][column] != "l" and self.table[row][column] != "r" and self.table[row][column] != "c":
                if (row == 0 or self.table[row-1][column] == ".") and (row != 9 and self.table[row+1][column] != "."):
                    self.fill_corners_and_adj(row,column,"t")
                    if self.table[row][column] != "S" and self.table[row][column] != "t":
                        self.rowtip[row] -= 1
                    self.table[row][column] = "t"
                    counter += 1

                elif (row != 0 and self.table[row-1][column] != ".") and (row == 9 or self.table[row+1][column] == "."):
                    self.fill_corners_and_adj(row,column,"b")
                    if self.table[row][column] != "S" and self.table[row][column] != "b":
                        self.rowtip[row] -= 1
                    self.table[row][column] = "b"
                    counter += 1
                    self.fleet[4-counter] -= 1
                    counter = 0

                elif (column == 0 or self.table[row][column-1] == ".") and (column == 9 or self.table[row][column+1] == ".") and (row == 0 or self.table[row-1][column] == ".") and (row == 9 or self.table[row+1][column] == "."):
                    self.fill_corners(row,column)
                    if self.table[row][column] != "S" and self.table[row][column] != "c":
                        self.rowtip[row] -= 1
                    self.table[row][column] = "c"
                    self.fleet[3] -= 1

                elif (row == 0 or self.table[row-1][column] == ".") and (row == 9 or self.table[row+1][column] == ".") and self.table[row][column] != "m":
                    self.fill_corners(row,column)
                    if self.table[row][column] != "S":
                        self.rowtip[row] -= 1
                    self.table[row][column] = "S"

                elif (row != 0 and self.table[row-1][column] != ".") and (row != 9 and self.table[row+1][column] != "."):
                    self.fill_corners(row,column)
                    if column != 9:
                        self.table[row][column+1] = "."
                    if column != 0:
                        self.table[row][column-1] = "."
                    if self.table[row][column] != "S" and self.table[row][column] != "m":
                        self.rowtip[row] -= 1
                    self.table[row][column] = "m"
                    counter += 1
            row +=1
        self.coltip[column] = 0


    def check_rows(self):
        changed = 0
        row = 0
        while row<10:
            counter = 0
            column = 0
            while column<10:
                if self.table[row][column] == "-":
                    counter +=1
                column+=1
            if counter == self.rowtip[row] and counter != 0:
                self.fill_row(row)
                if counter != 0:
                    changed = 1
            if counter < self.rowtip[row]:
                return -1
            row+=1
        return changed

    def check_columns(self):
        column = 0
        changed = 0
        while column<10:
            counter = 0
            row = 0
            while row<10:
                if self.table[row][column] == "-":
                    counter +=1
                row+=1
            if counter == self.coltip[column] and counter != 0:
                self.fill_column(column)
                if counter != 0:
                    changed = 1
            if counter < self.coltip[column]:
                return 0
            column+=1
        return changed
    

    def check_zeros(self):
        column = 0
        row = 0
        changed = 0
        counter = 0
        while column<10:
            row = 0
            counter = 0
            while row<10:
                    if self.table[row][column] == "-":
                        counter+=1
                    row+=1
            if self.coltip[column] == 0 and counter != 0:
                row = 0
                while row<10:
                    if self.table[row][column] == "-":
                        self.table[row][column] = "."
                    row+=1
                changed = 1
            if self.coltip[column] < 0:
                return -1
            column+=1
        counter = 0
        column = 0
        row = 0
        while row<10:
            column = 0
            counter = 0
            while column<10:
                    if self.table[row][column] == "-":
                        counter+=1
                    column+=1
            if self.rowtip[row] == 0 and counter != 0:
                column = 0
                while column<10:
                    if self.table[row][column] == "-":
                        self.table[row][column] = "."
                    column+=1
                changed = 1
            if self.rowtip[row] < 0:
                return -1
            row+=1
        return changed
    
    
    def fill_middle(self,row,column):
        if (row == 0 or self.table[row-1][column] == "." or row == 9 or self.table[row+1][column] == ".") and ((column != 0 and self.table[row][column-1] != ".") and  (column != 9 and self.table[row][column+1] != ".")):
            if row != 0:
                self.table[row-1][column] = "."
            if row != 9:
                self.table[row+1][column] = "."
            if (column-1 == 0 or self.table[row][column-2] == ".") and self.table[row][column-1] == "-":
                self.table[row][column-1] = "l"
                self.rowtip[row] -= 1
                self.coltip[column-1] -= 1
            elif self.table[row][column-1] == "-":
                self.table[row][column-1] = "S"
                self.rowtip[row] -= 1
                self.coltip[column-1] -= 1
            if (column+1 == 9 or self.table[row][column+2] == ".") and self.table[row][column+1] == "-":
                self.table[row][column+1] = "r"
                self.rowtip[row] -= 1
                self.coltip[column+1] -= 1
            elif self.table[row][column+1] == "-":
                self.table[row][column+1] = "S"
                self.rowtip[row] -= 1
                self.coltip[column+1] -= 1

        if (column == 0 or self.table[row][column-1] == "." or  column == 9 or self.table[row][column+1] == ".") and ((row != 0 and self.table[row-1][column] != ".") and (row != 9 and self.table[row+1][column] != ".")):
            if column != 0:
                self.table[row][column-1] = "."
            if column != 9:
                self.table[row][column+1] = "."
            if (row-1 == 0 or self.table[row-2][column] == ".") and self.table[row-1][column] == "-":
                self.table[row-1][column] = "t"
                self.rowtip[row-1] -= 1
                self.coltip[column] -= 1
            elif self.table[row-1][column] == "-":
                self.table[row-1][column] = "S"
                self.rowtip[row-1] -= 1
                self.coltip[column] -= 1
            if (row+1 == 9 or self.table[row+2][column] == ".") and self.table[row+1][column] == "-":
                self.table[row+1][column] = "b"
                self.rowtip[row+1] -= 1
                self.coltip[column] -= 1
            elif self.table[row+1][column] == "-":
                self.table[row+1][column] = "S"
                self.rowtip[row+1] -= 1
                self.coltip[column] -= 1
        return 0

  

    def fix_ship(self,row,column):
        if (row == 9 or self.table[row+1][column] == ".") and (row == 0 or self.table[row-1][column] == ".") and (column == 9 or self.table[row][column+1] == ".") and (column == 0 or self.table[row][column-1] == "."):
            self.table[row][column] = "c"
        elif (row == 9 or self.table[row+1][column] == ".") and (row == 0 or self.table[row-1][column] == ".") and (column == 9 or self.table[row][column+1] == ".") and (column != 0 and self.table[row][column-1] != ".") and (column != 0 and self.table[row][column-1] != "-"):
            self.table[row][column] = "r"
        elif (row == 9 or self.table[row+1][column] == ".") and (row == 0 or self.table[row-1][column] == ".") and (column != 9 and self.table[row][column+1] != ".") and (column == 0 or self.table[row][column-1] == ".") and (column != 9 and self.table[row][column+1] != "-"):
            self.table[row][column] = "l"
        elif (row != 9 and self.table[row+1][column] != ".") and (row == 0 or self.table[row-1][column] == ".") and (column == 9 or self.table[row][column+1] == ".") and (column == 0 or self.table[row][column-1] == ".") and (row != 9 and self.table[row+1][column] != "-"):
            self.table[row][column] = "t"
        elif (row == 9 or self.table[row+1][column] == ".") and (row != 0 and self.table[row-1][column] != ".") and (column == 9 or self.table[row][column+1] == ".") and (column == 0 or self.table[row][column-1] == ".") and (row != 0 and self.table[row-1][column] != "-"):
            self.table[row][column] = "b"
        elif (row == 9 or self.table[row+1][column] == ".") and (row == 0 or self.table[row-1][column] == ".") and (column != 9 and self.table[row][column+1] != ".") and (column != 0 and self.table[row][column-1] != ".") and (column != 0 and self.table[row][column-1] != "-") and (column != 9 and self.table[row][column+1] != "-"):
            self.table[row][column] = "m"
        elif (row != 9 and self.table[row+1][column] != ".") and (row != 0 and self.table[row-1][column] != ".") and (column == 9 or self.table[row][column+1] == ".") and (column == 0 or self.table[row][column-1] == ".") and (row != 0 and self.table[row-1][column] != "-") and (row != 9 and self.table[row+1][column] != "-"):
            self.table[row][column] = "m"
            
    def fix_all_ships(self):
        row=0
        while row < 10:
            column = 0
            while column < 10:
                if self.table[row][column] == "S":
                    self.fix_ship(row,column)
                column+=1
            row+=1

  
    def check_pieces(self):
        row = 0
        while row < 10:
            column = 0
            while column < 10:
                if self.table[row][column] == "m":
                    self.fill_middle(row,column)
                elif self.table[row][column] == "S":
                    self.fix_ship
                column += 1
            row += 1


    
    def fill_board(self):
        repeat = 1
        changed = 0
        counter = 0
        while repeat != 0:
            repeat = 0
            changed = self.check_zeros()
            if changed == -1:
                return changed
            if changed == 1:
                repeat = 1
            changed = self.check_rows()
            if changed == -1:
                return changed
            if changed == 1:
                repeat = 1
            changed = self.check_columns()
            if changed == -1:
                return changed
            if changed == 1:
                repeat = 1
            counter += 1
        if counter > 1:
            return 1
        return 0
    
    def fill_all(self):
        repeat = 0
        while repeat < 1:
            repeat += 1
            changed = self.fill_board()
            if changed == 1:
                repeat = 0
            self.check_pieces()
            self.fix_all_ships()
            row = 0
            column = 0
            while row < 10:
                column = 0
                while column < 10:
                    if self.table[row][column] != "." and self.table[row][column] != "c" and self.table[row][column] != "-":
                        self.complete(row,column,self.table[row][column])
                    column += 1
                row += 1
        return 0
    
    def place_boat(self, boat):

        if boat[3] == "o":
            self.fill_corners_and_adj(boat[0],boat[1],"c")
            if self.table[boat[0]][boat[1]] == "-":
                self.coltip[boat[1]] -= 1
                self.rowtip[boat[0]] -= 1
            self.table[boat[0]][boat[1]] = "c"
        elif boat [3] == "h":
            counter = 0
            while counter < boat[2]:
                if counter == 0:
                    self.fill_corners_and_adj(boat[0],boat[1]+counter,"l")
                    if self.table[boat[0]][boat[1]+counter] == "-":
                        self.coltip[boat[1]+counter] -= 1
                        self.rowtip[boat[0]] -= 1
                    self.table[boat[0]][boat[1]+counter] = "l"
                elif counter == boat[2] - 1:
                    self.fill_corners_and_adj(boat[0],boat[1]+counter,"r")
                    if self.table[boat[0]][boat[1]+counter] == "-":
                        self.coltip[boat[1]+counter] -= 1
                        self.rowtip[boat[0]] -= 1
                    self.table[boat[0]][boat[1]+counter] = "r"
                    
                else:
                    self.fill_corners_and_adj(boat[0],boat[1]+counter,"m")
                    if self.table[boat[0]][boat[1]+counter] == "-":
                        self.coltip[boat[1]+counter] -= 1
                        self.rowtip[boat[0]] -= 1
                    self.table[boat[0]][boat[1]+counter] = "m"
                counter+=1
        elif boat [3] == "v":
            counter = 0
            while counter < boat[2]:
                if counter == 0:
                    self.fill_corners_and_adj(boat[0]+counter,boat[1],"t")
                    if self.table[boat[0]+counter][boat[1]] == "-":
                        self.coltip[boat[1]] -= 1
                        self.rowtip[boat[0]+counter] -= 1
                    self.table[boat[0]+counter][boat[1]] = "t"
                elif counter == boat[2] - 1:
                    self.fill_corners_and_adj(boat[0]+counter,boat[1],"b")
                    if self.table[boat[0]+counter][boat[1]] == "-":
                        self.coltip[boat[1]] -= 1
                        self.rowtip[boat[0]+counter] -= 1
                    self.table[boat[0]+counter][boat[1]] = "b"
                else:
                    self.fill_corners_and_adj(boat[0]+counter,boat[1],"m")
                    if self.table[boat[0]+counter][boat[1]] == "-":
                        self.coltip[boat[1]] -= 1
                        self.rowtip[boat[0]+counter] -= 1
                    self.table[boat[0]+counter][boat[1]] = "m"
                    
                counter+=1

    
    def count_ships(self):
        self.fleet[0] = 1
        self.fleet[1] = 2
        self.fleet[2] = 3
        self.fleet[3] = 4
        row = 0
        while row < 10:
            column = 0
            while column < 10:
                counter = 0
                if self.table[row][column] == "c":
                    self.fleet[3] -= 1
                elif self.table[row][column] == "l":
                    repeat = 0
                    while repeat == 0:
                        if column + counter == 10:
                            return -1
                        elif self.table[row][column+counter] == "r":
                            repeat = 1
                            self.fleet[3-counter] -= 1
                        elif self.table[row][column+counter] == "m":
                            counter += 1
                        elif self.table[row][column+counter] == "l":
                            counter += 1
                        else:
                            repeat = 1
                elif self.table[row][column] == "t":
                    repeat = 0
                    while repeat == 0:
                        if row + counter == 10:
                            return -1
                        elif self.table[row+counter][column] == "b":
                            repeat = 1
                            self.fleet[3-counter] -= 1
                        elif self.table[row+counter][column] == "m":
                            counter += 1
                        elif self.table[row+counter][column] == "t":
                            counter += 1
                        else:
                            repeat = 1
                column += 1
            row += 1

    
    def check_tips(self):
        row = 0
        column = 0
        while row < 10:
            if self.rowtip[row] != 0:
                return -1
            row += 1
        while column < 10:
            if self.coltip[column] != 0:
                return -1
            column += 1

    def check_ships(self):
        counter = 0
        while counter < 4:
            if self.fleet[counter] != 0:
                return -1
            counter += 1
        return 0
    
    
    def get_hint(self, hint:tuple):
        row = hint[0]
        column = hint[1]
        shape = hint[2]
        shape = shape.lower()
        self.table[row][column] = shape
        if shape != "w":
            self.rowtip[row] -= 1
            self.coltip[column] -= 1
            self.fill_corners_and_adj(row,column,shape)
        else:
            self.table[row][column] = "."
        if shape == "c":
            self.fleet[3] -= 1


    def output_board(self):
        for row in range (10):
            for column in range (10):
                print(self.table[row][column],end='')
            print()
    
    def get_boats_four(self):
        boats = []
        for row in range (10):
            rowt = self.rowtip[row]
            for column in range (7):
                c = 0
                shape = self.table[row][column]
                if shape == '-': c += 1
                shape2 = self.table[row][column+1]
                if shape2 == '-': c += 1
                shape3 = self.table[row][column+2]
                if shape3 == '-': c += 1
                shape4 = self.table[row][column+3]
                if shape4 == '-': c += 1
                if c > rowt : continue
                if shape == 'l' and shape2 == 'm' and shape3 == 'm' and shape4 == 'r': continue
                tip = self.coltip[column]
                tip2 = self.coltip[column+1]
                tip3 = self.coltip[column+2]
                tip4 = self.coltip[column+3]
                if (shape == '-' and tip >= 1) or shape == 'l' or shape == 'S':
                    if ((shape2 == '-' and tip2 >= 1) or shape2 == 'S' or shape2 == 'm') and ((shape3 == '-' and tip3 >= 1) or shape3 == 'S' or shape3 == 'm') and ((shape4 == '-' and tip4 >= 1) or shape4 == 'S' or shape4 == 'r'):
                        boats.append((row, column, 4, 'h'))
                else:
                    continue
        for column in range (10):
            colt = self.coltip[column]
            for row in range (7):
                c = 0
                shape = self.table[row][column]
                if shape == '-': c += 1
                shape2 = self.table[row+1][column]
                if shape2 == '-': c += 1
                shape3 = self.table[row+2][column]
                if shape3 == '-': c += 1
                shape4 = self.table[row+3][column]
                if shape4 == '-': c += 1
                if c > colt: continue
                if shape == 't' and shape2 == 'm' and shape3 == 'm' and shape4 == 'b': continue
                tip = self.rowtip[row]
                tip2 = self.rowtip[row+1]
                tip3 = self.rowtip[row+2]
                tip4 = self.rowtip[row+3]
                if (shape == '-' and tip >= 1) or shape == 't' or shape == 'S':
                    if ((shape2 == '-' and tip2 >= 1) or shape2 == 'S' or shape2 == 'm') and ((shape3 == '-' and tip3 >= 1) or shape3 == 'S' or shape3 == 'm') and ((shape4 == '-' and tip4 >= 1) or shape4 == 'S' or shape4 == 'b'):
                        boats.append((row, column, 4, 'v'))
                else:
                    continue
        return boats


    def get_boats_three(self):
        boats = []
        for row in range (10):
            rowt = self.rowtip[row]
            for column in range (8):
                c = 0
                shape = self.table[row][column]
                if shape == '-': c += 1
                shape2 = self.table[row][column+1]
                if shape2 == '-': c += 1
                shape3 = self.table[row][column+2]
                if shape3 == '-': c += 1
                if c > rowt: continue
                if shape == 'l' and shape2 == 'm' and shape3 == 'r': continue
                tip = self.coltip[column]
                tip2 = self.coltip[column+1]
                tip3 = self.coltip[column+2]
                if (shape == '-' and tip >= 1) or shape == 'l' or shape == 'S':
                    if ((shape2 == '-' and tip2 >= 1) or shape2 == 'S' or shape2 == 'm') and ((shape3 == '-' and tip3 >= 1) or shape3 == 'S' or shape3 == 'r'):
                        boats.append((row, column, 3, 'h'))
                else:
                    continue
        for column in range (10):
            colt =  self.coltip[column]
            for row in range (8):
                c = 0
                shape = self.table[row][column]
                if shape == '-': c += 1
                shape2 = self.table[row+1][column]
                if shape2 == '-': c += 1
                shape3 = self.table[row+2][column]
                if shape3 == '-': c += 1
                if c > colt: continue
                if shape == 't' and shape2 == 'm' and shape3 == 'b': continue
                tip = self.rowtip[row]
                tip2 = self.rowtip[row+1]
                tip3 = self.rowtip[row+2]
                if (shape == '-' and tip >= 1) or shape == 't' or shape == 'S':
                    if ((shape2 == '-' and tip2 >= 1) or shape2 == 'S' or shape2 == 'm') and ((shape3 == '-' and tip3 >= 1) or shape3 == 'S' or shape3 == 'b'):
                        boats.append((row, column, 3, 'v'))
                else:
                    continue
        return boats


    def get_boats_two(self):
        boats = []
        for row in range (10):
            rowt = self.rowtip[row]
            for column in range (9):
                c = 0
                shape = self.table[row][column]
                if shape == '-': c += 1
                shape2 = self.table[row][column+1]
                if shape2 == '-': c += 1
                if c > rowt: continue
                if shape == 'l' and shape2 == 'r': continue
                tip = self.coltip[column]
                tip2 = self.coltip[column+1]
                if (shape == '-' and tip >= 1) or shape == 'l' or shape == 'S':
                    if ((shape2 == '-' and tip2 >= 1) or shape2 == 'S' or shape2 == 'r'):
                        boats.append((row, column, 2, 'h'))
                else:
                    continue
        for column in range (10):
            colt = self.coltip[column]
            for row in range (9):
                c = 0
                shape = self.table[row][column]
                if shape == '-': c += 1
                shape2 = self.table[row+1][column]
                if shape2 == '-': c += 1
                if c > colt: continue
                if shape == 't' and shape2 == 'b': continue
                tip = self.rowtip[row]
                tip2 = self.rowtip[row+1]
                if (shape == '-' and tip >= 1) or shape == 't' or shape == 'S':
                    if ((shape2 == '-' and tip2 >= 1) or shape2 == 'S' or shape2 == 'b'):
                        boats.append((row, column, 2, 'v'))
                else:
                    continue
        return boats
    

    
    def get_boats_one(self):
        boats = []
        for row in range(10):
            for column in range(10):
                shape = self.table[row][column]
                if self.rowtip[row] < 1 and self.coltip[column] < 1:
                    continue
                if (shape == '-' and self.rowtip[row] >= 1 and self.coltip[column] >= 1) or shape == 'S':
                    boats.append((row, column, 1, 'o'))
        return boats

    def get_boats(self):
        if self.fleet[0] > 0:
            return self.get_boats_four()
        elif self.fleet[1] > 0:
            return self.get_boats_three()
        elif self.fleet[2] > 0:
            return self.get_boats_two()
        else:
            return self.get_boats_one()


class Bimaru(Problem):
    def __init__(self, board: Board):
        self.board = board
        self.board.fill_all()
        self.board.count_ships()
        pass

    def actions(self, state: BimaruState):
        b = state.board.get_boats()
        return b

    def result(self, state: BimaruState, action):
        new_state = copy.deepcopy(state)
        new_state.board.fleet = copy.deepcopy(state.board.fleet)
        new_state.board.coltip = copy.deepcopy(state.board.coltip)
        new_state.board.table = copy.deepcopy(state.board.table)
        new_state.board.rowtip = copy.deepcopy(state.board.rowtip)
        new_state.board.place_boat(action)
        new_state.board.fill_all()
        new_state.board.count_ships()
        return new_state

    def goal_test(self, state: BimaruState):
        if state.board.check_tips() == -1:
            return False
        if state.board.check_ships() == -1:
            return False
        return True
        
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        count = 0
        for x in range(10):
            count += node.state.board.rowtip[x]
        for x in range(10):
            count += node.state.board.coltip[x]
        return count

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    b = Bimaru(board)
    initial_state=BimaruState(copy.copy(b.board))
    b.initial=initial_state
    solution = astar_search(b)
    if solution != None:
        solution.state.board.check_tips()
    for x in range(len(hints)):
        solution.state.board.table[hints[x][0]][hints[x][1]] = hints[x][2]
    solution.state.board.output_board()
    exit(0)