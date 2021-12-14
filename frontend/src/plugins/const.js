export default class CONST {
  static URL = class {
    static SERVER_IP = window.location.origin + '/';
  };

  static APP = class {
    static COLOR_OBJ         = '#00796B';
    static DISABLE           = '#616161'
    static LOGIN = class {
      static BACKGROUND = "#191122"
    }
    static TOOL_MENU = class {
      static WIDTH   = 56;
      static ACTIVE_COLOR = '#FFFFFF';
      static DISABLED_COLOR = '#9E9E9E';
    }
    //static COLOR_FONT        = '#fff';
  };


  static API = class {
    static BASE_PREFIX = 'api';
    static AUTH = class {
      static LOGIN = 'auth/authentication/login/'
      static LOGOUT = 'auth/authentication/logout/'
      static IDENTIFY = 'auth/authorization/'
    };
    static OBJ = class {
      static GEOMETRY_SEARCH = 'objects/geometry_search/';
      static GEOMETRY_FC     = 'objects/geometry_fc/';
      static OSM_SEARCH      = 'objects/osm_search/';
      static OSM_FC          = 'objects/osm_fc/';
    };
    static SCRIPT = class {
      static MAP           = 'script/execute_map/';
    };
  };


  static ICON = class {
    static OBJ = class {
      static GEOMETRY = 'mdi-vector-polygon';
    };
    static WEB = 'mdi-web';
  };


  static TREE = class {
    static ICON_SIZE         = undefined; // '20';
    static ICON_FOLDER_CLOSE = 'mdi-folder-outline';
    static ICON_FOLDER_OPEN  = 'mdi-folder-open-outline';

    static COLOR_DEFAULT     = undefined; // '#616161';
    static COLOR_SELECT      = CONST.APP.COLOR_OBJ;
  };
};
