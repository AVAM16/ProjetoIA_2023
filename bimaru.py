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
    def __init__(self, rown:tuple, coln:tuple):
        self.rowtip = np.asarray(rown)
        self.coltip = np.asarray(coln)
        self.table = np.full((10,10), "-")
        for i in range(10):
            if rown[i] == 0:
                self.table[i] = np.full((1,10), ".") 
        for i in range(10):
            if coln[i] == 0:
                self.table[:, i] = np.full((1,10), ".") 
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
        row = stdin.readline().split().pop(0)
        row = [int(x) for x in row]
        column = stdin.readline().split().pop(0)
        column = [int(x) for x in column]
        b = Board(tuple(row), tuple(column))
        n = int(stdin.readline().strip())
        x = 0
        while x < n:
            hint = stdin.readline().split().pop(0)
            hint = [int(x) for x in hint]
            b.get_hint(tuple(hint))
            x += 1
        return b

    # TODO: outros metodos da classe
    """"W (water), C (circle), T (top), M (middle), B (bottom), L (left) e R (right)"""
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
            if counter == self.rowtip[row]:
                fill_row(self,row)
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
            if counter == self.coltip[column]:
                fill_column(self,column)
                changed = 1
            if counter < self.coltip[column]:
                return -1
            column+=1
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
    

    def fill_corners_and_adj(self,row , column,shape):
        if row == 9:
            if column == 9:
                self.table[row+1][column+1] = "."
            if column == 0:
                self.table[row+1][column-1] = "."
        if row == 0:
            if column == 9:
                self.table[row-1][column+1] = "."
            if column == 0:
                self.table[row-1][column-1] = "."
        if shape != "B" or shape != "M" or row == 9:
            self.table[row+1][column] = "."
        if shape != "L" or shape != "M" or column == 9:
            self.table[row][column+1] = "."
        if shape != "R" or shape != "M" or column == 0:
            self.table[row][column-1] = "."
        if shape != "T" or shape != "M" or row == 0:
            self.table[row-1][column] = "."

    def get_hint(self, hint:tuple):
        row = hint[0]
        column = hint[1]
        shape = hint[2]
        self.table[row][column] = shape
        if shape != "W":
            self.rowtip[row] -= 1
            self.coltip[column] -= 1
            
        if shape == "C":
            self.fleet[3] -= 1
        



class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        self.table.[row]
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
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
