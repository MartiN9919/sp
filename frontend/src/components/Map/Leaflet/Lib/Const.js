
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
