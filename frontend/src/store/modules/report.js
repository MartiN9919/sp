import axios from '@/plugins/axiosSettings'

export default {
  state: {
    listFiles: []
  },
  getters: {
    listFiles: state => state.listFiles
  },
  mutations: {
    setListFiles: (state, files) => state.listFiles = files,
    addFileToList: (state, file) => state.listFiles.unshift(file),
    changeFileStatus: (state, alert) => {
      if (state.listFiles.length) {
        if (alert.status === 'information') state.listFiles.find(file => file.id === alert.file).status = 'done'
        if (alert.status === 'error') state.listFiles.find(file => file.id === alert.file).status = 'error'
      }
    }
  },
  actions: {
    getListFiles ({ commit }, config = {}) {
      return axios.get('reports/list/', config)
        .then(response => {
          commit('setListFiles', response.data.list)
          return response
        })
        .catch(() => {})
    },
    executeReportScript ({ commit }, parameters = {}) {
      return axios.post('script/execute_report/', parameters.request, parameters.config)
        .then(response => {
          commit('changeSelectedTreeViewItem', {})
          commit('addFileToList', response.data)
        })
        .catch(() => {})
    }
  }
}
