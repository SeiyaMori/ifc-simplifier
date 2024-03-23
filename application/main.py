# main.py

import sys
from PyQt6.QtCore import QSize, Qt, QSortFilterProxyModel
from PyQt6.QtWidgets import QPushButton, QLineEdit, QApplication, QMainWindow, QWidget, QTableView, QGridLayout, QVBoxLayout, QLabel
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from helpers import CheckBoxDelegate


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set window properties
        self.set_properties()

        # Other windows
        self.w = None  # No external window yet.

        # Widgets ----

        # Table controls label
        self.table_controls_label = self.create_table_controls_label()

        # Table view
        self.table, self.proxy_model = self.create_table_widget()

        # Table controls
        self.table_controls = self.create_table_controls()

        # Table label
        self.table_label = self.create_table_label()

        # Layout management ----

        layout = QVBoxLayout()
        layout.addWidget(self.table_controls_label)
        layout.addLayout(self.table_controls)
        layout.addWidget(self.table_label)
        layout.addWidget(self.table)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def set_properties(self):
        # Title
        self.setWindowTitle("IFC Model Simplifier")

        # Window dimensions
        self.setMinimumSize(QSize(800, 600))
    
    def create_table_controls_label(self):
        label = QLabel("Filter controls")
        font = label.font()
        font.setPointSize(12)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        return label

    def create_table_controls(self):
        # Filter settings button
        button = QPushButton(text="Filters", parent=self)
        button.clicked.connect(self.show_new_window)

        # Search bar
        searchbar = QLineEdit()
        searchbar.setPlaceholderText("Search entire table")
        searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)

        # Table controls
        table_controls = QGridLayout()
        table_controls.addWidget(button, 0, 0)
        table_controls.addWidget(searchbar, 0, 1)
        return table_controls

    def create_table_label(self):
        label = QLabel("Elements")
        font = label.font()
        font.setPointSize(12)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        return label

    def create_table_widget(self):
        self._table_view = QTableView(self)
        #self._table_view.setItemDelegate(ReadOnlyDelegate())
        #self._table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        #self._table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        #self._table_view.setEditTriggers(QTableView.EditTrigger.EditKeyPressed)
        #self._table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self._table_view.setItemDelegateForColumn(4, CheckBoxDelegate())

        self.db = QSqlDatabase.addDatabase("QSQLITE")  
        self.db.setDatabaseName("sqlite.db")

        if self.db.open():
            print("Connected to the database")

            self.model = QSqlTableModel(self)
            self.model.setTable("elements")  # Set the table name

            # Set boolean field as checkboxes
            self.model.setHeaderData(4, Qt.Orientation.Horizontal, "exclude")

            # Edit strategy
            self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

            # Filter proxy model
            self.proxy_model = QSortFilterProxyModel()
            self.proxy_model.setFilterKeyColumn(-1)
            self.proxy_model.setSourceModel(self.model)
            self.proxy_model.sort(0, Qt.SortOrder.AscendingOrder)


            if self.model.select():
                self._table_view.setModel(self.proxy_model)
            else:
                print("Failed to select data from the table")
            
            # Set row height
            for i in range(self.model.rowCount()):
                self._table_view.setRowHeight(i, 20)

        else:
            print("Failed to connect to the database")
        return self._table_view, self.proxy_model
    
    def show_new_window(self, checked):
        if self.w is None:
            self.w = AnotherWindow()
        self.w.show()


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())