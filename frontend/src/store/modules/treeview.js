import CONST  from '@/plugins/const'
import axios  from '@/plugins/axiosSettings'
import router from '@/router'

export default {
  state: {
    treeViewItemsMap: [],
    treeViewItemsReport: [],
    selectedTreeViewItemMap: {},
    selectedTreeViewItemReport: {}
  },
  getters: {
    selectedTreeViewItem: state => page => {
      if (page === 'Map') return state.selectedTreeViewItemMap
      if (page === 'Report') return state.selectedTreeViewItemReport
    },
    treeViewItems: state => page => {
      if (page === 'Map') return state.treeViewItemsMap
      if (page === 'Report') return state.treeViewItemsReport
    }
  },
  mutations: {
    setTreeViewItems: (state, treeViewItemsFromServer) => {
      if (router.currentRoute.name === 'Map') state.treeViewItemsMap = treeViewItemsFromServer
      if (router.currentRoute.name === 'Report') state.treeViewItemsReport = treeViewItemsFromServer
    },
    changeSelectedTreeViewItem: (state, selectedItem) => {
      if (router.currentRoute.name === 'Map') state.selectedTreeViewItemMap = selectedItem
      if (router.currentRoute.name === 'Report') state.selectedTreeViewItemReport = selectedItem
    }
  },
  actions: {
    changeSelectedTreeViewItem: ({ commit }, selectedItem = {}) => commit('changeSelectedTreeViewItem', selectedItem),

    getTreeViewItemsFromServer ({ commit }, config = {}) {
      return axios.get(CONST.API.SCRIPT.GET_LIST_SCRIPT, config)
        .then(response => commit('setTreeViewItems', response.data))
        .catch(() => {})
    }

  }
}
