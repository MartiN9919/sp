import { getResponseAxios, postResponseAxios, getResponseAxiosForCloseProblemWithAlertInLoginPage } from '@/plugins/axios_settings'

import router from '@/router'

export default {
  state: {
    userInformation: null,
    navigationDrawerStatusMap: false,
    navigationDrawerStatusReport: false,
    progressLinearStatus: false
  },
  getters: {
    progressLinearStatus: state => state.progressLinearStatus,
    userInformation: state => state.userInformation,
    navigationDrawerStatus: state => page => {
      if (page === 'Map') return state.navigationDrawerStatusMap
      if (page === 'Report') return state.navigationDrawerStatusReport
    }
  },
  mutations: {
    changeProgressLinearStatus: (state, status) => state.progressLinearStatus = status,
    changeNavigationDrawerStatus: (state) => {
      if (router.currentRoute.name === 'Map') state.navigationDrawerStatusMap = !state.navigationDrawerStatusMap
      if (router.currentRoute.name === 'Report') state.navigationDrawerStatusReport = !state.navigationDrawerStatusReport
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
