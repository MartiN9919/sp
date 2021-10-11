
export const MAP_ITEM = {
  FC: {
    KEY: 'fc',
    FEATURES: {
      KEY: 'features',
      PROPERTIES: {
        KEY:   'properties',
        VALUE: 'value',               // для полигона - вход:  fc.features[i].property.VALUE - значение, которое определяет цвет полигона
      },
    },
  },

  LEGEND_COLOR: 'legend_color',       // [], заполняется автоматически
};



export const MAP_STYLE = {
  KEY: 'style',

  COLOR: {
    KEY:    'color',
    DEF:    '#f00',               // цвет по умолчанию
    ORIGIN: '#000',               // цвет маркеров и фигур ДО    ИЗМЕНЕНИЯ
    MODIFY: '#f00',               // цвет маркеров и фигур ПОСЛЕ ИЗМЕНЕНИЯ
  },

  MARKER: {
    KEY:  'marker',
    PATH: 'img/markers/',         // путь к файлам маркеров
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
    COLORING: {
      KEY:   'coloring',
      GREEN: {
        KEY:   'green',
        MIN:   'min',             // цвет полигона в зависимости от значения: зеленый(хуже)  -> красный(лучше) https://leafletjs.com/examples/choropleth/example.html
        MAX:   'max',             // цвет полигона в зависимости от значения: зеленый(лучше) -> красный(хуже)
      },
      BEGIN:     '00FF00',        // цвет: начальный
      END:       'FF0000',        // цвет: конечный
    },
  },
};
