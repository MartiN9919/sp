
class SYS {
    static DELAY_ACTION      = 1500;                // Задержка после выбора пользователя, мсек. 
}


// AJAX 
class AJ {                                          // в начале '/': абсолютный путь 
    static ALERT_SET         = '/aj/alert/set/';
    static ALERT_GET         = '/aj/alert/get/';
    
    static SCRIPT_LIST       = '/aj/script/list/';       
    static SCRIPT_EXEC       = '/aj/script/exec/';       
    static SCRIPT_NAME       = class {
        static OBJ_LIST         = 'obj_list';
        static KEY_LIST         = 'key_list';
        
        static REL_TO_GEO       = 'rel_to_geo';
        
        static GEOMETRY_TREE    = 'geometry_tree';
        static GEOMETRY_GET     = 'geometry_get';
        static GEOMETRY_SET     = 'geometry_set';

        static TEST             = 'test';
    };

    static EL_FIND           = '/aj/el/find/';
    static PANORAMA_GET      = '/aj/panorama/get/';
    static POLYGON_GET_OSM   = '/aj/polygon/get/osm/';
}

// ключи классификатора
class KEY {
    static TEST_GEO_COLOR    = 'test_geo_color';    // temp
}

// ключи FeaturesCollection.Properties 
class FC_PROPERTIES {
    static IND = class {
        static VAL = 0;
        static DAT = 1;
    };
    static NAME              = 'name';
    static COLOR             = 'color';
}
