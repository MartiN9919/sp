import axios from "@/plugins/axiosSettings";

export default {
  state: {
    alertsList: [],
    loadStatus: false
  },
  getters: {
    alertsList: state => state.alertsList,
    loadStatus: state => state.loadStatus,
  },
  mutations: {
    changeLoadStatus: (state, status) => state.loadStatus = status,
    removeAlertFromList: (state, alert) => state.alertsList.splice(state.alertsList.indexOf(alert), 1),
    appendAlert: (state, alert) => {
      alert.id = Date.now().toString() + state.alertsList.length.toString()
      state.alertsList.unshift(alert)
    }
  },
  actions: {
    appendErrorAlert: ({ commit }, error = {}) => commit('appendAlert', error),
    removeAlertFromList: ({ commit }, alert = {}) => {
      if ('id_alert' in alert) addVerifiedAlert(alert.id_alert)
      commit('removeAlertFromList', alert)
    },
    getNotifications: ({ commit, rootState }, conf={}) => {
      setInterval(() =>
        axios.get('notifications/list', Object.assign(conf, { params: {list: []}}))
      , 20000);

    }
  }
}
