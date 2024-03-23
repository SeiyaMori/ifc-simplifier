# helpers.py

from PyQt6.QtCore import QSize, Qt, QEvent, QSortFilterProxyModel
from PyQt6.QtWidgets import QPushButton, QLineEdit, QApplication, QMainWindow, QWidget, QTableView, QStyledItemDelegate, QItemDelegate, QGridLayout, QVBoxLayout, QComboBox, QLabel
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
