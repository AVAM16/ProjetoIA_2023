# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 29:
# 102503 Artur Martins
# 102938 Francisco Caetano Fortunato

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

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

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
        x = 0
        while x < n:
            hint = stdin.readline().split()
            hint.pop(0)
            shape = hint.pop(2)
            hint = [int(x) for x in hint]
            b.get_hint((hint[0],hint[1],shape))
            x += 1
        return b

    # TODO: outros metodos da classe
    """"W (water), C (circle), T (top), M (middle), B (bottom), L (left) e R (right)"""


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
            if row != 1:
                self.table[row-1][column] = "."
            if row != 8:
                self.table[row+1][column] = "."
        if shape == "m" and (column == 0 or self.table[row][column-1] == "." or  column == 9 or self.table[row][column+1] == ".") and ((row != 0 and self.table[row-1][column] != ".") and (row != 9 and self.table[row+1][column] != ".")):
            if column != 1:
                self.table[row][column-1] = "."
            if column != 8:
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
                self.fill_corners(row+2,column)
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

                elif (column == 0 or self.table[row][column-1] == ".") and (column == 9 or self.table[row][column+1] == "."):
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

                elif (row == 0 or self.table[row-1][column] == ".") and (row == 9 or self.table[row+1][column] == "."):
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
    

    def check_finish(self):
        column = 0
        counter = 0
        while column<10:
            row = 0
            while row<10:
                if self.table[row][column] == "-":
                    counter +=1
                row+=1   
            column+=1
        if counter == 0:
            return 1
        return 0
    
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
        elif (row == 9 or self.table[row+1][column] == ".") and (row == 0 or self.table[row-1][column] == ".") and (column == 9 or self.table[row][column+1] == ".") and (column != 0 and self.table[row][column-1] != ".") and (column != 0 or self.table[row][column-1] != "-"):
            self.table[row][column] = "r"
        elif (row == 9 or self.table[row+1][column] == ".") and (row == 0 or self.table[row-1][column] == ".") and (column != 9 and self.table[row][column+1] != ".") and (column == 0 or self.table[row][column-1] == ".") and (column != 9 or self.table[row][column+1] != "-"):
            self.table[row][column] = "l"
        elif (row != 9 and self.table[row+1][column] != ".") and (row == 0 or self.table[row-1][column] == ".") and (column == 9 or self.table[row][column+1] == ".") and (column == 0 or self.table[row][column-1] == ".") and (row != 9 or self.table[row+1][column] != "-"):
            self.table[row][column] = "t"
        elif (row == 9 or self.table[row+1][column] == ".") and (row != 0 and self.table[row-1][column] != ".") and (column == 9 or self.table[row][column+1] == ".") and (column == 0 or self.table[row][column-1] == ".") and (row != 0 or self.table[row-1][column] != "-"):
            self.table[row][column] = "b"
        elif (row == 9 or self.table[row+1][column] == ".") and (row == 0 or self.table[row-1][column] == ".") and (column != 9 and self.table[row][column+1] != ".") and (column != 0 and self.table[row][column-1] != ".") and (column != 0 or self.table[row][column-1] != "-") and (column != 9 or self.table[row][column+1] != "-"):
            self.table[row][column] = "m"
        elif (row != 9 and self.table[row+1][column] != ".") and (row != 0 and self.table[row-1][column] != ".") and (column == 9 or self.table[row][column+1] == ".") and (column == 0 or self.table[row][column-1] == ".") and (row != 0 or self.table[row-1][column] != "-") and (row != 9 or self.table[row+1][column] != "-"):
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
        while repeat != 0:
            repeat = 0
            changed = self.check_zeros()
            if changed == -1:
                return changed
            
            if changed == 1:
                repeat = 1
            """self.check_pieces() """
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
            """ self.check_pieces() """
        return 0

    
    def check_tips(self):
        row = 0
        column = 0
        while row < 10:
            print(self.rowtip[row])
            row += 1
        while column < 10:
            print(self.coltip[column])
            column += 1
    
    
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
            self.complete(row,column,shape)
        else:
            self.table[row][column] = "."
        if shape == "c":
            self.fleet[3] -= 1


    def output_board(self):
        for row in range (10):
            for column in range (10):
                print(self.table[row][column],end='')
            print()



class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    b = Board.parse_instance()
    b.fill_board()
    b.check_pieces()
    b.fill_board()
    b.fix_all_ships()
    b.output_board()
    b.check_tips()
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
