import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Эспрессо')

        self.ground_beans = ['В зернах', 'Молотый']

        self.connection = sqlite3.connect('coffee.db')
        self.update_table()

        self.btn_update.clicked.connect(self.update_table)

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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
ex = MainWidget()
ex.show()
sys.excepthook = except_hook
sys.exit(app.exec_())
