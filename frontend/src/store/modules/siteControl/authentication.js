import { getResponseAxios, postResponseAxios } from '@/plugins/axios_settings'
import router from '@/router'

export default {
  state: {
    userInformation: null,
  },
  getters: {
    userInformation: state => state.userInformation,
  },
  mutations: {
    setUserInformation: (state, userInformation) => state.userInformation = userInformation,
  },
  actions: {
    authenticateUser ({ commit }, parameters = {}) {
      return postResponseAxios('auth/authentication/login/', parameters.userInformation, parameters.config)
        .then(response => {
          commit('setUserInformation', response.user)
          router.push({ name: 'Map' })
        })
        .catch(() => {})
    },
    logOutUser ({ commit, dispatch }, config = {}) {
      return getResponseAxios('auth/authentication/logout/', config)
        .then(() => router.go({ name: 'Login' }))
        .catch(() => {})
    },

    identifyUser ({ commit, dispatch, getters }, config = {}) {
      return getResponseAxios('auth/authorization/', config)
        .then(response => {
          commit('setUserInformation', response.user)
          if (!getters.baseLists.length) dispatch('getBaseLists')
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
