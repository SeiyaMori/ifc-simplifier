# main.py

from PyQt6.QtCore import QSize, Qt, QAbstractTableModel
from PyQt6.QtWidgets import QTableView, QFileDialog, QApplication, QPushButton, QMainWindow
from PyQt6.QtGui import QAction

import ifcopenshell
import sys

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        # Widow title
        self.setWindowTitle("My App")

        # Window size
        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(1000,700))


        # Add button

        # Menu action
        button_open_file = QAction("Open...", self)
        button_open_file.triggered.connect(self.open_file)
        button_quit_app = QAction("Quit", self)
        button_quit_app.triggered.connect(self.quit_app)

        # Add menu bar
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction(button_open_file)
        file_menu.addSeparator()
        file_menu.addAction(button_quit_app)

        # Data table
        self.table = QTableView()

        data = [
          [4, 9, 2],
          [1, 0, 0],
          [3, 5, 0],
          [3, 3, 2],
          [7, 8, 9],
        ]

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)
    
    def quit_app(self):
        self.app.quit()
    
    def open_file(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "${HOME}",
            "IFC Files (*.ifc)",
        )
        if fname[0] == "":
            return
        self.get_file_content(fname[0])

    
    def get_file_content(self, file_path):
        file = ifcopenshell.open(file_path)

        # Get wall type
        walls = file.by_type("IfcWall")
        wall_type = ifcopenshell.util.element.get_type(walls[0])
        psets = ifcopenshell.util.element.get_psets(wall_type)
        print(psets)
        

        return file


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow(app)
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.
