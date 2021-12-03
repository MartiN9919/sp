import router from '@/router'
import UserSetting from '@/store/addition'

export default {
  state: {
    globalTooltipStatus: new UserSetting('globalTooltipStatus', true),
    globalNotificationStatus: new UserSetting('globalNotificationStatus', true),
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
    },
    appbarTabs: [
      { title: 'Карта', route: 'map', icon: 'mdi-map-search-outline' },
      { title: 'Граф', route: 'graph', icon: 'mdi-graph-outline' },
      { title: 'Отчеты', route: 'report', icon: 'mdi-file-document-multiple-outline' }
    ]
  },
  getters: {
    navigationDrawerStatus: state => page => state.navigationDrawer[page],
    activeTool: state => page => state.activeTool[page],
    toolsMenu: state => page => state.toolsMenu[page],
    globalTooltipStatus: state => state.globalTooltipStatus.value,
    globalNotificationStatus: state => state.globalNotificationStatus.value,
    appbarTabs: state => state.appbarTabs,
  },
  mutations: {
    setNavigationDrawerStatus: (state, status) => state.navigationDrawer[router.currentRoute.name] = status,
    setActiveTool: (state, tool) => state.activeTool[router.currentRoute.name] = tool,
    setGlobalTooltipStatus: (state, status) => state.globalTooltipStatus.value = status,
    setGlobalNotificationStatus: (state, status) => state.globalNotificationStatus.value = status,
  },
  actions: {
    setNavigationDrawerStatus: ({ getters, commit }, status) => commit('setNavigationDrawerStatus', status),
    setActiveTool({ commit }, tool) { commit('setActiveTool', tool) },
    setGlobalTooltipStatus({ commit }, status) {
      commit('setGlobalTooltipStatus', status)
    },
    setGlobalNotificationStatus({ commit, dispatch }, status) {
      status ? dispatch('getNotifications') : commit('stopNotificationInterval')
      commit('setGlobalNotificationStatus', status)
    },
  }
}