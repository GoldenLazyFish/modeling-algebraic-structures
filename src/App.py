import sys
import numpy as np

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel, QScrollArea, QHBoxLayout)
from PyQt5.QtGui import QPixmap


from AdjasencyMatrixProcessing import AdjasencyMatrixProcessing
from DB import DB

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

        self.matrix_size_input = QLineEdit("2")
        self.left_layout.addWidget(self.matrix_size_input)

        self.create_matrix_button = QPushButton("Create Matrix")
        self.create_matrix_button.clicked.connect(self.on_clicked_button_create_matrix)
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
        self.create_graph_button.clicked.connect(self.on_clicked_button_create_graph)
        self.right_layout.addWidget(self.create_graph_button)

        self.create_structure_button = QPushButton("Create Structure")
        self.create_structure_button.clicked.connect(self.on_clicked_button_create_structure)
        self.right_layout.addWidget(self.create_structure_button)

        self.flip_button = QPushButton("Flip")
        self.flip_button.clicked.connect(self.on_clicked_button_flip)
        self.right_layout.addWidget(self.flip_button)

        self.create_point_button = QPushButton("Create start and end")
        self.create_point_button.clicked.connect(self.on_clicked_button_create_point)
        self.right_layout.addWidget(self.create_point_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.on_clicked_button_reset)
        self.right_layout.addWidget(self.reset_button)

        self.add_element_button = QPushButton("Add Element")
        self.add_element_button.clicked.connect(self.on_clicked_button_add_element)
        self.right_layout.addWidget(self.add_element_button)

        self.matrix_id_label = QLabel("Matrix ID:")
        self.right_layout.addWidget(self.matrix_id_label)

        self.matrix_id_input = QLineEdit()
        self.right_layout.addWidget(self.matrix_id_input)

        self.save_to_db_button = QPushButton("Save to Database")
        self.save_to_db_button.clicked.connect(self.on_clicked_button_save_to_database)
        self.right_layout.addWidget(self.save_to_db_button)

        self.load_matrix_button = QPushButton("Load Matrix")
        self.load_matrix_button.clicked.connect(self.on_clicked_button_load_matrix_by_id)
        self.right_layout.addWidget(self.load_matrix_button)

        self.update_matrix_button = QPushButton("Update Matrix")
        self.update_matrix_button.clicked.connect(self.on_clicked_button_update_matrix_by_id)
        self.right_layout.addWidget(self.update_matrix_button)

        self.graph_view = QLabel()
        self.right_layout.addWidget(self.graph_view)

        self.processing = AdjasencyMatrixProcessing(2)
        self.display_matrix()

        self.DB = DB()

    def display_matrix(self) -> None:
        # cleaning layout
        for i in reversed(range(self.matrix_layout.count())):
            widget = self.matrix_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        # filling layout
        for i in range(self.processing.size):
            for j in range(self.processing.size):
                entry = QLineEdit(str(int(self.processing.matrix[i, j])))
                self.matrix_layout.addWidget(entry, i, j)

    def on_clicked_button_create_matrix(self) -> None:
        try:
            size = int(self.matrix_size_input.text())
            self.processing.create_matrix(size)
            self.display_matrix()

        except ValueError:
            print("Invalid input for matrix size")



    def on_clicked_button_create_graph(self) -> None:
        self.update_matrix()
        buf = self.processing.create_graph()

        # Display the graph in the QLabel
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        self.graph_view.setPixmap(pixmap)

    def on_clicked_button_create_structure(self) -> None:
        self.processing.create_structure()
        self.display_matrix()

    def update_matrix(self) -> None:
        matrix_values = []
        for i in range(self.processing.size):
            row = []
            for j in range(self.processing.size):
                widget = self.matrix_layout.itemAtPosition(i, j).widget()
                value = int(widget.text())
                row.append(value)
            matrix_values.append(row)
        self.processing.matrix = np.array(matrix_values)

    def on_clicked_button_flip(self) -> None:
        self.update_matrix()
        self.processing.flip()
        self.display_matrix()

    def on_clicked_button_reset(self):
        self.update_matrix()
        self.processing.reset()
        self.display_matrix()

    def on_clicked_button_create_point(self) -> None:
        self.update_matrix()
        self.processing.create_point()
        self.display_matrix()

    def on_clicked_button_add_element(self) -> None:
        self.update_matrix()
        self.processing.add_element()
        self.display_matrix()


    def on_clicked_button_save_to_database(self) -> None:
        try:
            # Get the matrix size
            size = int(self.matrix_size_input.text())

            # Create a list to store the matrix values
            matrix_values = []

            # Iterate through the matrix layout and extract the values
            for i in range(size):
                row = []
                for j in range(size):
                    widget = self.matrix_layout.itemAt(i * size + j).widget()
                    value = int(widget.text())
                    row.append(value)
                matrix_values.append(row)

            self.DB.save(matrix_values=matrix_values, size=size)

        except Exception as e:
            print(f"[ERROR] Error saving matrix data to the database: {e}")

    def on_clicked_button_load_matrix_by_id(self) -> None:
        try:
            # Get the matrix ID from the user input
            matrix_id = int(self.matrix_id_input.text())

            matrix_data, matrix_size = self.DB.load_by_id(matrix_id)

            # Update the UI with the loaded matrix
            self.matrix_size_input.setText(str(matrix_size))
            self.create_matrix()
            for i in range(matrix_size):
                for j in range(matrix_size):
                    widget = self.matrix_layout.itemAt(i * matrix_size + j).widget()
                    widget.setText(str(matrix_data[i][j]))

            print(f"[INFO] Matrix data with ID {matrix_id} loaded from the database")

        except Exception as e:
            print(f"[ERROR] Error loading matrix data from the database: {e}")

    def on_clicked_button_update_matrix_by_id(self) -> None:
        try:
            # Get the matrix ID from the user input
            matrix_id = int(self.matrix_id_input.text())

            # Get the matrix size
            size = int(self.matrix_size_input.text())

            # Create a list to store the matrix values
            matrix_values = []

            # Iterate through the matrix layout and extract the values
            for i in range(size):
                row = []
                for j in range(size):
                    widget = self.matrix_layout.itemAt(i * size + j).widget()
                    value = int(widget.text())
                    row.append(value)
                matrix_values.append(row)

            # Convert the matrix to a string
            matrix_str = str(matrix_values)

            self.DB.update_by_id(matrix_id, matrix_str, size)

        except Exception as e:
            print(f"[ERROR] Error updating matrix data in the database: {e}")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatrixApp()
    window.show()
    sys.exit(app.exec_())
