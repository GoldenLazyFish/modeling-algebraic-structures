import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel, QScrollArea, QHBoxLayout)
from PyQt5.QtGui import QPixmap
import io
import random

class MatrixApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Matrix App")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.left_layout = QVBoxLayout()
        self.layout.addLayout(self.left_layout)

        self.matrix_size_label = QLabel("Matrix Size:")
        self.left_layout.addWidget(self.matrix_size_label)

        self.matrix_size_input = QLineEdit()
        self.left_layout.addWidget(self.matrix_size_input)

        self.create_matrix_button = QPushButton("Create Matrix")
        self.create_matrix_button.clicked.connect(self.create_matrix)
        self.left_layout.addWidget(self.create_matrix_button)

        self.matrix_layout = QGridLayout()
        self.matrix_layout.minimumSize()
        self.left_layout.addLayout(self.matrix_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setMinimumSize(660, 480)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        self.matrix_layout = QGridLayout(self.scroll_widget)
        self.left_layout.addWidget(self.scroll_area)

        self.right_layout = QVBoxLayout()
        self.layout.addLayout(self.right_layout)

        self.create_graph_button = QPushButton("Create Graph")
        self.create_graph_button.clicked.connect(self.create_graph)
        self.right_layout.addWidget(self.create_graph_button)

        self.create_structure_button = QPushButton("Create Structure")
        self.create_structure_button.clicked.connect(self.create_structure)
        self.right_layout.addWidget(self.create_structure_button)

        self.flip_button = QPushButton("Flip")
        self.flip_button.clicked.connect(self.flip)
        self.right_layout.addWidget(self.flip_button)

        self.create_point_button = QPushButton("Create start and end")
        self.create_point_button.clicked.connect(self.create_point)
        self.right_layout.addWidget(self.create_point_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset)
        self.right_layout.addWidget(self.reset_button)

        self.add_element_button = QPushButton("Add Element")
        self.add_element_button.clicked.connect(self.add_element)
        self.right_layout.addWidget(self.add_element_button)

        self.graph_view = QLabel()
        self.right_layout.addWidget(self.graph_view)

        self.adjacency_matrix = None

    def create_matrix(self):
        try:
            size = int(self.matrix_size_input.text())
            self.adjacency_matrix = np.zeros((size, size))
            self.clear_matrix_layout()
            for i in range(size):
                for j in range(size):
                    entry = QLineEdit()
                    self.matrix_layout.addWidget(entry, i, j)

        except ValueError:
            print("Invalid input for matrix size")

    def clear_matrix_layout(self):
        for i in reversed(range(self.matrix_layout.count())):
            widget = self.matrix_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

    def create_graph(self):
        if self.adjacency_matrix is None:
            print("Matrix not created yet")
            return

        graph = nx.Graph()
        size = self.adjacency_matrix.shape[0]
        for i in range(size):
            for j in range(size):
                weight = float(self.matrix_layout.itemAtPosition(i, j).widget().text())
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

        # Display the graph in the QLabel
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        self.graph_view.setPixmap(pixmap)

    def create_structure(self):
        if self.adjacency_matrix is None:
            print("Matrix not created yet")
            return

        size = self.adjacency_matrix.shape[0]
        for i in range(size):
            for j in range(size):
                if i == j:
                    self.adjacency_matrix[i, j] = 0
                else:
                    self.adjacency_matrix[i, j] = random.randint(0, 1)

        self.clear_matrix_layout()
        for i in range(size):
            for j in range(size):
                entry = QLineEdit(str(int(self.adjacency_matrix[i, j])))
                self.matrix_layout.addWidget(entry, i, j)

    def get_matrix_values(self):
        size = self.adjacency_matrix.shape[0]
        matrix_values = []
        for i in range(size):
            row = []
            for j in range(size):
                widget = self.matrix_layout.itemAtPosition(i, j).widget()
                value = float(widget.text())
                row.append(value)
            matrix_values.append(row)
        return np.array(matrix_values)

    def flip(self):
        if self.adjacency_matrix is None:
            print("Matrix not created yet")
            return

        size = self.adjacency_matrix.shape[0]
        matrix_values = self.get_matrix_values()
        self.adjacency_matrix = matrix_values

        # Переворот
        for i in range(size):
            for j in range(size):
                if self.adjacency_matrix[j, i] == 1:
                    self.adjacency_matrix[i, j] = 1

        for i in range(size):
            for j in range(size):
                if j <= i:
                    self.adjacency_matrix[i, j] = 0

        self.clear_matrix_layout()
        for i in range(size):
            for j in range(size):
                entry = QLineEdit(str(int(self.adjacency_matrix[i, j])))
                self.matrix_layout.addWidget(entry, i, j)

    def reset(self):
        if self.adjacency_matrix is None:
            print("Matrix not created yet")
            return

        size = self.adjacency_matrix.shape[0]
        matrix_values = self.get_matrix_values()
        self.adjacency_matrix = matrix_values

        for i in range(size):
            for j in range(size):
                arr = []
                if self.adjacency_matrix[i, j] == 1:
                    traverse(size, self, i, j, arr)

        self.clear_matrix_layout()
        for i in range(size):
            for j in range(size):
                entry = QLineEdit(str(int(self.adjacency_matrix[i, j])))
                self.matrix_layout.addWidget(entry, i, j)

    def create_point(self):
        if self.adjacency_matrix is None:
            print("Matrix not created yet")
            return

        size = self.adjacency_matrix.shape[0]
        matrix_values = self.get_matrix_values()
        self.adjacency_matrix = matrix_values
        starters = []
        enders = []
        n = 0

        for i in range(size):
            for j in range(size):
                if self.adjacency_matrix[j, i] == 1:
                    break
                if j == size-1:
                    starters.append(i)

        for i in range(size):
            for j in range(size):
                if self.adjacency_matrix[i, j] == 1:
                    break
                if j == size-1:
                    enders.append(i)


        if len(starters) >=2:
            new_matrix_str = np.zeros((size + 1, size + 1))

            # Получаем существующие данные из элементов QLineEdit
            existing_data = []
            for i in range(size):
                row = []
                for j in range(size):
                    entry = self.matrix_layout.itemAtPosition(i, j).widget()
                    value = entry.text()
                    row.append(value)
                existing_data.append(row)

            # Заполнение матрицы данными
            for i in range(size):
                new_matrix_str[i, 0] = 0
                new_matrix_str[0, i] = 0
                for j in range(len(starters)):
                    if i == starters[j] + 1:
                        new_matrix_str[0, i] = 1

                for j in range(size):
                    new_matrix_str[i + 1, j + 1] = float(existing_data[i][j]) if existing_data[i][j] else 0.0

            self.adjacency_matrix = new_matrix_str
            self.clear_matrix_layout()

            for i in range(size + 1):
                for j in range(size + 1):
                    entry = QLineEdit(str(int(self.adjacency_matrix[i, j])))
                    self.matrix_layout.addWidget(entry, i, j)

            n = n + 1

        if len(enders) >=2:

            for v in range(len(enders)):
                print(enders[v])

            new_matrix_end = np.zeros((size + 1 + n, size + 1 + n))

            # Получаем существующие данные из элементов QLineEdit
            existing_data = []
            for i in range(size + n):
                row = []
                for j in range(size + n):
                    entry = self.matrix_layout.itemAtPosition(i, j).widget()
                    value = entry.text()
                    row.append(value)
                existing_data.append(row)

            # Заполнение матрицы данными
            for i in range(size + n):
                print(size + n)
                new_matrix_end[i, size + n] = 0
                new_matrix_end[size + n, i] = 0
                for j in range(len(enders)):
                    if i == enders[j] + n:
                        new_matrix_end[i, size + n] = 1

                for j in range(size + n):
                    new_matrix_end[i, j] = float(existing_data[i][j]) if existing_data[i][j] else 0.0

            self.adjacency_matrix = new_matrix_end
            self.clear_matrix_layout()

            for i in range(size + 1 + n):
                for j in range(size + 1 + n):
                    entry = QLineEdit(str(int(self.adjacency_matrix[i, j])))
                    self.matrix_layout.addWidget(entry, i, j)

    def add_element(self):
        if self.adjacency_matrix is None:
            print("Matrix not created yet")
            return

        size = self.adjacency_matrix.shape[0]
        matrix_values = self.get_matrix_values()
        self.adjacency_matrix = matrix_values
        units = []
        intersections = []
        equals = []
        columns = []
        coordinates = []
        n = 0

        for i in range(size):
            for j in range(size):
                if self.adjacency_matrix[j, i] == 1:
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

                new_matrix_add = np.zeros((size + 1, size + 1))

                # Получаем существующие данные из элементов QLineEdit
                existing_data = []
                for i in range(size):
                    row = []
                    for j in range(size):
                        entry = self.matrix_layout.itemAtPosition(i, j).widget()
                        value = entry.text()
                        row.append(value)
                    existing_data.append(row)

                for i in range(size):
                    if i < equals[z][1][-1] + 1 + n:
                        for j in range(size):
                            if j < equals[z][1][-1] + 1 + n:
                                new_matrix_add[i, j] = float(existing_data[i][j]) if existing_data[i][j] else 0
                            if j >= equals[z][1][-1] + 1 + n:
                                new_matrix_add[i, j + 1] = float(existing_data[i][j]) if existing_data[i][j] else 0

                    if i >= equals[z][1][-1] + 1 + n:
                        for j in range(size):
                            if j < equals[z][1][-1] + 1 + n:
                                new_matrix_add[i + 1, j] = float(existing_data[i][j]) if existing_data[i][j] else 0
                            if j >= equals[z][1][-1] + 1 + n:
                                new_matrix_add[i + 1, j + 1] = float(existing_data[i][j]) if existing_data[i][j] else 0

                for i in range(len(equals[z][0])):
                    for j in range(len(equals[z][1])):
                        new_matrix_add[equals[z][1][j] + n, equals[z][0][i] + 1 + n] = 0
                        new_matrix_add[equals[z][1][j] + n, equals[z][1][-1] + 1 + n] = 1
                    new_matrix_add[equals[z][1][-1] + 1 + n, equals[z][0][i] + 1 + n] = 1

                self.adjacency_matrix = new_matrix_add
                self.clear_matrix_layout()

                for i in range(size + 1):
                    for j in range(size + 1):
                        entry = QLineEdit(str(int(self.adjacency_matrix[i, j])))
                        self.matrix_layout.addWidget(entry, i, j)
                size = size + 1
                n = n + 1


def traverse(size, self, i, j, arr):
    for k in range(j, size):
        if self.adjacency_matrix[j, k] == 1:
            self.adjacency_matrix[i, k] = 0
            for l in range(len(arr)):
                self.adjacency_matrix[arr[l], k] = 0
            arr.append(j)
            traverse(size, self, i, k, arr)
            arr.pop()






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatrixApp()
    window.show()
    sys.exit(app.exec_())
