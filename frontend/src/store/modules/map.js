import { postResponseAxios, getResponseAxios, deleteResponseAxios, putResponseAxios } from '@/plugins/axios_settings'

export default {
  state: {
    templatesList: [],
    selectedTemplate: {
      title: '',
      activeAnalysts: [],
      passiveAnalysts: []
    }
  },
  getters: {
    templatesList: state => state.templatesList,
    selectedTemplate: state => state.selectedTemplate
  },
  mutations: {
    changeSelectedTemplateTitle: (state, title) => state.selectedTemplate.title = title,
    addPassiveAnalysts: (state, analytics) => state.selectedTemplate.passiveAnalysts.push(analytics),

    changeTemplateTitle: (state) => {
      state.templatesList.find(
        template => template.id === parseInt(state.selectedTemplate.id)).title = state.selectedTemplate.title
    },

    changeColorActiveAnalysts: (state, parameters) => {
      state.selectedTemplate.activeAnalysts.find(
        analytics => analytics === parameters.analytics).color = parameters.color
    },
    loadTemplatesList: (state, templates) => state.templatesList = templates,
    addSelectedTemplate: (state, template) => {
      state.selectedTemplate = template
      state.selectedTemplate.activeAnalysts = []
      state.selectedTemplate.passiveAnalysts = []
    },
    addActiveAnalysts: (state, playLoad) => {
      playLoad.selectedScript.result = playLoad.result
      if (playLoad.selectedScript.color === '#696969FF') { playLoad.selectedScript.color = '#FFA500FF' }
      state.selectedTemplate.activeAnalysts.push(playLoad.selectedScript)
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
    createNewTemplate: (state) => state.selectedTemplate = { title: '', activeAnalysts: [], passiveAnalysts: [] }
  },
  actions: {
    addPassiveAnalysts: ({ commit }, analytics = {}) => commit('addPassiveAnalysts', analytics),

    removeAnalytics: ({ commit }, analytics = {}) => commit('removeAnalytics', analytics),

    changeColorActiveAnalysts: ({ commit }, parameters = {}) => commit('changeColorActiveAnalysts', parameters),

    changeSelectedTemplateTitle: ({ commit }, parameters = '') => commit('changeSelectedTemplateTitle', parameters),

    createNewTemplate: ({ commit }) => commit('createNewTemplate'),

    executeMapScript ({ commit }, parameters = {}) {
      return postResponseAxios('script/execute_map/', parameters.request, parameters.config)
        .then(response => {
          commit('removeAnalytics', parameters.request)
          commit('addActiveAnalysts', {
            selectedScript: parameters.request,
            result: response.data
          })
          commit('changeSelectedTreeViewItem', {})
        })
        .catch(() => {})
    },
    getTemplatesList ({ commit }, config = {}) {
      return getResponseAxios('script/templates/', config)
        .then(response => { { commit('loadTemplatesList', response.data) } })
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
    deleteSelectedTemplate ({ commit }, config = {}) {
      return deleteResponseAxios('script/template/', config)
        .then(response => {
          commit('deleteSelectedTemplate', config.params.template_id)
          commit('changeSelectedTreeViewItem', {})
        })
        .catch(() => {})
    }
  }
}
