import { CRS, } from 'proj4leaflet';


export const MAP_DATA_MENU_TILES = [
  {
    title:    'OSM',
    subtitle: 'Схема (Интернет)',
    url:      'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attr:     '',
    tms:      false,
    //crs:      L.CRS.EPSG3857,
    color:    'red',
  },
  {
    title:    'OSM',
    subtitle: 'Схема (Локальная сеть)',
    url:      'http://200.200.200.231/osm/{z}/{x}/{y}.png',
    attr:     '',
    tms:      false,
  },
  {
    title:    'Yandex',
    subtitle: 'Интернет',
    url:      'https://core-sat.maps.yandex.net/tiles?l=sat&v=3.786.0&x={x}&y={y}&z={z}&scale=2&lang=ru_UA',
    attr:     '',
    tms:      false,
    crs:      L.CRS.EPSG3395,
    color:    'red',
  },
  {
    title:    'Yandex',
    subtitle: 'Спутник (Локальная сеть)',
    url:      'http://200.200.200.232/{z}/{x}/{y}.jpg',
    attr:     '',
    tms:      false,
    crs:      L.CRS.EPSG3395, //+L.CRS.EPSG3857,  -L.CRS.EPSG4326
  },
  {
    title:    'ESRI',
    subtitle: 'Спутник (Интернет)',
    url:      'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr:     '',
    tms:      false,
    color:    'red',
  },
  {
    title:    'ОТМ',
    subtitle: 'Схема (Интернет)',
    url:      'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    attr:     '',
    tms:      false,
    color:    'red',
  },
  {
    title:    'Stamen',
    subtitle: 'Черно-белая (Интернет)',
    url:      'http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png',
    attr:     '',
    tms:      false,
    color:    'red',
  },
];
