export default class CONST {
  static URL = class {
    static SERVER_IP = '127.0.0.1:8000/';
    // static SERVER_IP = '192.168.56.1:8002/';
  };


  static APP = class {
    static COLOR_OBJ         = '#00796B';
    //static COLOR_FONT        = '#fff';
  };


  static API = class {
    static BASE_PREFIX = 'api';
    static OBJ = class {
      static GEOMETRY_TREE = 'objects/geometry_tree/';
      static GEOMETRY      = 'objects/geometry/';
      static OSM_SEARCH    = 'objects/osm_search/';
      static OSM_FC        = 'objects/osm_fc/';
    };
    static SCRIPT = class {
      static MAP           = 'script/execute_map/';
    };
  };


  static TREE = class {
    static ICON_SIZE         = undefined; // '20';
    static ICON_FOLDER_CLOSE = 'mdi-folder-outline';
    static ICON_FOLDER_OPEN  = 'mdi-folder-open-outline';

    static COLOR_DEFAULT     = undefined; // '#616161';
    static COLOR_SELECT      = CONST.APP.COLOR_OBJ;
  };
};
