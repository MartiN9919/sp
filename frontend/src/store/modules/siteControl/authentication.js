import axios, {removeInterceptor, addInterceptor} from '@/plugins/axiosSettings'
import CONST from '@/plugins/const'
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
    authenticateUser ({commit}, {userInformation, config={}}) {
      axios.post(CONST.API.AUTH.LOGIN, userInformation, config).then(() => router.push({name: 'Map'}))
    },
    logOutUser ({ commit }, config = {}) {
      axios.get(CONST.API.AUTH.LOGOUT, config).finally(() => router.push({name: 'Login'}))
    },
    identifyUser ({getters, commit, dispatch}, config = {}) {
      removeInterceptor()
      return axios.get(CONST.API.AUTH.IDENTIFY, config)
        .then(async response => {
          if(!getters.userInformation) {
            commit('setUserInformation', response.data)
            await dispatch('initialization')
          }
        })
        .finally(() => addInterceptor())
    }
  }
}
