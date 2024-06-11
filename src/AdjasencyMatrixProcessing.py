import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import io
import random

class AdjasencyMatrixProcessing:
    def __init__(self, size: int) -> None:
        self.size = size
        self.matrix = np.zeros((size, size))

    def create_matrix(self, size: int) -> None:
        self.size = size
        self.matrix = np.zeros((size, size))

    def create_graph(self) -> io.BytesIO:
        graph = nx.Graph()
        for i in range(self.size):
            for j in range(self.size):
                weight = float(self.matrix[i][j])
                if weight != 0:
                    graph.add_edge(i, j)

        pos = nx.spring_layout(graph, pos=None, seed=42)  # positions for all nodes

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(6, 6))

        # Draw the graph
        nx.draw(graph, pos=pos, with_labels=True, ax=ax)

        # Save the figure as a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format="PNG")
        buf.seek(0)
        return buf

    def create_structure(self) -> None:
        for i in range(self.size):
            for j in range(self.size):
                if i == j:
                    self.matrix[i, j] = 0
                else:
                    self.matrix[i, j] = random.randint(0, 1)

    def flip(self) -> None:
        # Переворот
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[j, i] == 1:
                    self.matrix[i, j] = 1

        for i in range(self.size):
            for j in range(self.size):
                if j <= i:
                    self.matrix[i, j] = 0
    
    def traverse(self, size:int, i:int, j:int, arr: np.ndarray) -> None:
        for k in range(j, size):
            if self.matrix[j, k] == 1:
                self.matrix[i, k] = 0
                for l in range(len(arr)):
                    self.matrix[arr[l], k] = 0
                arr.append(j)
                self.traverse(size, i, k, arr)
                arr.pop()

    def reset(self) -> None:
        for i in range(self.size):
            for j in range(self.size):
                arr = []
                if self.matrix[i, j] == 1:
                    self.traverse(self.size, i, j, arr)

    def create_point(self) -> None:
        starters = []
        enders = []
        n = 0

        existing_data = self.matrix.copy()

        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[j, i] == 1:
                    break
                if j == self.size-1:
                    starters.append(i)

        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i, j] == 1:
                    break
                if j == self.size-1:
                    enders.append(i)


        if len(starters) >=2:
            new_matrix_str = np.zeros((self.size + 1, self.size + 1))

            # Заполнение матрицы данными
            for i in range(self.size):
                new_matrix_str[i, 0] = 0
                new_matrix_str[0, i] = 0
                for j in range(len(starters)):
                    if i == starters[j] + 1:
                        new_matrix_str[0, i] = 1

                for j in range(self.size):
                    new_matrix_str[i + 1, j + 1] = float(existing_data[i][j]) if existing_data[i][j] else 0.0

            self.matrix = new_matrix_str
            n = n + 1

        if len(enders) >=2:
            for v in range(len(enders)):
                print(enders[v])

            new_matrix_end = np.zeros((self.size + 1 + n, self.size + 1 + n))


            # Заполнение матрицы данными
            for i in range(self.size + n):
                print(self.size + n)
                new_matrix_end[i, self.size + n] = 0
                new_matrix_end[self.size + n, i] = 0
                for j in range(len(enders)):
                    if i == enders[j] + n:
                        new_matrix_end[i, self.size + n] = 1

                for j in range(self.size + n):
                    new_matrix_end[i, j] = float(existing_data[i][j]) if existing_data[i][j] else 0.0

            self.matrix = new_matrix_end

    def add_element(self) -> None:
        units = []
        intersections = []
        equals = []
        columns = []
        coordinates = []
        n = 0

        existing_data = self.matrix.copy()

        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[j, i] == 1:
                    units.append(j)
            intersections.append(units)
            units = []

        # print(intersections)
        # # print(intersections[1][0])
        # print(len(intersections))
        # print(len(intersections[2]))

        # print(intersections[1].intersection(intersections[2]))


        for i in range(len(intersections)):
            set1 = set(intersections[i])
            for j in range(1, len(intersections) - i):
                set2 = set(intersections[i + j])
                if len(set1.intersection(set2)) >= 2:
                    columns.append(i)
                    columns.append(i+j)
                    coordinates.append(columns)
                    coordinates.append(list(set1.intersection(set2)))
                    equals.append(coordinates)
                    columns = []
                    coordinates = []

        print(equals)
        # print(equals[0])
        # print(equals[0][0])

        if len(equals) >= 1:
            for z in range(len(equals)):

                new_matrix_add = np.zeros((self.size + 1, self.size + 1))

                for i in range(self.size):
                    if i < equals[z][1][-1] + 1 + n:
                        for j in range(self.size):
                            if j < equals[z][1][-1] + 1 + n:
                                new_matrix_add[i, j] = float(existing_data[i][j]) if existing_data[i][j] else 0
                            if j >= equals[z][1][-1] + 1 + n:
                                new_matrix_add[i, j + 1] = float(existing_data[i][j]) if existing_data[i][j] else 0

                    if i >= equals[z][1][-1] + 1 + n:
                        for j in range(self.size):
                            if j < equals[z][1][-1] + 1 + n:
                                new_matrix_add[i + 1, j] = float(existing_data[i][j]) if existing_data[i][j] else 0
                            if j >= equals[z][1][-1] + 1 + n:
                                new_matrix_add[i + 1, j + 1] = float(existing_data[i][j]) if existing_data[i][j] else 0

                for i in range(len(equals[z][0])):
                    for j in range(len(equals[z][1])):
                        new_matrix_add[equals[z][1][j] + n, equals[z][0][i] + 1 + n] = 0
                        new_matrix_add[equals[z][1][j] + n, equals[z][1][-1] + 1 + n] = 1
                    new_matrix_add[equals[z][1][-1] + 1 + n, equals[z][0][i] + 1 + n] = 1

                self.matrix = new_matrix_add

                self.size = self.size + 1
                n = n + 1





