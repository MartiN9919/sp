import { CRS, } from 'proj4leaflet';


export const MAP_DATA_MENU_TILES = [
  {
    title:    'OSM',
    subtitle: 'Схема (Интернет)',
    icon:     'mdi-map-outline',
    url:      'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attr:     '',
    tms:      false,
    //crs:      L.CRS.EPSG3857,
  },
  {
    title:    'OSM',
    subtitle: 'Схема (Локальная сеть)',
    icon:     'mdi-map-outline',
    url:      'http://200.200.200.231/osm/{z}/{x}/{y}.png',
    attr:     '',
    tms:      false,
  },

  // {
  //   title:    'OSM',
  //   subtitle: 'Схема (Локальная сеть)',
  //   url:      'http://192.168.56.1:8080/osm/{z}/{x}/{y}.png',
  //   icon:     'mdi-map-outline',
  //   attr:     '',
  //   tms:      false,
  //   enabled:  false,
  // },

  {
    title:    'Yandex',
    subtitle: 'Интернет',
    url:      'https://core-sat.maps.yandex.net/tiles?l=sat&v=3.786.0&x={x}&y={y}&z={z}&scale=2&lang=ru_UA',
    icon:     'mdi-map-outline',
    attr:     '',
    tms:      false,
    crs:      L.CRS.EPSG3395,
    enabled:  false,
  },

  {
    title:    'ESRI',
    subtitle: 'Спутник (Интернет)',
    icon:     'mdi-map-outline',
    url:      'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr:     '',
    tms:      false,
  },
  {
    title:    'ОТМ',
    subtitle: 'Схема (Интернет)',
    url:      'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    icon:     'mdi-map-outline',
    attr:     '',
    tms:      false,
  },
  {
    title:    'Stamen',
    subtitle: 'Черно-белая (Интернет)',
    icon:     'mdi-map-outline',
    url:      'http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png',
    attr:     '',
    tms:      false,
  },
  {
    title:    'Yandex',
    subtitle: 'Спутник (Локальная сеть)',
    url:      'http://200.200.200.232/{z}/{x}/{-y}.jpg',
    icon:     'mdi-map-outline',
    attr:     '',
    tms:      false,
    crs:      L.CRS.EPSG4326, //+L.CRS.EPSG3857,  -L.CRS.EPSG4326 -L.CRS.EPSG3395, -L.CRS.Simple,
    enabled:  false,
  },
];
