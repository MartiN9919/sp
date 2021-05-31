import axios from 'axios'
import store from '../store/index'

const http = axios.create({
  withCredentials: true,
  baseURL: 'http://127.0.0.1:8000/api',
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  headers: {
    'Content-Type': 'application/json;charset=utf-8',
    'X-Frame-Options': 'DENY'
  }
})

export async function getResponseAxios (url, config = {}) {
  store.commit('changeProgressLinearStatus', true)
  return await http.get(url, config)
    .then((response) => {
      store.commit('changeProgressLinearStatus', false)
      return response.data
    })
    .catch(error => {
      console.log(error)
      store.commit('changeProgressLinearStatus', false)
      //store.dispatch('appendErrorAlert', error.response)
      return Promise.reject()
    })
}

export async function postResponseAxios (url, data, config = {}) {
  store.commit('changeProgressLinearStatus', true)
  return await http.post(url, data, config)
    .then((response) => {
      store.commit('changeProgressLinearStatus', false)
      return response.data
    })
    .catch(error => {
      store.commit('changeProgressLinearStatus', false)
      store.dispatch('appendErrorAlert', error.response)
      return Promise.reject()
    })
}

export async function putResponseAxios (url, data, config = {}) {
  store.commit('changeProgressLinearStatus', true)
  return await http.put(url, data, config)
    .then((response) => {
      store.commit('changeProgressLinearStatus', false)
      return response.data
    })
    .catch(error => {
      store.commit('changeProgressLinearStatus', false)
      store.dispatch('appendErrorAlert', error.response)
      return Promise.reject()
    })
}

export async function deleteResponseAxios (url, config = {}) {
  store.commit('changeProgressLinearStatus', true)
  return await http.delete(url, config)
    .then((response) => {
      store.commit('changeProgressLinearStatus', false)
      return response.data
    })
    .catch(error => {
      store.commit('changeProgressLinearStatus', false)
      store.dispatch('appendErrorAlert', error.response)
      return Promise.reject()
    })
}

export default () => {
  return http
}
