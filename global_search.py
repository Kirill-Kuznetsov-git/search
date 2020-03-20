import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image
from scope import scale
from distance import lonlat_distance

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}


response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()

# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
scope = scale(toponym_to_find)

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": ','.join(toponym_coodrinates.split(' ')),
    "type": "biz"
}
all_points = []
response = requests.get(search_api_server, params=search_params)
time = []
json_response = response.json()


for i in range(10):
    organization = json_response["features"][i]
    try:
        if organization["properties"]["CompanyMetaData"]["Hours"]['text'].split(' ')[0][:-1] == 'ежедневно':
            time.append('pm2blm')
        else:
            time.append('pm2gnm')
    except Exception:
        time.append('pm2grm')
    org_address = organization["properties"]["CompanyMetaData"]["address"]

    point = organization["geometry"]["coordinates"]
    org_point = "{},{}".format(point[0], point[1])
    all_points.append(org_point)

map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": f'{scale(org_address, toponym_to_find)},{scale(org_address, toponym_to_find)}',
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": "{},{}~{},{}~{},{}~{},{}~{},{}~{},{}~{},{}~{},{}~{},{}~{},{}".format(all_points[0], time[0], all_points[1], time[1],
                                                                               all_points[2], time[2], all_points[3], time[3],
                                                                               all_points[4], time[4], all_points[5], time[5],
                                                                               all_points[6], time[6], all_points[7], time[7],
                                                                               all_points[8], time[8], all_points[9], time[9])
}

map_api_server = "http://static-maps.yandex.ru/1.x/"

response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(response.content)).show()
