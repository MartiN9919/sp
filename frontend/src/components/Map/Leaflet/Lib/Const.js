
export const MAP_STYLE = {
  COLOR: {
    KEY:    'color',
    DEF:    '#f00',               // цвет по умолчанию
    ORIGIN: '#000',               // цвет маркеров и фигур ДО    ИЗМЕНЕНИЯ
    MODIFY: '#f00',               // цвет маркеров и фигур ПОСЛЕ ИЗМЕНЕНИЯ
  },

  MARKER: {
    KEY:      'marker',
    ICON: {
      KEY:      'icon',
      DEF:      '',               // значение по умолчанию
      PREF_MDI: 'mdi-',           // маркер: шрифт mdi
      PREF_FS:  'fs-',            // маркер: шрифт дополнительный
      PULSE:    'pulse',          // маркер: пульсирующий
    },
    ZOOM:   { KEY: 'zoom' },
    SIZE:   { KEY: 'size', },
    SIZE_W: { KEY: 'size_w', },
    SIZE_H: { KEY: 'size_h', },
  },

  LINE: {
    KEY: 'line',
    TYPE: {                       // тип линии, совпадает с именем класса для установки стиля
      KEY: 'type',
      ANT: 'ant',                 // бегущая линия
    },
  },

  POLYGON: {
    KEY: 'polygon',
  },
};


export const COLORING = {         // раскраска в зависимости от значения
  COLOR: {
    BEGIN: '00FF00',              // цвет: начальный
    END:   'FF0000',              // цвет: конечный
  },
  FC: {
    VALUE: 'value',               // вход:  fc.features[i].property.VALUE - значение определяет цвет полигона
    COLOR: 'color',               // выход: fc.features[i].COLOR - расчитанный цвет полигона
  },
  GREEN_MIN: 'green_min',         // цвет полигона в зависимости от значения: зеленый(хуже)  -> красный(лучше) https://leafletjs.com/examples/choropleth/example.html
  GREEN_MAX: 'green_max',         // цвет полигона в зависимости от значения: зеленый(лучше) -> красный(хуже)
};


export const PATH = {
  MARKERS: 'img/markers/',        // путь к файлам маркеров
};
