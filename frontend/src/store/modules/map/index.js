
import { MAP_ITEM }  from '@/components/Map/Leaflet/Lib/Const';
import { cook_set, cook_get_int, cook_get_bool, datesql_to_ts, hash_simple } from '@/plugins/sys';
import { MAP_DATA_MENU_TILES } from '@/store/modules/map/index_menu';

export default {
  state: {
    tiles: MAP_DATA_MENU_TILES,                        // источники плиток https://leaflet-extras.github.io/leaflet-providers/preview/

    range:      cook_get_bool('MAP_RANGE',   false),   // фильтр отображаемых данных по дате/времени
    tile:       cook_get_int ('MAP_TILE',    0),       // (int) индекс активного источника плиток tiles[tile]
    cluster:    cook_get_bool('MAP_CLUSTER', true),    // (bool) допустима ли кластеризация (группировка) близко расположенных маркеров
    hint:       cook_get_bool('MAP_HINT',    false),   // (bool) показывать ли всплывающие подсказки
    legend:     cook_get_bool('MAP_LEGEND',  true),    // (bool) показывать ли всплывающую легенду
    scale:      cook_get_bool('MAP_SCALE',   true),    // (bool) отображать ли шкалу масштаба
    measure:    cook_get_bool('MAP_MEASURE', false),   // (bool) отображать ли рулетку
    logo:       cook_get_bool('MAP_LOGO',    false),   // (bool) показывать ли логотип
    notify:     cook_get_bool('MAP_NOTIFY',  true),    // (bool) показывать ли заметки

    zoom:       0,                                     // текущее приближение
    edit:       undefined,                             // FeatureCollection РЕДАКТИРУЕМЫХ фигур и маркеров
    refresh:    0,                                     // ключ-признак принудительного обновления карты
  },

  getters: {
    MAP_GET_KEY: (state, getters) => (ind) => {
      let ret =
        ind+'-'+
        getters.MAP_GET_REFRESH                         +'-'+
        getters.SCRIPT_GET_ITEM_SEL                     +'-'+
        getters.SCRIPT_GET_ITEM_REFRESH            (ind)+'-'+
        JSON.stringify(getters.SCRIPT_GET_ITEM_FC_STYLE_MARKER(ind))+'-'+
        // getters.SCRIPT_GET_ITEM_FC_STYLE_LINE   (ind)+'-'+
        // getters.SCRIPT_GET_ITEM_FC_STYLE_POLYGON(ind)+'-'+
        getters.SCRIPT_GET_ITEM_COLOR              (ind)+'-'+
        getters.MAP_GET_RANGE                           +'-'+
        getters.MAP_GET_CLUSTER                         +'-'+
        getters.MAP_GET_HINT                            +'-'+
        getters.MAP_GET_ZOOM;
      return hash_simple(ret);
    },

    MAP_GET_RANGE:      (state) =>  state.range,
    MAP_GET_TILES:      (state) =>  state.tiles,
    MAP_GET_TILE:       (state) =>  state.tile,
    MAP_GET_TILE2:      (state) =>  state.tiles[state.tile],
    MAP_GET_CLUSTER:    (state) =>  state.cluster,
    MAP_GET_HINT:       (state) =>  state.hint,
    MAP_GET_LEGEND:     (state) =>  state.legend,
    MAP_GET_SCALE:      (state) =>  state.scale,
    MAP_GET_MEASURE:    (state) =>  state.measure,
    MAP_GET_LOGO:       (state) =>  state.logo,
    MAP_GET_NOTIFY:     (state) =>  state.notify,

    MAP_GET_ZOOM:       (state) =>  state.zoom,
    MAP_GET_EDIT:       (state) =>  state.edit,
    MAP_GET_REFRESH:    (state) =>  state.refresh,
  },


  mutations: {
    MAP_MUT_RANGE:      (state, on)   => state.range    = on,
    MAP_MUT_TILE:       (state, ind)  => state.tile     = ind,
    MAP_MUT_CLUSTER:    (state, on)   => state.cluster  = on,
    MAP_MUT_HINT:       (state, on)   => state.hint     = on,
    MAP_MUT_LEGEND:     (state, on)   => state.legend   = on,
    MAP_MUT_SCALE:      (state, on)   => state.scale    = on,
    MAP_MUT_MEASURE:    (state, on)   => state.measure  = on,
    MAP_MUT_LOGO:       (state, on)   => state.logo     = on,
    MAP_MUT_NOTIFY:     (state, on)   => state.notify   = on,

  //MAP_MUT_CENTER_X:   (state, val)  => state.center_x = val,
  //MAP_MUT_CENTER_Y:   (state, val)  => state.center_y = val,
    MAP_MUT_ZOOM:       (state, val)  => state.zoom     = val,
    MAP_MUT_EDIT:       (state, data) => state.edit     = data, // data || { "type": "FeatureCollection", "features": [], },
    MAP_MUT_REFRESH:    (state)       => state.refresh  = Math.random()*100000000000|0,
  },


  actions: {
    MAP_ACT_RANGE:      ({commit}, param={}) => { commit('MAP_MUT_RANGE',         param.on);  cook_set('MAP_RANGE',   param.on ); },
    MAP_ACT_TILE:       ({commit}, param={}) => { commit('MAP_MUT_TILE',          param.ind); cook_set('MAP_TILE',    param.ind); },
    MAP_ACT_CLUSTER:    ({commit}, param={}) => { commit('MAP_MUT_CLUSTER',       param.on);  cook_set('MAP_CLUSTER', param.on ); },
    MAP_ACT_HINT:       ({commit}, param={}) => { commit('MAP_MUT_HINT',          param.on);  cook_set('MAP_HINT',    param.on ); },
    MAP_ACT_LEGEND:     ({commit}, param={}) => { commit('MAP_MUT_LEGEND',        param.on);  cook_set('MAP_LEGEND',  param.on ); },
    MAP_ACT_SCALE:      ({commit}, param={}) => { commit('MAP_MUT_SCALE',         param.on);  cook_set('MAP_SCALE',   param.on ); },
    MAP_ACT_MEASURE:    ({commit}, param={}) => { commit('MAP_MUT_MEASURE',       param.on);  cook_set('MAP_MEASURE', param.on ); },
    MAP_ACT_LOGO:       ({commit}, param={}) => { commit('MAP_MUT_LOGO',          param.on);  cook_set('MAP_LOGO',    param.on ); },
    MAP_ACT_NOTIFY:     ({commit}, param={}) => { commit('MAP_MUT_NOTIFY',        param.on);  cook_set('MAP_NOTIFY',  param.on ); },

    MAP_ACT_ITEM_ADD:   ({commit}, param={}) =>   commit('SCRIPT_MUT_ITEM_ADD',   param),
    MAP_ACT_ITEM_COLOR: ({commit}, param={}) =>   commit('SCRIPT_MUT_ITEM_COLOR', param),
    MAP_ACT_ITEM_DEL:   ({commit}, param={}) =>   commit('SCRIPT_MUT_ITEM_DEL',   param.id),

    MAP_ACT_ZOOM:       ({commit}, zoom)     =>   commit('MAP_MUT_ZOOM',          zoom),
    MAP_ACT_EDIT:       ({commit}, param={}) =>   commit('MAP_MUT_EDIT',          param.data),
    MAP_ACT_REFRESH:    ({commit})           =>   commit('MAP_MUT_REFRESH'),
  },
}
