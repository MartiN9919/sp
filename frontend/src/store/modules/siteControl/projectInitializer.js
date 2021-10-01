import {getResponseAxios} from '@/plugins/axios_settings'

export default {
  state: {
    baseLists: [],
  },
  getters: {
    baseLists: state => { return state.baseLists },
    baseList: state => id => { return state.baseLists[id] },
  },
  mutations: {
    setBaseLists: (state, lists) => state.baseLists = lists,
  },
  actions: {
    async getBaseLists({commit}, config = {}) {
      await getResponseAxios('objects/lists/', config)
        .then(r => { commit('setBaseLists', r.data) })
        .catch(e => { return Promise.reject(e) })
      return Promise.resolve()
    },
  }
}
