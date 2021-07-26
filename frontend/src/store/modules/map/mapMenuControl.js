export default {
  state: {
    toolsMapMenu: [
      { name: 'scriptsPage', icon: 'mdi-script-outline' },
      { name: 'dossierPage', icon: 'mdi-text-box-multiple-outline' },
    ],
    activeToolMap: null,
  },
  getters: {
    activeToolMap: state => { return state.activeToolMap },
    toolsMapMenu: state => { return state.toolsMapMenu },
  },
  mutations: {
    setActiveToolMap: (state, tool) => { state.activeToolMap = tool },
    setDefaultValueActiveToolMap: (state) => { state.activeToolMap = state.toolsMapMenu[0].name },
  },
  actions: {
    setActiveToolMap({ commit }, tool) { commit('setActiveToolMap', tool) },
    setDefaultValueActiveToolMap({ commit }) { commit('setDefaultValueActiveToolMap') },
  }
}