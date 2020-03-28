import requests


def scale(*name):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    x_up = 0
    y_up = 0

    x_low = 10000000000000
    y_low = 10000000000000

    for i in name:
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": i,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            pass

        json_response = response.json()
        coords = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]['boundedBy']['Envelope']

        if float(coords['upperCorner'].split(' ')[0]) > x_up:
            x_up = float(coords['upperCorner'].split(' ')[0])
        if float(coords['upperCorner'].split(' ')[1]) > y_up:
            y_up = float(coords['upperCorner'].split(' ')[1])
        if float(coords['lowerCorner'].split(' ')[0]) < x_low:
            x_low = float(coords['lowerCorner'].split(' ')[0])
        if float(coords['lowerCorner'].split(' ')[1]) < y_low:
            y_low = float(coords['lowerCorner'].split(' ')[1])

    return min(x_up - x_low, y_up - y_low)
