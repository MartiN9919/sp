import {
  postResponseAxios,
  getResponseAxios,
  deleteResponseAxios,
  putResponseAxios,
} from '@/plugins/axios_settings'

import { MAP_CONST, MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { color_random } from '@/components/Map/Leaflet/Lib/LibColor';


export default {
  state: {
    templatesList: [],

    /**
     * state.selectedTemplateactiveAnalysts            - список активных скриптов
     * state.selectedTemplate.activeAnalysts[ind]
     *   id     (int)                                  - id скрипта (НЕ УНИКАЛЬНЫЙ)
     *   fc.id     (str, int)                          - уникальный идентификатор слоя, ПОКА НЕ НУЖЕН - НЕ УДАЛЯЛ
     */
    selectedTemplate: {
      title: '',
      activeAnalysts: [],
      passiveAnalysts: [],
    },


    /**
     * state.selectedFC[ind]                           - список указателей на объекты, соотнесенные с выделенными фигурами
     *   obj_id (int)                                  - тип объекта
     *   rec_id (str)                                  - id записи
     */
    selectedFC: [],
  },
  getters: {
    templatesList:                    state =>        state.templatesList,
    selectedTemplate:                 state =>        state.selectedTemplate,

    SCRIPT_GET:                       state =>        state.selectedTemplate.activeAnalysts,
    SCRIPT_GET_ITEM:                  state => ind => state.selectedTemplate.activeAnalysts[ind],
  //SCRIPT_GET_ITEM_FC_STYLE:         state => ind => state.selectedTemplate.activeAnalysts[ind].fc.style                 ?? {},
    SCRIPT_GET_ITEM_FC_STYLE_MARKER:  state => ind => state.selectedTemplate.activeAnalysts[ind].fc.style?.marker         ?? {},
    SCRIPT_GET_ITEM_FC_STYLE_LINE:    state => ind => state.selectedTemplate.activeAnalysts[ind].fc.style?.line           ?? {},
    SCRIPT_GET_ITEM_FC_STYLE_POLYGON: state => ind => state.selectedTemplate.activeAnalysts[ind].fc.style?.polygon        ?? {},
    SCRIPT_GET_ITEM_COLOR:            state => ind => state.selectedTemplate.activeAnalysts[ind][MAP_ITEM.COLOR]          ?? MAP_CONST.COLOR.DEFAULT,
    SCRIPT_GET_ITEM_LEGEND_COLOR:     state => ind => state.selectedTemplate.activeAnalysts[ind][MAP_ITEM._LEGEND_COLOR_] ?? [],
    SCRIPT_GET_ITEM_REFRESH:          state => ind => state.selectedTemplate.activeAnalysts[ind].refresh,
    SCRIPT_GET_ITEM_SEL:              state =>        JSON.stringify(state.selectedFC),
  },

  mutations: {
    changeSelectedTemplateTitle: (state, title) => state.selectedTemplate.title = title,
    addPassiveAnalysts: (state, analytics) => state.selectedTemplate.passiveAnalysts.push(analytics),

    changeTemplateTitle: (state) => {
      state.templatesList.find(
        template => template.id === parseInt(state.selectedTemplate.id)).title = state.selectedTemplate.title
    },

    changeColorActiveAnalysts: (state, parameters) => {
      let item = state.selectedTemplate.activeAnalysts.find(analytics => analytics === parameters.analytics);
      item[MAP_ITEM.COLOR] = parameters.color;
    },
    loadTemplatesList: (state, templates) => state.templatesList = templates,
    addSelectedTemplate: (state, template) => {
      state.selectedTemplate = template
      state.selectedTemplate.activeAnalysts = []
      state.selectedTemplate.passiveAnalysts = []
    },
    removeAnalytics: (state, analytics) => {
      let checkForAvailability = state.selectedTemplate.passiveAnalysts.indexOf(analytics)
      if (checkForAvailability !== -1) { state.selectedTemplate.passiveAnalysts.splice(checkForAvailability, 1) }
      checkForAvailability = state.selectedTemplate.activeAnalysts.indexOf(analytics)
      if (checkForAvailability !== -1) { state.selectedTemplate.activeAnalysts.splice(checkForAvailability, 1) }
    },
    saveSelectedTemplate: (state, templateId) => {
      state.selectedTemplate.id = templateId
      state.templatesList.push(state.selectedTemplate)
    },
    deleteSelectedTemplate: (state, templateId) => {
      state.selectedTemplate = { title: '', activeAnalysts: [], passiveAnalysts: [] }
      state.templatesList.splice(state.templatesList.findIndex(
        template => template.id === parseInt(templateId)), 1)
    },
    createNewTemplate: (state) => state.selectedTemplate = { title: '', activeAnalysts: [], passiveAnalysts: [] },


    SCRIPT_MUT_ITEM_ADD: (state, item) => {
      // item.color: нет или цвет неактивного скрипта -> выбрать цвет
      if ((item[MAP_ITEM.COLOR] === MAP_CONST.COLOR.SCRIPT_OFF) || (item[MAP_ITEM.COLOR] === undefined)) {
        // выбрать очередной цвет из MAP_CONST.COLOR.SCRIPT_BANK
        let color = undefined;
        for(let ind_bank=0; ind_bank<MAP_CONST.COLOR.SCRIPT_BANK.length; ind_bank++) {
          let item_bank = MAP_CONST.COLOR.SCRIPT_BANK[ind_bank];
          // item_bank не должен уже быть в активных скриптах
          for(let ind_script=0; ind_script<state.selectedTemplate.activeAnalysts.length; ind_script++) {
            let item_script = state.selectedTemplate.activeAnalysts[ind_script];
            // цвет из банка уже присвоен другому скрипту - прервать и взять другой цвет из банка
            if (item_script.color === item_bank) {
              item_bank = undefined;
              break;
            }
          }
          // нашли цвет -> запомнить
          if (item_bank) {
            color = item_bank;
            break;
          }
        }

        // все цвета заняты -> случайный цвет
        if (!color) { color  = color_random(); }
        // записать найденный цвет
        item[MAP_ITEM.COLOR] = color;
      }

      let item_copy = JSON.parse(JSON.stringify(item));        // deep copy
      item_copy.refresh = new Date().getTime();
      state.selectedTemplate.activeAnalysts.push(item_copy);
    },

    SCRIPT_MUT_ITEM_DEL:   (state, id)    => state.selectedTemplate.activeAnalysts.splice(id, 1),
    SCRIPT_MUT_ITEM_COLOR: (state, param) => {
      let item = state.selectedTemplate.activeAnalysts[param.ind];
      item[MAP_ITEM.COLOR] = param.color;
    },



    //
    // state.selectedFC
    //
    // установить/убрать выделение объекта на карте
    SCRIPT_MUT_SEL_SWITCH: (state, param)   => {    // param.obj_id, param.rec_id
      let ind_exist = undefined;
      for (let ind in state.selectedFC) {
        if ((state.selectedFC[ind].rec_id == param?.rec_id) && (state.selectedFC[ind].obj_id == param?.obj_id)) {
          ind_exist = ind;
          break;
        }
      }
      if (ind_exist) {
        state.selectedFC.splice(ind_exist, 1);
      } else {
        state.selectedFC.push({
          obj_id: param?.obj_id,
          rec_id: param?.rec_id,
        });
      }
    },
    SCRIPT_MUT_SEL_CLEAR: (state) => {
      state.selectedFC = [];
    },

    // пометить выделенные items (в скриптах)
    SCRIPT_MAP_SEL_MARK: (state) => {
      // просмотреть все активные скрипты
      let sel_items;
      for (let item_script of state.selectedTemplate.activeAnalysts) {
        for (let item of item_script.fc.features) {
          sel_items = state.selectedFC.find(sel_item => ((item.rec_id == sel_item.rec_id) && (item.obj_id == sel_item.obj_id)));
          if (sel_items) { item.properties[MAP_ITEM.FC.FEATURES.PROPERTIES._SEL_] = true; }
          else { if (item.properties[MAP_ITEM.FC.FEATURES.PROPERTIES._SEL_]) { delete item.properties[MAP_ITEM.FC.FEATURES.PROPERTIES._SEL_]; } }
        }
      }
    },
  },


  actions: {
    addPassiveAnalysts: ({ commit }, analytics = {}) => commit('addPassiveAnalysts', analytics),

    removeAnalytics: ({ commit, dispatch }, analytics = {}) => { commit('removeAnalytics', analytics); dispatch('MAP_ACT_RANGE_TS'); },

    changeColorActiveAnalysts: ({ commit }, parameters = {}) => commit('changeColorActiveAnalysts', parameters),

    changeSelectedTemplateTitle: ({ commit }, parameters = '') => commit('changeSelectedTemplateTitle', parameters),

    createNewTemplate: ({ commit }) => commit('createNewTemplate'),

    executeMapScript ({ commit, dispatch }, parameters = {}) {
      return postResponseAxios(this._vm.$CONST.API.SCRIPT.MAP, parameters.request, parameters.config)
        .then(response => {
          commit('removeAnalytics', parameters.request);
          parameters.request[MAP_ITEM.FC.KEY] = response.data;
          commit('SCRIPT_MUT_ITEM_ADD', parameters.request);
          commit('changeSelectedTreeViewItem', {});
          dispatch('MAP_ACT_RANGE_TS');
        })
        .catch(() => {})
    },


    // добавить/удалить выделение
    SCRIPT_ACT_SEL_SET({ commit }, param) {         // param.obj_id, param.rec_id, param.ctrl
      if (!param?.ctrl) { commit('SCRIPT_MUT_SEL_CLEAR'); }
      commit('SCRIPT_MUT_SEL_SWITCH', param);
      commit('SCRIPT_MAP_SEL_MARK');
    },
    SCRIPT_ACT_SEL_CLEAR({ commit }) {
      commit('SCRIPT_MUT_SEL_CLEAR');
      commit('SCRIPT_MAP_SEL_MARK');
    },


    getTemplatesList ({ commit, dispatch }, config = {}) {
      return getResponseAxios('script/templates/', config)
        .then(response => { { commit('loadTemplatesList', response.data); dispatch('MAP_ACT_RANGE_TS'); } })
        .catch(() => {})
    },
    saveSelectedTemplate ({ state, commit }, parameters = {}) {
      return postResponseAxios('script/template/', parameters.selectedTemplate, parameters.config)
        .then(response => { commit('saveSelectedTemplate', response.data) })
        .catch(() => {})
    },
    putSelectedTemplate ({ state, commit }, parameters = {}) {
      return putResponseAxios('script/template/', parameters.selectedTemplate, parameters.config)
        .then(response => { commit('changeTemplateTitle') })
        .catch(() => {})
    },
    getSelectedTemplate ({ state, commit, dispatch }, config = {}) {
      return getResponseAxios('script/template/', config)
        .then(response => {
          const activeAnalysts = response.data.activeAnalysts
          const passiveAnalysts = response.data.passiveAnalysts
          commit('changeSelectedTreeViewItem', {})
          commit('addSelectedTemplate', response.data)
          for (const script of activeAnalysts) { dispatch('executeMapScript', { request: script, script: script, config: {} }) }
          for (const script of passiveAnalysts) { commit('addPassiveAnalysts', script) }
        })
        .catch(() => {})
    },
    deleteSelectedTemplate ({ commit, dispatch }, config = {}) {
      return deleteResponseAxios('script/template/', config)
        .then(response => {
          commit('deleteSelectedTemplate', config.params.template_id)
          commit('changeSelectedTreeViewItem', {})
          dispatch('MAP_ACT_RANGE_TS')
        })
        .catch(() => {})
    }
  },
}
