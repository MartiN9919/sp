import CONST  from '@/plugins/const'
import axios  from '@/plugins/axiosSettings'
import router from '@/router'
import _ from 'lodash'

export default {
  state: {
    scriptSearchMap: '',
    scriptSearchReport: '',
    treeViewItemsMap: [],
    treeViewItemsReport: [],
    selectedTreeViewItemMap: {},
    selectedTreeViewItemReport: {}
  },
  getters: {
    scriptSearch: state => page => {
      if (page === 'Map') return state.scriptSearchMap
      if (page === 'Report') return state.scriptSearchReport
    },
    selectedTreeViewItem: state => page => {
      if (page === 'Map') return state.selectedTreeViewItemMap
      if (page === 'Report') return state.selectedTreeViewItemReport
    },
    treeViewItems: state => page => {
      const filter = function (items, name) {
        let newItems = []
        for (let item of items) {
          if (item.hasOwnProperty('children')) {
            let temp = filter(item.children, name)
            if(temp.length) {
              item.children = temp
              newItems.push(item)
            }
          } else {
            if (item.name.toLowerCase().search(name.toLowerCase()) !== -1) {
              newItems.push(item)
            }
          }
        }
        return newItems
      }
      if (page === 'Map') return filter(_.cloneDeep(state.treeViewItemsMap), state.scriptSearchMap)
      if (page === 'Report') return filter(_.cloneDeep(state.treeViewItemsReport), state.scriptSearchReport)
    }
  },
  mutations: {
    setScriptSearch: (state, search) => {
      if (router.currentRoute.name === 'Map') state.scriptSearchMap = search
      if (router.currentRoute.name === 'Report') state.scriptSearchReport = search
    },
    setTreeViewItems: (state, treeViewItemsFromServer) => {
      if (router.currentRoute.name === 'Map') state.treeViewItemsMap = treeViewItemsFromServer
      if (router.currentRoute.name === 'Report') state.treeViewItemsReport = treeViewItemsFromServer
    },
    changeSelectedTreeViewItem: (state, selectedItem) => {
      if (router.currentRoute.name === 'Map') state.selectedTreeViewItemMap = selectedItem
      if (router.currentRoute.name === 'Report') state.selectedTreeViewItemReport = _.cloneDeep(selectedItem)
    }
  },
  actions: {
    setScriptSearch: ({commit}, search) => commit('setScriptSearch', search),

    changeSelectedTreeViewItem: ({ commit }, selectedItem = {}) => {
      if(!selectedItem.hasOwnProperty('refresh')) {
        selectedItem.refresh = Date.now()
      }
      commit('changeSelectedTreeViewItem', selectedItem)
    },

    getTreeViewItemsFromServer ({ commit }, config = {}) {
      return axios.get(CONST.API.SCRIPT.GET_LIST_SCRIPT, config)
        .then(response => commit('setTreeViewItems', response.data))
        .catch(() => {})
    }

  }
}
