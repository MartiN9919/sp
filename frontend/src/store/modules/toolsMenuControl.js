import router from '@/router'

export default {
  state: {
    toolsMenuMap: [
      { name: 'scriptsPage', icon: 'mdi-script-outline' },
      { name: 'dossierPage', icon: 'mdi-text-box-multiple-outline' },
    ],
    activeToolMap: null,

    toolsMenuGraph: [
      { name: 'searchPage', icon: 'mdi-magnify' },
      { name: 'addPage', icon: 'mdi-plus' },
      { name: 'dossierPage', icon: 'mdi-text-box-multiple-outline' },
    ],
    activeToolGraph: null,
  },
  getters: {
    activeTool: state => page => {
      if (page === 'Map')  return state.activeToolMap
      if (page === 'Graph')  return state.activeToolGraph
    },
    toolsMenu: state => page => {
      if (page === 'Map')  return state.toolsMenuMap
      if (page === 'Graph')  return state.toolsMenuGraph
    },
  },
  mutations: {
    setActiveTool: (state, tool) => {
      if (router.currentRoute.name === 'Map')  state.activeToolMap = tool
      if (router.currentRoute.name === 'Graph')  state.activeToolGraph = tool
    },
    setDefaultValueActiveTool: (state) => {
      if (router.currentRoute.name === 'Map')  state.activeToolMap = state.toolsMenuMap[0].name
      if (router.currentRoute.name === 'Graph')  state.activeToolGraph = state.toolsMenuGraph[0].name
    },
  },
  actions: {
    setActiveTool({ commit }, tool) { commit('setActiveTool', tool) },
    setDefaultValueActiveTool({ commit }) { commit('setDefaultValueActiveTool') },
  }
}