import router from '@/router'

export default {
  state: {
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
    navigationDrawerStatus: state => page => { return state.navigationDrawer[page] },
    activeTool: state => page => { return state.activeTool[page] },
    toolsMenu: state => page => { return state.toolsMenu[page] },
  },
  mutations: {
    setNavigationDrawerStatus: (state, status) => state.navigationDrawer[router.currentRoute.name] = status,
    setActiveTool: (state, tool) => state.activeTool[router.currentRoute.name] = tool,
  },
  actions: {
    setNavigationDrawerStatus: ({ getters, commit }, status) => commit('setNavigationDrawerStatus', status),
    setActiveTool({ commit }, tool) { commit('setActiveTool', tool) },
  }
}