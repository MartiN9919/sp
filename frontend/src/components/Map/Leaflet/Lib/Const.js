export const MAP_CONST = {
  COLOR: {
    DEFAULT:            '#f00',           // цвет по умолчанию
    DEFAULT_STYLE_PATH: 'gray',           // цвет по умолчанию для стилизации (декорирования) фигур
    EDITOR_ORIGIN:      '#000',           // редактор: цвет ДО    ИЗМЕНЕНИЯ
    EDITOR_MODIFY:      '#f00',           // редактор: цвет ПОСЛЕ ИЗМЕНЕНИЯ
    SCRIPT_OFF:         '#696969FF',      // цвет неактивного скрипта
    SCRIPT_BANK: [                        // цвета активных скриптов
      '#FF0000FF',
      '#0008FFFF',
      '#008E00FF',
      '#A400A0FF',
      '#A400A0FF',
      '#4DD6D6FF',
      '#E3F017FF',
    ],
    COLORING: {                           // цвет в зависимости от значения
      GREEN_MIN: 'green_min',             // зеленый(хуже)  -> красный(лучше) https://leafletjs.com/examples/choropleth/example.html
      GREEN_MAX: 'green_max',             // зеленый(лучше) -> красный(хуже)
      BEGIN:     '00FF00',                // цвет: начальный
      END:       'FF0000',                // цвет: конечный
    },
  },

  GEOMETRY_TYPE: {
    GC:        'GeometryCollection',
    POINT:     'Point',
    LINE:      'LineString',
    POLYGON:   'Polygon',
  },
};

export const MAP_ITEM = {
  COLOR: 'color',                        // копия в FC.STYLE._COLOR_
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
        VALUE: 'value',                  // значение, которое определяет цвет полигона
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
      COLORING: 'coloring',               // цвет полигона в зависимости от значения. MAP_CONST.COLOR.COLORING.GREEN_MIN (GREEN_MAX)

      MARKER: {
        KEY:  'marker',
      },

      LINE: {
        KEY:   'line',
      },

      POLYGON: {
        KEY: 'polygon',
      },
    },
  },


  // ZOOM: {
  //   KEY: 'zoom',                      // увеличение карты
  // },

  _LEGEND_COLOR_: 'legend_color',        // [], заполняется программой

};
