import { getResponseAxios, postResponseAxios } from '@/plugins/axios_settings'

import router from '@/router'

export default {
  state: {
    userInformation: null,
    navigationDrawerStatusMap: false,
    navigationDrawerStatusReport: false,
    navigationDrawerStatusGraph: false,
    loadStatus: false
  },
  getters: {
    loadStatus: state => state.loadStatus,
    userInformation: state => state.userInformation,
    navigationDrawerStatus: state => page => {
      if (page === 'Map') return state.navigationDrawerStatusMap
      if (page === 'Report') return state.navigationDrawerStatusReport
      if (page === 'Graph') return state.navigationDrawerStatusGraph
    }
  },
  mutations: {
    changeLoadStatus: (state, status) => state.loadStatus = status,
    changeNavigationDrawerStatus: (state) => {
      if (router.currentRoute.name === 'Map') state.navigationDrawerStatusMap = !state.navigationDrawerStatusMap
      if (router.currentRoute.name === 'Report') state.navigationDrawerStatusReport = !state.navigationDrawerStatusReport
      if (router.currentRoute.name === 'Graph') state.navigationDrawerStatusGraph = !state.navigationDrawerStatusGraph
    },
    setUserInformation: (state, userInformation) => state.userInformation = userInformation
  },
  actions: {
    changeNavigationDrawerStatus: ({ commit }) => commit('changeNavigationDrawerStatus'),

    authenticateUser ({ commit }, parameters = {}) {
      return postResponseAxios('auth/authentication/login/', parameters.userInformation, parameters.config)
        .then(response => { commit('setUserInformation', response.user); router.push({ name: 'Map' }) })
        .catch(() => {})
    },

    deauthenticateUser ({ commit, dispatch }, config = {}) {
      return getResponseAxios('auth/authentication/logout/', config)
        .then(() => router.go({ name: 'Login' }))
        .catch(() => {})
    },

    identifyUser ({ commit, dispatch, getters }, config = {}) {
      return getResponseAxios('auth/authorization/', config)
        .then(response => {
          commit('setUserInformation', response.user)
          if (!getters.socket) {
            dispatch('connectSocket').then(() => {
              dispatch('socketListener')
              dispatch('sendCookieAlerts')
            })
          }
          return Promise.resolve()
        })
        .catch(error => { return Promise.reject(error) })
    }
  }
}
