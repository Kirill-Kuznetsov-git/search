import sys
import math
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt

SCREEN_SIZE = [800, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.spn_first = ['', '']
        self.spn = ['', '']
        self.size_map = [550 * 111, 450 * 111 * math.cos(math.radians(550) / 2)]
        self.ll = []
        self.pt = []
        self.l = 'map'
        self.initUI()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and float(self.spn[0]) / 5 > 0.0001 and float(self.spn[1]) / 5 > 0.0001:
            self.spn[0] = str(float(self.spn[0]) / 5)
            self.spn[1] = str(float(self.spn[1]) / 5)
            self.getImage()
        if event.key() == Qt.Key_PageDown and float(self.spn[0]) * 5 <= 90 and float(self.spn[1]) * 5 <= 90:
            self.spn[0] = str(float(self.spn[0]) * 5)
            self.spn[1] = str(float(self.spn[1]) * 5)
            self.getImage()
        if event.key() == Qt.Key_Up:
            self.ll[1] = str(float(self.ll[1]) + float(self.spn[1]) * float(self.ll[1]) / 60)
            self.getImage()
        if event.key() == Qt.Key_Down:
            self.ll[1] = str(float(self.ll[1]) - float(self.spn[1]) * float(self.ll[1]) / 60)
            self.getImage()
        if event.key() == Qt.Key_Left:
            self.ll[0] = str(float(self.ll[0]) - float(self.spn[0]) * float(self.ll[1]) / 60)
            self.getImage()
        if event.key() == Qt.Key_Right:
            self.ll[0] = str(float(self.ll[0]) + float(self.spn[0]) * float(self.ll[1]) / 60)
            self.getImage()

    def getImage(self):
        pt_str = ''
        for i in range(len(self.pt)):
            if i != len(self.pt) - 1:
                pt_str += str(self.pt[i])
                pt_str += ',pm2dgl~'
            else:
                pt_str += str(self.pt[i])
                pt_str += ',pm2dgl'
        map_params = {
            "ll": ','.join(self.ll),
            "spn": ','.join(self.spn),
            "l": self.l,
            'pt': f"{pt_str}"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"

        response = requests.get(map_api_server, params=map_params)
        if not response:
            print("Ошибка выполнения запроса:")
            sys.exit(1)

        self.map_file = "map.png"

        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.btn = QPushButton('OK', self)
        self.btn.resize(100, 20)
        self.btn.move(560, 200)
        self.btn.clicked.connect(self.plas)

        self.btn_search = QPushButton('Искать', self)
        self.btn_search.resize(100, 20)
        self.btn_search.move(560, 270)
        self.btn_search.clicked.connect(self.search_org)

        self.btn_del = QPushButton('Удалить последнюю метку', self)
        self.btn_del.resize(160, 20)
        self.btn_del.move(560, 290)
        self.btn_del.clicked.connect(self.delete_mark)

        self.label_ll = QLabel('Координаты через запетую:', self)
        self.label_ll.move(560, 100)

        self.label_spn = QLabel('Маштаб через запятую:', self)
        self.label_spn.move(560, 150)

        self.label_search = QLabel('Название организации:', self)
        self.label_search.move(560, 230)

        self.line_ll = QLineEdit(self)
        self.line_ll.move(560, 120)

        self.line_spn = QLineEdit(self)
        self.line_spn.move(560, 170)

        self.line_search = QLineEdit(self)
        self.line_search.move(560, 250)

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(550, 450)

        self.radio_btn_1 = QRadioButton('Схема', self)
        self.radio_btn_1.move(720, 100)
        self.radio_btn_1.setChecked(True)
        self.radio_btn_2 = QRadioButton('Спутник', self)
        self.radio_btn_2.move(720, 120)
        self.radio_btn_3 = QRadioButton('Гибрид', self)
        self.radio_btn_3.move(720, 140)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_btn_1)
        self.button_group.addButton(self.radio_btn_2)
        self.button_group.addButton(self.radio_btn_3)
        self.button_group.buttonClicked.connect(self.on_radio_button_clicked)

    def plas(self):
        self.spn[0] = str(float(self.line_spn.text().split(',')[0]))
        self.spn[1] = str(float(self.line_spn.text().split(',')[1]))
        self.spn_first = [float(self.line_spn.text().split(',')[0]), float(self.line_spn.text().split(',')[1])]
        self.ll = [self.line_ll.text().split(',')[0], self.line_ll.text().split(',')[1]]
        self.getImage()

    def on_radio_button_clicked(self, button):
        if button.text() == 'Схема':
            self.l = 'map'
        elif button.text() == 'Спутник':
            self.l = 'sat'
        else:
            self.l = 'sat,skl'
        self.getImage()

    def search_org(self):
        search_api_server = "https://search-maps.yandex.ru/v1/"
        api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

        if len(self.ll) != 0:
            search_params = {
                "apikey": api_key,
                "text": f"{self.line_search.text()}",
                "lang": "ru_RU",
                "ll": ','.join(self.ll),
                "type": "biz"
            }
        else:
            search_params = {
                "apikey": api_key,
                "text": f"{self.line_search.text()}",
                "lang": "ru_RU",
                "type": "biz"
            }

        response = requests.get(search_api_server, params=search_params)
        if not response:
            print('ERROR')
            sys.exit(1)

        json_response = response.json()
        organization = json_response["features"][0]
        point = organization["geometry"]["coordinates"]
        org_point = "{},{}".format(point[0], point[1])
        self.pt.append(org_point)
        self.ll = org_point.split(',')
        delta = "0.1"
        self.spn_first = [float(delta), float(delta)]
        if self.spn[0] == '' and self.spn[1] == '':
            self.spn = [delta, delta]

        self.getImage()

    def delete_mark(self):
        try:
            del self.pt[-1]
            self.getImage()
        except Exception:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
