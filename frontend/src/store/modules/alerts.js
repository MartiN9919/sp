export function findArrayVerifiedAlerts () {
  for (const cookie_string of decodeURIComponent(document.cookie).split('; ')) {
    const cookie = cookie_string.split('=')
    if (cookie[0] === 'verified_alerts') return JSON.parse(cookie[1])
  }
  return []
}

function deleteVerifiedAlert (index) {
  const verifiedAlert = findArrayVerifiedAlerts()
  verifiedAlert.splice(index, 1)
  document.cookie = 'verified_alerts=' + JSON.stringify(verifiedAlert)
}

function addVerifiedAlert (idAlert) {
  const verifiedAlert = findArrayVerifiedAlerts()
  verifiedAlert.push(idAlert)
  document.cookie = 'verified_alerts=' + JSON.stringify(verifiedAlert) + '; SameSite="Secure";'
}

export default {
  state: {
    alertsList: []
  },
  getters: {
    alertsList: state => state.alertsList
  },
  mutations: {
    removeAlertFromList: (state, alert) => state.alertsList.splice(state.alertsList.indexOf(alert), 1),
    removeVerifiedAlert: (state, alertId) => {
      const indexVerifiedAlerts = findArrayVerifiedAlerts().indexOf(parseInt(alertId))
      if (indexVerifiedAlerts !== -1) deleteVerifiedAlert(indexVerifiedAlerts)
    },
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

    processingReceivedNotifications: ({ commit, rootState }, response) => {
      for (const removeAlertId of response.to_remove) { commit('removeVerifiedAlert', removeAlertId) }
      for (const alert of response.notifications) {
        if (alert.file) {
          if (rootState.report.listFiles.length) { commit('changeFileStatus', {fileId: alert.file, status: alert.status}) }
        }
        commit('appendAlert', alert)
      }
    }
  }
}
