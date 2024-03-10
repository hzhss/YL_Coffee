import sys
import sqlite3

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTableWidgetItem, QTableWidget, QHBoxLayout

class addEditCoffee(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.connection = sqlite3.connect("coffee.db")
        self.addButton.clicked.connect(self.add)
        self.changeButton.clicked.connect(self.change)

    def add(self):
        cur = self.connection.cursor()
        lst_of_line = [self.name_sort_line.text(), self.degree_line.text(), self.corn_line.text(),
                       self.taste_line.text(), self.price_line.text(), self.volume_line.text()]
        que = ("""INSERT INTO coffee ([название сорта], [степень обжарки], [молотый/в зернах], [описание вкуса], [цена, руб.], [объем упаковки, кг])
VALUES (""")
        for i in range(len(lst_of_line) - 1):
            if not lst_of_line[i]:
                que += 'NULL, '
            elif i == len(lst_of_line) - 2:
                que += f"{lst_of_line[i]}, "
            else:
                que += f"'{lst_of_line[i]}', "
        if not lst_of_line[-1]:
            que += 'NULL);'
        else:
            que += f"{lst_of_line[-1]});"
        cur.execute(que)
        self.connection.commit()

    def change(self):
        curs = self.connection.cursor()
        self.change_line.text()
        que1 = (f"""UPDATE coffee SET [{self.change_line.text()}] = '{self.new_line.text()}' 
        WHERE ID = {self.id_line.text()}""")
        curs.execute(que1)
        self.connection.commit()


    def closeEvent(self, event):
        # При закрытии формы закроем и наше соединение
        # с базой данных
        self.connection.close()

class Table(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.db")
        cur = self.connection.cursor()
        result = cur.execute("""SELECT * FROM coffee""").fetchall()

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                                    'описание вкуса', 'цена', 'объем упаковки'])
        # Заполняем таблицу элементами
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        # При закрытии формы закроем и наше соединение
        # с базой данных
        self.connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Table()
    ex.show()
    ex1 = addEditCoffee()
    ex1.show()
    sys.exit(app.exec())