# main.py

import sys
from PyQt6.QtCore import QSize, Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QStyledItemDelegate
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel


class ReadOnlyDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def createEditor(self, parent, option, index):
        return None


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(QSize(800, 600))
        self.setMaximumSize(QSize(1200,900))

        self._table_view = QTableView(self)
        self._table_view.setItemDelegate(ReadOnlyDelegate())
        #self._table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        #self._table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        #self._table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.setCentralWidget(self._table_view)

        self.db = QSqlDatabase.addDatabase("QSQLITE")  
        #self.db.setHostName("127.0.0.1")
        self.db.setDatabaseName("sqlite.db")
        #self.db.setUserName("root")
        #self.db.setPassword("1234")

        if self.db.open():
            print("Connected to the database")

            self.model = QSqlTableModel(self)
            self.model.setTable("elements")  # Set the table name

            # Set boolean field as checkboxes
            self.model.setHeaderData(4, Qt.Orientation.Horizontal, "exclude")

            # Edit strategy
            self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

            if self.model.select():
                self._table_view.setModel(self.model)
            else:
                print("Failed to select data from the table")
            
            

        else:
            print("Failed to connect to the database")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())