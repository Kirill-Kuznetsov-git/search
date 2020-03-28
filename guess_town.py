import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QLCDNumber
import time

const = ['Димитровград', 'Москва', 'Казань', 'Самара', 'Псков']

SCREEN_SIZE = [800, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.p = 0
        self.i = 0
        self.spn = 0.12111700000000525
        self.initUI()

    def getImage(self, name):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": name,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)
        json_response = response.json()

        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]

        toponym_coodrinates = ','.join(toponym["Point"]["pos"].split(' '))

        h = toponym_coodrinates.split(',')

        a = [0, 0]
        a[0] = str(float(h[0]) - 0.039999)
        a[1] = str(float(h[1]) + 0.00999)
        a = ','.join(a)

        b = [0, 0]
        b[0] = str(float(h[0]) + 0.039999)
        b[1] = str(float(h[1]) + 0.00999)
        b = ','.join(b)

        c = [0, 0]
        c[0] = str(float(h[0]) + 0.039999)
        c[1] = str(float(h[1]))
        c = ','.join(c)

        d = [0, 0]
        d[0] = str(float(h[0]) - 0.039999)
        d[1] = str(float(h[1]))
        d = ','.join(d)

        if not response:
            print("Ошибка выполнения запроса:")
            sys.exit(1)

        map_params = {
            "ll": toponym_coodrinates,
            "spn": ",".join([str(self.spn), str(self.spn)]),
            "l": "map",
            'pl': f'c:ec473fFF,f:ec473fFF, w:7,{a},{b},{c},{d},{a}'
        }
        print(toponym_coodrinates, ",".join([str(self.spn), str(self.spn)]))
        map_api_server = "http://static-maps.yandex.ru/1.x/"

        response = requests.get(map_api_server, params=map_params)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.btn = QPushButton('ок', self)
        self.btn.resize(100, 20)
        self.btn.move(560, 185)
        self.btn.clicked.connect(self.plas)

        self.LCD_first = QLCDNumber(self)
        self.LCD_first.move(560, 100)
        self.LCD_first.display(int(self.p))

        self.label = QLabel('Введите город:', self)
        self.label.move(560, 130)

        self.label_end = QLabel('Конец игры', self)
        self.label_end.move(560, 130)
        self.label_end.hide()

        self.line = QLineEdit(self)
        self.line.move(560, 155)

        self.getImage(const[self.i])
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(550, 450)
        self.image.setPixmap(self.pixmap)

    def plas(self):
        if self.line.text() == const[self.i] or self.line.text() == const[self.i].lower():
            self.p += 1
            self.LCD_first.display(int(self.p))

        try:
            self.i += 1
            self.getImage(const[self.i])
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
            self.line.clear()
        except Exception:
            print(f'Ваш результат: {self.p} из {len(const)}')
            quit()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
