export class MAP_ITEM {

  static MARKER     = class {
    static NAME       = 'marker';
    static DEFAULT    = '';
    static COLOR      = 'color';
    static PULSE      = 'pulse';
    static FONT       = 'font';
  };

  static LINE       = class {
    static NAME       = 'line';
    static DEFAULT    = '';
    static ANT        = 'ant';          // бегущая линия === имени соответствующего класса
  };

  static POLYGON    = class {
    static NAME       = 'polygon';
    static DEFAULT    = '';
    static GREEN_MIN  = 'green_min';     // цвет полигона в зависимости от значения: зеленый(хуже)  -> красный(лучше) https://leafletjs.com/examples/choropleth/example.html
    static GREEN_MAX  = 'green_max';     // цвет полигона в зависимости от значения: зеленый(лучше) -> красный(хуже)
  };

  static ICON       = 'icon';
  static COLOR      = 'color';

  static FC         = 'result';
  static FC_COLOR   = 'color';
}
