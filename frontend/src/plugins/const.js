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
    static BASE_PREFIX           = 'api';
    static AUTH = class {
      static LOGIN               = 'auth/authentication/login/'
      static LOGOUT              = 'auth/authentication/logout/'
      static IDENTIFY            = 'auth/authorization/'
    };
    static OBJ = class {
      static GET_LIST_OBJ        = 'objects/get_list_obj/';         // список объектов
      static GET_LIST_KEY_OBJ    = 'objects/get_list_key_obj/';     // список ключей-свойств объектов (классификатор)
      static GET_LIST_KEY_REL    = 'objects/get_list_key_rel/';     // список ключей-свойств связей объектов (классификатор)
      static GET_LISTS           = 'objects/get_lists/';            // списки возможных значений
      static GET_TILES           = 'objects/get_tiles/';            // списки источников тайлов
      static SET_RELATION        = 'objects/set_relation/';
      static GEOMETRY_SEARCH     = 'objects/geometry_search/';
      static GEOMETRY_FC         = 'objects/geometry_fc/';
      static OSM_SEARCH          = 'objects/osm_search/';
      static OSM_FC              = 'objects/osm_fc/';
    };
    static SCRIPT = class {
      static GET_LIST_SCRIPT     = 'script/get_list_script/';
      static GET_LIST_TRIGGER    = 'script/get_list_trigger/';
      static GET_LIST_TEMPLATE   = 'script/get_list_template/';
      static GET_TEMPLATE        = 'script/get_template/';
      static EXEC_MAP            = 'script/exec_map/';
      static EXEC_REPORT         = 'script/exec_report/';
    };
    static REPORT = class {
      static GET_LIST            = 'reports/get_list/';
      static CHECK_PROGRESS      = 'reports/check_progress/';
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
