export const MAP_CONST = {
  POS: {                                  // центр и увеличение карты
    SEPARATOR: '_',
    DEFAULT:   '27.537231445312504_53.64138139745019_7',
    X:    27.537231445312504,
    Y:    53.64138139745019,
    ZOOM: 7,
  },

  CLASS: {
    SEL: 'sel',                           // название класса: выделено (pulse)
  //ANT: 'ant',                           // название класса: бегущая линия
    ICON: {
      TYPE:           'icon',             // иконка: тип
      PATH:           'img/markers/',     // иконка: путь к файлам иконок
      SEPARATOR:      '-',                // иконка: разделитель
      SVG:            'svg',              // иконка: svg
      SVG_STANDART:   'standart',         // иконка: svg стандарт
      SVG_ZOOM_BASE:  .5,                 // иконка: стартовый масштаб ВСЕХ иконок от размера 100х100
      SVG_ZOOM_START: 9.,                 // увеличение карты, при котором масштабируемая иконка начинает уменьшаться
      FILE:           'file',             // иконка: файл
      MDI:            'mdi',              // иконка: шрифт mdi
      FS:             'fs',               // иконка: шрифт fs
      PULSE:          'pulse',            // иконка: пульсирующая
    },
  },

  TYPE_GEOMETRY: {
    GC:        'GeometryCollection',
    POINT:     'Point',
    LINE:      'LineString',
    POLYGON:   'Polygon',
  },

  COLOR: {
    DEFAULT:            '#f00',           // цвет по умолчанию
    DEFAULT_STYLE_PATH: 'gray',           // цвет по умолчанию для стилизации (декорирования) фигур
    DEFAULT_STYLE_ICON: 'blue',           // цвет по умолчанию для иконок (в скрипте как правило определен другой цвет)
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
      BEGIN:     'FF0000',                // цвет: начальный
      END:       '00FF00',                // цвет: конечный
    },
  },
};


// ЭЛЕМЕНТЫ, ДОПОЛНЕННЫЕ К СТАНДАРТНЫМ
export const MAP_ITEM = {
//ZOOM: 'zoom',                           // увеличение карты
  COLOR: 'color',                         // цвет скрипта
  _LEGEND_COLOR_: 'legend_color',         // заполняется программой, []
  FC: {
    //TYPE: 'type',                       // не используется
    FEATURES: {
      IND:        'ind',                  // порядковый номер фигуры в fc.features
      PROPERTIES: {
        CLASS:        'class',            // key: класс для стилизации
        DATE:         'date',             // дата
        COLOR:        'color',            // цвет фигуры, приоритет над цветом скрипта
        VALUE:        'value',            // значение, которое определяет цвет полигона
        TEXT:         'text',             // надпись на маркере, пока что только для svg-маркеров
        ZOOM:         'zoom',             // масштабирование маркера: ['auto'], false, Numeric, пока что только для svg-маркеров
        ROTATE:       'rotate',           // поворот иконки, в градусах
        HINT:         'hint',             // всплывающая подсказка, НЕТ РЕАКТИВНОСТИ?
        SHADOW:       'shadow',           // иконки svg: false - отключить тень, 'red'
        TOP:          'top',              // иконки svg: true - поднять выше (важно при декорировании фигур несколькими иконками)
        _FILL_COLOR_: 'fill_color',       // заполняется программой, цвет заливки фигуры
        _SEL_:        'sel',              // заполняется программой, выделенный features[], true - выделено
      },
      GEOMETRY:  {
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
