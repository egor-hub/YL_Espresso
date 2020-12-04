import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem

from UI.main_ui import Ui_MainWindow
from UI.addEditCoffeeForm_ui import Ui_Dialog


class EditVarietyDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, window_title):
        super().__init__(parent)
        # uic.loadUi('addEditCoffeeForm.ui', self)
        self.setupUi(self)

        self.setWindowTitle(window_title)

        self.buttonBox.accepted.connect(self.ok_pressed)

    def check_form(self):
        if not self.edit_title.text():
            return False
        return True

    def ok_pressed(self):
        if not self.check_form():
            return self.label_info.setText('Неверно заполнена форма')
        self.accept()

    def set_variety(self, variety):
        self.edit_title.setText(variety[0])
        self.edit_roasting_degree.setText(variety[1])
        self.select_ground_beans.setCurrentText(variety[2])
        self.edit_taste.setText(variety[3])
        self.spin_price.setValue(int(variety[4]))
        self.spin_size.setValue(int(variety[5]))

    def get_query_params(self):
        title = self.edit_title.text()
        roasting_degree = self.edit_roasting_degree.text()
        ground = self.select_ground_beans.currentIndex()
        taste = self.edit_taste.text()
        price = self.spin_price.value()
        size = self.spin_size.value()
        return title, roasting_degree, ground, taste, price, size


class MainWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('main.ui', self)
        self.setupUi(self)

        self.setWindowTitle('Эспрессо')

        self.ground_beans = ['В зернах', 'Молотый']

        self.connection = sqlite3.connect('data/coffee.db')
        self.update_table()

        self.btn_update.clicked.connect(self.update_table)
        self.btn_add.clicked.connect(self.add_variety)
        self.btn_edit.clicked.connect(self.edit_variety)

    def update_table(self):
        query = 'SELECT * FROM Varieties'
        result = self.connection.cursor().execute(query).fetchall()

        self.table.setRowCount(0)
        for i, row in enumerate(result):
            row = map(str, row)
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                if j == 3:
                    elem = self.ground_beans[int(elem)]
                self.table.setItem(i, j, QTableWidgetItem(elem))
        self.table.resizeColumnsToContents()

    def add_variety(self):
        dialog = EditVarietyDialog(self, 'Добавить вид')

        is_ok = dialog.exec_()
        if not is_ok:
            return

        query = """
        INSERT INTO Varieties (title, roasting_degree, ground, taste, price, size)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = dialog.get_query_params()
        self.connection.cursor().execute(query, params)
        self.connection.commit()

        self.update_table()

    def edit_variety(self):
        row_index = self.table.currentRow()
        if row_index < 0:
            return

        row = [self.table.item(row_index, i).text() for i in range(self.table.columnCount())]

        dialog = EditVarietyDialog(self, 'Изменить вид')
        dialog.set_variety(row[1:])

        is_ok = dialog.exec_()
        if not is_ok:
            return

        query = """
        UPDATE Varieties
        SET title = ?, roasting_degree = ?, ground = ?, taste = ?, price = ?, size = ?
        WHERE id = ?
        """
        params = tuple(list(dialog.get_query_params()) + [row[0]])
        self.connection.cursor().execute(query, params)
        self.connection.commit()

        self.update_table()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
ex = MainWidget()
ex.show()
sys.excepthook = except_hook
sys.exit(app.exec_())
