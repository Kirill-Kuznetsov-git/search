import math


def lonlat_distance(a, b):
    degree_to_kilometers_factor = 111
    a_lon, a_lat = float(a[0]), float(a[1])
    b_lon, b_lat = float(b[0]), float(b[1])

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lon + b_lon) / 2)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_kilometers_factor
    dy = abs(a_lat - b_lat) * degree_to_kilometers_factor * lat_lon_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance
