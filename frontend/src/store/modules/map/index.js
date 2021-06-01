
import {
  mapState,
  mapMutations,
} from 'vuex';

import {
  MAP_ITEM,
} from '@/components/Map/Leaflet/L.Const';

import {
  cook_set,
  cook_get_int,
  cook_get_bool,
  datesql_to_ts,
} from '@/plugins/sys';

import {
  MAP_DATA_MENU_TILES,
} from '@/store/modules/map/index_menu';

export default {
  state: {
    tiles: MAP_DATA_MENU_TILES,                      // источники плиток https://leaflet-extras.github.io/leaflet-providers/preview/

    range: {                                         // фильтр отображаемых данных по дате/времени
      show: cook_get_bool('MAP_RANGE_SHOW', false),  // создавать ли компонент (не путать с visible)
      sel_min:   0,                                  // выбранное минимальное значение, ts
      sel_max:   0,                                  // выбранное максимальное значение, ts
      limit_min: 0,                                  // минимально допустимое значение, ts
      limit_max: 0,                                  // максимально допустимое значение, ts
    },

    tile:       cook_get_int ('MAP_TILE',    0),     // (int) индекс активного источника плиток tiles[tile]
    cluster:    cook_get_bool('MAP_CLUSTER', true),  // (bool) допустима ли кластеризация (группировка) близко расположенных маркеров
    hint:       cook_get_bool('MAP_HINT',    false), // (bool) показывать ли всплывающие подсказки
    legend:     cook_get_bool('MAP_LEGEND',  true),  // (bool) показывать ли всплывающую легенду
    scale:      cook_get_bool('MAP_SCALE',   true),  // (bool) отображать ли шкалу масштаба
    measure:    cook_get_bool('MAP_MEASURE', false), // (bool) отображать ли рулетку
    logo:       cook_get_bool('MAP_LOGO',    false), // (bool) показывать ли логотип

    edit: {                                          // режим редактирования
      active: false,                                 // активация режима - не изменять в MAP_ACT_EDIT_ON
      mode:   {                                      // доступные фигуры, если не выбрано - доступно всё
        marker:  false,
        line:    false,
        polygon: false,
      },
      select: '',                                    // выбранный по умолчанию режим
      data:   undefined,                             // FeatureCollection РЕДАКТИРУЕМЫХ фигур и маркеров
    },
  },

  getters: {
    MAP_GET_KEY: (state, getters) => (ind) =>
      ind+'-'+
      getters.MAP_GET_RANGE_SEL        +'-'+
      getters.SCRIPT_GET_ITEM_MARKER (ind)+'-'+
      getters.SCRIPT_GET_ITEM_LINE   (ind)+'-'+
      // getters.SCRIPT_GET_ITEM_POLYGON(ind)+'-'+
      getters.SCRIPT_GET_ITEM_COLOR  (ind)+'-'+
      getters.SCRIPT_GET_ITEM_ICON   (ind)+'-'+
      getters.MAP_GET_CLUSTER          +'-'+
      getters.MAP_GET_HINT,

    MAP_GET_RANGE_SHOW:        (state) =>  state.range.show,
    MAP_GET_RANGE_SEL:         (state) => (state.range.show)?[state.range.sel_min,state.range.sel_max]:[0,0],
    MAP_GET_RANGE_MIN:         (state) =>  state.range.limit_min,
    MAP_GET_RANGE_MAX:         (state) =>  state.range.limit_max,
    MAP_GET_TILES:             (state) =>  state.tiles,
    MAP_GET_TILE:              (state) =>  state.tile,
    MAP_GET_TILE2:             (state) =>  state.tiles[state.tile],
    MAP_GET_CLUSTER:           (state) =>  state.cluster,
    MAP_GET_HINT:              (state) =>  state.hint,
    MAP_GET_LEGEND:            (state) =>  state.legend,
    MAP_GET_SCALE:             (state) =>  state.scale,
    MAP_GET_MEASURE:           (state) =>  state.measure,
    MAP_GET_LOGO:              (state) =>  state.logo,

    MAP_GET_EDIT_ACTIVE:       (state) =>  state.edit.active,
    MAP_GET_EDIT_MODE_MARKER:  (state) => (state.edit.mode.marker  || !(state.edit.mode.line   || state.edit.mode.polygon)),
    MAP_GET_EDIT_MODE_LINE:    (state) => (state.edit.mode.line    || !(state.edit.mode.marker || state.edit.mode.polygon)),
    MAP_GET_EDIT_MODE_POLYGON: (state) => (state.edit.mode.polygon || !(state.edit.mode.marker || state.edit.mode.line   )),
    MAP_GET_EDIT_SELECT:       (state) =>  state.edit.select,
    MAP_GET_EDIT_DATA:         (state) =>  state.edit.data,
  },


  mutations: {
    MAP_MUT_RANGE_SHOW:        (state, on)  => state.range.show = on,
    MAP_MUT_RANGE_LIMIT:       (state, lst) => { state.range.limit_min = lst[0]; state.range.limit_max = lst[1]; },
    MAP_MUT_RANGE_SEL:         (state, lst) => { state.range.sel_min   = lst[0]; state.range.sel_max   = lst[1]; },

    MAP_MUT_TILE:              (state, ind) => state.tile       = ind,
    MAP_MUT_CLUSTER:           (state, on)  => state.cluster    = on,
    MAP_MUT_HINT:              (state, on)  => state.hint       = on,
    MAP_MUT_LEGEND:            (state, on)  => state.legend     = on,
    MAP_MUT_SCALE:             (state, on)  => state.scale      = on,
    MAP_MUT_MEASURE:           (state, on)  => state.measure    = on,
    MAP_MUT_LOGO:              (state, on)  => state.logo       = on,
    MAP_MUT_EDIT:              (state, on)  => state.edit       = on,

    MAP_MUT_CENTER_X:          (state, val) => state.center_x   = val,
    MAP_MUT_CENTER_Y:          (state, val) => state.center_y   = val,
    MAP_MUT_ZOOM:              (state, val) => state.zoom       = val,

    MAP_MUT_EDIT_ON: (state, param={}) => {
      state.edit.active        = true;
      state.edit.mode.marker   = param.mode_marker  || false;
      state.edit.mode.line     = param.mode_line    || false;
      state.edit.mode.polygon  = param.mode_polygon || false;
      state.edit.select        = param.select       || '';
      state.edit.data          = param.data         || { "type": "FeatureCollection", "features": [], };
    },
    MAP_MUT_EDIT_DATA: (state, param={}) => {
      state.edit.data          = param.data         || { "type": "FeatureCollection", "features": [], };
    },
    MAP_MUT_EDIT_OFF: (state) => {
      state.edit.active        = false;
      state.edit.mode.marker   = false;
      state.edit.mode.line     = false;
      state.edit.mode.polygon  = false;
      state.edit.select        = '';
      // данные не удалять
      // state.edit.data          = undefined;
      // state.edit.data.features = {};
      // state.edit.data.type     = '';
    },
  },


  actions: {
    MAP_ACT_RANGE_SHOW:     ({commit}, param={}) => { commit('MAP_MUT_RANGE_SHOW', param.on);  cook_set('MAP_RANGE_SHOW', param.on ); },
    MAP_ACT_RANGE_SEL:      ({commit}, param={}) => { commit('MAP_MUT_RANGE_SEL',  param.lst); },
    MAP_ACT_TILE:           ({commit}, param={}) => { commit('MAP_MUT_TILE',       param.ind); cook_set('MAP_TILE',       param.ind); },
    MAP_ACT_CLUSTER:        ({commit}, param={}) => { commit('MAP_MUT_CLUSTER',    param.on);  cook_set('MAP_CLUSTER',    param.on ); },
    MAP_ACT_HINT:           ({commit}, param={}) => { commit('MAP_MUT_HINT',       param.on);  cook_set('MAP_HINT',       param.on ); },
    MAP_ACT_LEGEND:         ({commit}, param={}) => { commit('MAP_MUT_LEGEND',     param.on);  cook_set('MAP_LEGEND',     param.on ); },
    MAP_ACT_SCALE:          ({commit}, param={}) => { commit('MAP_MUT_SCALE',      param.on);  cook_set('MAP_SCALE',      param.on ); },
    MAP_ACT_MEASURE:        ({commit}, param={}) => { commit('MAP_MUT_MEASURE',    param.on);  cook_set('MAP_MEASURE',    param.on ); },
    MAP_ACT_LOGO:           ({commit}, param={}) => { commit('MAP_MUT_LOGO',       param.on);  cook_set('MAP_LOGO',       param.on ); },

    MAP_ACT_ITEM_ADD:       ({commit, dispatch}, param={}) => { commit('SCRIPT_MUT_ITEM_ADD',   param);    dispatch('MAP_ACT_RANGE_TS'); },
    MAP_ACT_ITEM_COLOR:     ({commit}, param={})           =>   commit('SCRIPT_MUT_ITEM_COLOR', param),
    MAP_ACT_ITEM_DEL:       ({commit, dispatch}, param={}) => { commit('SCRIPT_MUT_ITEM_DEL',   param.id); dispatch('MAP_ACT_RANGE_TS'); },

    // установить мин и макс даты
    MAP_ACT_RANGE_TS:       ({commit, dispatch, getters, rootGetters}) => {
      let limit_min = '';
      let limit_max = '';
      getters.SCRIPT_GET.forEach(function(layer){
        layer.fc.features.forEach(function(feature){
          let date = feature.properties.date;
          if (!date) return;
          if ((date < limit_min) || (limit_min == '')) limit_min=date;
          if ((date > limit_max) || (limit_max == '')) limit_max=date;
        }.bind(this));
      }.bind(this));
      limit_min = datesql_to_ts(limit_min);
      limit_max = datesql_to_ts(limit_max);
      commit('MAP_MUT_RANGE_LIMIT', [limit_min, limit_max]);

      // скорректирвать выбранный диапазон
      let sel     = getters.MAP_GET_RANGE_SEL;
      let sel_min = sel[0];
      let sel_max = sel[1];
      sel_min = ((limit_min <= sel_min) && ( sel_min <= limit_max))?sel_min:limit_min;
      sel_max = ((limit_min <= sel_max) && ( sel_max <= limit_max))?sel_max:limit_max;
      commit('MAP_MUT_RANGE_SEL', [sel_min, sel_max]);
    },

    MAP_ACT_EDIT_ON:        ({commit}, param={}) =>   commit('MAP_MUT_EDIT_ON',    param),
    MAP_ACT_EDIT_OFF:       ({commit})           =>   commit('MAP_MUT_EDIT_OFF'),
    MAP_ACT_EDIT_DATA:      ({commit}, param={}) =>   commit('MAP_MUT_EDIT_DATA',  { data: param.data, } ),
  },
}
