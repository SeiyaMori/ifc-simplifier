# main.py

import sys
from PyQt6.QtCore import QSize, Qt, QEvent, QSortFilterProxyModel
from PyQt6.QtWidgets import QPushButton, QLineEdit, QApplication, QMainWindow, QWidget, QTableView, QStyledItemDelegate, QItemDelegate, QHBoxLayout, QVBoxLayout, QComboBox, QLabel
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel


class CheckBoxDelegate(QItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox cell of the column to which it's applied.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        """
        Important, otherwise an editor is created if the user clicks in this cell.
        """
        return None

    def paint(self, painter, option, index):
        """
        Paint a checkbox without the label.
        """
        self.drawCheck(painter, option, option.rect, Qt.CheckState.Unchecked if int(index.data()) == 0 else Qt.CheckState.Checked)

    def editorEvent(self, event, model, option, index):
        '''
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton and this cell is editable. Otherwise do nothing.
        '''

        if event.type() == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            # Change the checkbox-state
            self.setModelData(None, model, index)
            return True

        return False


    def setModelData (self, editor, model, index):
        '''
        The user wanted to change the old state in the opposite.
        '''
        model.setData(index, 1 if int(index.data()) == 0 else 0, Qt.ItemDataRole.EditRole)



class ReadOnlyDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def createEditor(self, parent, option, index):
        return None


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.w = None  # No external window yet.

        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(800, 600))
        #self.setMaximumSize(QSize(1200,900))

        self._table_view = QTableView(self)
        #self._table_view.setItemDelegate(ReadOnlyDelegate())
        #self._table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        #self._table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        #self._table_view.setEditTriggers(QTableView.EditTrigger.EditKeyPressed)
        #self._table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self._table_view.setItemDelegateForColumn(4, CheckBoxDelegate())
        #self.setCentralWidget(self._table_view)

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

        # Filter dropdown label
        self.filter_label = QLabel("Filter controls")
        font = self.filter_label.font()
        font.setPointSize(12)
        self.filter_label.setFont(font)
        self.filter_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        

        # Filter settings button
        self.filter_button = QPushButton(text="Filter settings", parent=self)
        self.filter_button.clicked.connect(self.show_new_window)

        # Search bar
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search entire table")
        self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)


        # Table label
        self.table_label = QLabel("Elements")
        font = self.table_label.font()
        font.setPointSize(12)
        self.table_label.setFont(font)
        self.table_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.filter_label)
        layout.addWidget(self.filter_button)
        layout.addWidget(self.searchbar)
        layout.addWidget(self.table_label)
        layout.addWidget(self._table_view)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
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