
export const MAP_ITEM = {
  FC: {
    KEY: 'fc',
    TYPE: {
      KEY: 'type',
      VAL: 'FeatureCollection',
    },

    FEATURES: {
      KEY: 'features',
      PROPERTIES: {
        KEY:     'properties',
        CLASS: {
          KEY: 'class',                  // key: класс для стилизации
          SEL: 'sel',                    // название класса: выделено (pulse)
          ANT: 'ant',                    // название класса: бегущая линия
          ICON_TYPE: 'icon',             // иконка
          ICON_PATH: 'img/markers/',     // иконка: путь к файлам иконок
          ICON_TYPE_SEPARATOR: '-',      // иконка: разделитель
          ICON_TYPE_MDI:   'mdi',        // иконка: шрифт mdi
          ICON_TYPE_FS:    'fs',         // иконка: шрифт fs
          ICON_TYPE_FILE:  'file',       // иконка: файл
          ICON_TYPE_PULSE: 'pulse',      // иконка: пульсирующая
        },
        VALUE: {                         // key: для полигона - вход:  fc.features[i].property.VALUE - значение, которое определяет цвет полигона
          KEY: 'value',
        },
        _COLOR_: {                       // key: заполняется программой, цвет заливки фигуры
          KEY: 'color',
        },
        _SEL_: {                         // key: заполняется программой, выделенный features[], true - выделено
          KEY: 'sel',
        },
      },
      GEOMETRY:  {
        KEY:     'geometry',
        TYPE: {
          KEY:       'type',
          GC:        'GeometryCollection',
          MARKER:    'Marker',           // кажется нужно использовать POINT
          POINT:     'Point',
          LINE:      'LineString',
          POLYGON:   'Polygon',
        },
        COORDINATES: {
          KEY:       'coordinates',
        },
        GEOMETRIES: {                    // вложенные геометрии MAP_ITEM.FC.FEATURES.GEOMETRY
          KEY:      'geometries',
        },
      },
    },

    STYLE: {                             // стили маркеров и фигур
      KEY:     'style',
      _COLOR_: {                         // в некоторых случаях транслируется сюда из MAP_ITEM.COLOR (чтобы использовать в стилях)
        KEY:   'color',
      },

      MARKER: {
        KEY:  'marker',
        ICON: {
          KEY:      'icon',
          DEF:      '',                  // значение по умолчанию
          PREF_MDI: 'mdi-',              // маркер: шрифт mdi
          PREF_FS:  'fs-',               // маркер: шрифт дополнительный
          PULSE:    'pulse',             // маркер: пульсирующий
        },
        ZOOM:   { KEY: 'zoom' },
        SIZE:   { KEY: 'size', },
        SIZE_W: { KEY: 'size_w', },
        SIZE_H: { KEY: 'size_h', },
        // CLASS: {                      // классы, без decoratorPath и decoratorSVG (не задействовано)
        //   KEY: 'class',
        // },
      },

      LINE: {
        KEY:   'line',
      },

      POLYGON: {
        KEY: 'polygon',
        COLORING: {
          KEY:   'coloring',
          GREEN: {
            KEY:   'green',
            MIN:   'min',                // цвет полигона в зависимости от значения: зеленый(хуже)  -> красный(лучше) https://leafletjs.com/examples/choropleth/example.html
            MAX:   'max',                // цвет полигона в зависимости от значения: зеленый(лучше) -> красный(хуже)
          },
          BEGIN:     '00FF00',           // цвет: начальный
          END:       'FF0000',           // цвет: конечный
        },
      },
    },
  },

  COLOR: {                               // копия в FC.STYLE._COLOR_
    KEY:        'color',
    DEF:        '#f00',                  // цвет по умолчанию
    ORIGIN:     '#000',                  // редактор: цвет ДО    ИЗМЕНЕНИЯ
    MODIFY:     '#f00',                  // редактор: цвет ПОСЛЕ ИЗМЕНЕНИЯ
    SCRIPT_OFF: '#696969FF',             // цвет неактивного скрипта
    SCRIPT_BANK: [                       // цвета активных скриптов
      '#FF0000FF',
      '#0008FFFF',
      '#008E00FF',
      '#A400A0FF',
      '#A400A0FF',
      '#4DD6D6FF',
      '#E3F017FF',
    ],
  },

  // ZOOM: {
  //   KEY: 'zoom',                      // увеличение карты
  // },

  _LEGEND_COLOR_: 'legend_color',        // [], заполняется программой

};
