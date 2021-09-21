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
        { name: 'scriptsPage', icon: 'mdi-script-outline', disabled: false },
        { name: 'dossierPage', icon: 'mdi-text-box-multiple-outline', disabled: false },
      ],
      Graph: [
        { name: 'searchPage', icon: 'mdi-cloud-search-outline', disabled: false },
        { name: 'createPage', icon: 'mdi-text-box-plus-outline', disabled: false },
        { name: 'createRelationPage', icon: 'mdi-link-variant-plus', disabled: true },
        { name: 'dossierPage', icon: 'mdi-file-document-outline', disabled: true },
        { name: 'settingsPage', icon: 'mdi-cog-outline', disabled: false },
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
    setDefaultValueActiveTool: (state) => state.activeTool[router.currentRoute.name] = state.toolsMenu[router.currentRoute.name][0].name,
    setToolStatus: (state, playLoad) => state.toolsMenu[router.currentRoute.name].find(t => t.name === playLoad.tool).disabled = playLoad.status,
  },
  actions: {
    setNavigationDrawerStatus: ({ getters, commit }, status) => commit('setNavigationDrawerStatus', status),
    setDefaultValueActiveTool({ commit }) { commit('setDefaultValueActiveTool') },
    setToolStatus({ commit }, playLoad) { console.log(playLoad); commit('setToolStatus', playLoad) },
    setActiveTool({ commit }, tool) { commit('setActiveTool', tool) },
  }
}