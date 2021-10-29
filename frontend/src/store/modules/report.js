import axios from '@/plugins/axios_settings'

export default {
  state: {
    listFiles: []
  },
  getters: {
    listFiles: state => state.listFiles
  },
  mutations: {
    addListFiles: (state, file) => {
      state.listFiles.unshift(file)
    },
    changeFileStatus: (state, alert) => {
      if (alert.status === 501) state.listFiles.find(file => file.id === alert.fileId).status = 'done'
      if (alert.status === 503) state.listFiles.find(file => file.id === alert.fileId).status = 'error'
    }
  },
  actions: {
    getListFiles ({ commit }, config = {}) {
      return axios.get('reports/list/', config)
        .then(response => { for (const file of response.data) commit('addListFiles', file) })
        .catch(() => {})
    },
    executeReportScript ({ commit }, parameters = {}) {
      return axios.post('script/execute_report/', parameters.request, parameters.config)
        .then(response => {
          commit('changeSelectedTreeViewItem', {})
          commit('addListFiles', response.data)
        })
        .catch(() => {})
    }
  }
}
