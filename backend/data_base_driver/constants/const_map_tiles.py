import os

from data_base_driver.constants.const_admin import DEPLOY_SETTING

mode = os.environ.get('MODE')


class MAP_TILES:
    TILES = DEPLOY_SETTING['tiles'] if mode == 'deploy' else [
        {
            'id': 1,
            'title': 'OSM',
            'subtitle': 'Схема (Интернет)',
            'url': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            'attr': '',
            'tms': False,
            'color': 'red',
        },
        {
            'id': 2,
            'title': 'OSM',
            'subtitle': 'Схема (Локальная сеть)',
            'url': 'http://200.200.200.231/osm/{z}/{x}/{y}.png',
            'attr': '',
            'tms': False,
        },
        {
            'id': 3,
            'title': 'Yandex',
            'subtitle': 'Интернет',
            'url': 'https://core-sat.maps.yandex.net/tiles?l=sat&v=3.786.0&x={x}&y={y}&z={z}&scale=2&lang=ru_UA',
            'attr': '',
            'tms': False,
            'crs': 'L.CRS.EPSG3395',
            'color': 'red',
        },
        {
            'id': 4,
            'title': 'Yandex',
            'subtitle': 'Спутник (Локальная сеть)',
            'url': 'http://200.200.200.232/{z}/{x}/{y}.jpg',
            'attr': '',
            'tms': False,
            'crs': 'L.CRS.EPSG3395',
        },
        {
            'id': 5,
            'title': 'ESRI',
            'subtitle': 'Спутник (Интернет)',
            'url': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            'attr': '',
            'tms': False,
            'color': 'red',
        },
        {
            'id': 6,
            'title': 'ОТМ',
            'subtitle': 'Схема (Интернет)',
            'url': 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
            'attr': '',
            'tms': False,
            'color': 'red',
        },
        {
            'id': 7,
            'title': 'Stamen',
            'subtitle': 'Черно-белая (Интернет)',
            'url': 'http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png',
            'attr': '',
            'tms': False,
            'color': 'red',
        }
    ]
