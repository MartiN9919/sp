import router from '@/router'

function getDefaultSettings(identifier) {
  if(!localStorage.getItem(identifier))
    localStorage.setItem(identifier, 'true')
  return localStorage.getItem(identifier) === 'true'
}

export default {
  state: {
    globalTooltipStatus: getDefaultSettings('globalTooltipStatus'),
    globalNotificationStatus: getDefaultSettings('globalNotificationStatus'),
    navigationDrawer: {
      Map: false,
      Report: false,
      Graph: false,
    },
    activeTool: {
      Map: null,
      Graph: null,
    },
    toolsMenu: {
      Map: [
        { name: 'scriptsPage', icon: 'mdi-script-outline', description: 'Скрипты' },
        { name: 'dossierPage', icon: 'mdi-text-box-multiple-outline', description: 'Описание объекта' },
      ],
      Graph: [
        { name: 'searchPage', icon: 'mdi-cloud-search-outline', description: 'Поиск по объектам' },
        { name: 'searchRelationPage', icon: 'mdi-vector-link', description: 'Поиск по связям' },
        { name: 'createObjectPage', icon: 'mdi-text-box-plus-outline', description: 'Создание объекта' },
        { name: 'createRelationPage', icon: 'mdi-link-variant-plus', description: 'Создание связи' },
        { name: 'settingsPage', icon: 'mdi-cog-outline', description: 'Общие настройки графа' },
      ]
    }
  },
  getters: {
    navigationDrawerStatus: state => page => state.navigationDrawer[page],
    activeTool: state => page => state.activeTool[page],
    toolsMenu: state => page => state.toolsMenu[page],
    globalTooltipStatus: state => state.globalTooltipStatus,
    globalNotificationStatus: state => state.globalNotificationStatus,
  },
  mutations: {
    setNavigationDrawerStatus: (state, status) => state.navigationDrawer[router.currentRoute.name] = status,
    setActiveTool: (state, tool) => state.activeTool[router.currentRoute.name] = tool,
    setGlobalTooltipStatus: (state, status) => state.globalTooltipStatus = status,
    setGlobalNotificationStatus: (state, status) => state.globalNotificationStatus = status,
  },
  actions: {
    setNavigationDrawerStatus: ({ getters, commit }, status) => commit('setNavigationDrawerStatus', status),
    setActiveTool({ commit }, tool) { commit('setActiveTool', tool) },
    setGlobalTooltipStatus({ commit }, status) {
      localStorage.setItem('globalTooltipStatus', status)
      commit('setGlobalTooltipStatus', status)
    },
    setGlobalNotificationStatus({ commit, dispatch }, status) {
      if(status) 
        dispatch('getNotifications')
      else
        commit('stopNotificationInterval')
      localStorage.setItem('globalNotificationStatus', status)
      commit('setGlobalNotificationStatus', status)
    },
  }
}