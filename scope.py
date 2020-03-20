import requests


def scale(name):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": name,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass

    json_response = response.json()

    coords = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]['boundedBy']['Envelope']

    return [str(float(coords['upperCorner'].split(' ')[0]) - float(coords['lowerCorner'].split(' ')[0])),
            str(float(coords['upperCorner'].split(' ')[1]) - float(coords['lowerCorner'].split(' ')[1]))]
