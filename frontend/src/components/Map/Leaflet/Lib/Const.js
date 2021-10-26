export const MAP_CONST = {
  CLASS: {
    SEL: 'sel',                           // название класса: выделено (pulse)
  //ANT: 'ant',                           // название класса: бегущая линия
    ICON: {
      TYPE:      'icon',                  // иконка: тип
      PATH:      'img/markers/',          // иконка: путь к файлам иконок
      SEPARATOR: '-',                     // иконка: разделитель
      MDI:       'mdi',                   // иконка: шрифт mdi
      FS:        'fs',                    // иконка: шрифт fs
      FILE:      'file',                  // иконка: файл
      PULSE:     'pulse',                 // иконка: пульсирующая
    },
  },

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
//ZOOM: 'zoom',                           // увеличение карты
  COLOR: 'color',                         // копия в FC.STYLE._COLOR_
  _LEGEND_COLOR_: 'legend_color',         // [], заполняется программой
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
          KEY: 'class',                   // key: класс для стилизации
        },
        VALUE:   'value',                 // значение, которое определяет цвет полигона
        _COLOR_: 'color',                 // заполняется программой, цвет заливки фигуры
        _SEL_:   'sel',                   // заполняется программой, выделенный features[], true - выделено
      },
      GEOMETRY:  {
        KEY:         'geometry',
        TYPE:        'type',
        COORDINATES: 'coordinates',
        GEOMETRIES:  'geometries',        // вложенные геометрии MAP_ITEM.FC.FEATURES.GEOMETRY
      },
    },

    STYLE: {                              // стили маркеров и фигур
      KEY:     'style',
      COLORING: 'coloring',               // цвет полигона в зависимости от значения. MAP_CONST.COLOR.COLORING.GREEN_MIN (GREEN_MAX)
    },
  },
};
