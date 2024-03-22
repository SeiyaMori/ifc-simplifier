# main.py

import sys
from PyQt6.QtCore import QSize, Qt, QAbstractTableModel, QModelIndex, QEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QStyleOptionViewItem, QTableView, QStyledItemDelegate, QItemDelegate, QCheckBox
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
            
            # Set row height
            for i in range(self.model.rowCount()):
                self._table_view.setRowHeight(i, 20)

        else:
            print("Failed to connect to the database")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())