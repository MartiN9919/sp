import axios from "@/plugins/axiosSettings"
import uuid from 'uuid'

export default {
  state: {
    notificationTypes: {
      information: {
        color: '#43A047',
        text: 'Информация',
        icon: 'mdi-check'
      },
      warning: {
        color: '#039BE5',
        text: 'Предупреждение',
        icon: 'mdi-alert-circle-outline'
      },
      error: {
        color: '#8E24AA',
        text: 'Ошибка',
        icon: 'mdi-alert-rhombus-outline'
      },
      default: {
        color: '#D32F2F',
        text: 'Ошибка системы',
        icon: 'mdi-alert-rhombus-outline'
      },
    },
    notifications: [],
    loadStatus: false,
    notificationInterval: null,
  },
  getters: {
    notificationType: state => n => state.notificationTypes[n.status] || state.notificationTypes.default,
    notifications: state => state.notifications,
    loadStatus: state => state.loadStatus,
  },
  mutations: {
    changeLoadStatus: (state, status) => state.loadStatus = status,
    setNotificationInterval: (state, interval) => state.notificationInterval = interval,
    stopNotificationInterval: (state) => {
      if(state.notificationInterval) {
        clearInterval(state.notificationInterval)
        state.notificationInterval = null
      }
    },
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
      const interval = setInterval(() => getNotifications(), 10000)
      commit('setNotificationInterval', interval)
    },
    setReadNotification: ({commit}, {notification, config = {}}) => {
      if (notification.id_notification)
        axios.get(`notifications/${notification.id_notification}/`, config)
      commit('removeNotification', notification)
    },
    addNotification: ({commit}, notification) => {
      if (notification?.status === undefined) notification.status = 'information'
      const notify = new Notification(notification)
      commit('appendNotification', notify)
      notification?.timeout && setTimeout(() => commit('removeNotification', notify), notification?.timeout*1000)
    }
  }
}

class Notification {
  /**
   * @param: {
   *   "content": String: -'Текст уведомления',
   *   "status": String: { variant: ["information", "warning", "error"]},
   *   "id_alert": Number: { default: null } -id в базе,
   *   "from": String: { default: 'Система' } -Отправитель,
   *   "date_time": String: { default: getDateTimeNow() } -'Дата создания уведомления',
   * }
   */
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
