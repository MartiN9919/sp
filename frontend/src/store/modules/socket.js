import { findArrayVerifiedAlerts } from './alerts'
import { WS_SERVER_IP } from '@/plugins/axios_settings'

export default {
  state: {
    socket: null
  },
  getters: {
    socket: state => state.socket
  },
  mutations: {
    connectSocket: (state, socket) => state.socket = socket,
    sendCookieAlerts: (state) => state.socket.send(JSON.stringify({ type: 'alerts', message: findArrayVerifiedAlerts() }))
  },
  actions: {
    connectSocket: ({ commit }) => {
      return new Promise((resolve, reject) => {
        const socket = new WebSocket(WS_SERVER_IP + 'channel/')
        socket.onopen = () => {
          commit('connectSocket', socket)
          resolve()
        }
      })
    },
    sendCookieAlerts: ({ commit }) => commit('sendCookieAlerts'),

    socketListener: ({ dispatch, state }) => {
      state.socket.onmessage = ({ data }) => {
        dispatch('processingReceivedNotifications', JSON.parse(data))
      }
    }
  }
}
