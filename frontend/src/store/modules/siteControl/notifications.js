import axios from "@/plugins/axiosSettings"
import uuid from 'uuid'

export default {
  state: {
    notifications: [],
    loadStatus: false
  },
  getters: {
    notifications: state => state.notifications,
    loadStatus: state => state.loadStatus,
  },
  mutations: {
    changeLoadStatus: (state, status) => state.loadStatus = status,
    appendNotification: (state, notification) => state.notifications.unshift(notification),
    removeNotification: (state, notification) => {
      state.notifications.splice(state.notifications.findIndex(n => n.id === notification.id), 1)
    }
  },
  actions: {
    appendErrorAlert: ({ commit }, error = {}) => {
      const alert = new Notification({content: error.data.status, status: error.status})
      commit('appendNotification', alert)
      setTimeout(() => commit('removeNotification', alert), 5000)
    },
    getNotifications: ({ getters, commit }, config={}) => {
      const getNotifications = function () {
        const notifications = getters.notifications.filter(a => a.id_notification)
        const availableNotifications = Array.from(notifications, alert => alert.id_notification)
        axios.get('notifications/', Object.assign(config, {params: {list: availableNotifications}}))
        .then(r => r.data.map(n => {
          if(n.file) commit('changeFileStatus', n)
          commit('appendNotification', new Notification(n))
        }))
      }
      getNotifications()
      setInterval(() => getNotifications(), 10000)
    },
    setReadNotification: ({commit}, {notification, config = {}}) => {
      if (notification.id_notification)
        axios.get(`notifications/${notification.id_notification}/`, config)
      commit('removeNotification', notification)
    }
  }
}

class Notification {

  constructor(notification) {
    this.id = uuid()
    this.id_notification = notification.id_alert || null
    this.content = notification.content
    this.status = notification.status
    this.from = notification.from || "Система"
    this.time = notification.date_time || this.getDateTimeNow()
  }

  getDateTimeNow() {
    let m = new Date();
    return m.getFullYear() + "-" +
      ("0" + (m.getMonth()+1)).slice(-2) + "-" +
      ("0" + m.getDate()).slice(-2) + " " +
      ("0" + m.getHours()).slice(-2) + ":" +
      ("0" + m.getMinutes()).slice(-2) + ":" +
      ("0" + m.getSeconds()).slice(-2)
  }
}
