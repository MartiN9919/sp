import axios from 'axios'
import store from '../store/index'
import CONST from '@/plugins/const'

export const WS_SERVER_IP = 'ws://' + CONST.URL.SERVER_IP
export const HTTP_SERVER_IP = 'http://' + CONST.URL.SERVER_IP

const http = axios.create({
  withCredentials: true,
  baseURL: HTTP_SERVER_IP + 'api',
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  headers: {
    'Content-Type': 'application/json;charset=utf-8',
    'X-Frame-Options': 'DENY'
  }
})

export function checkErrorStatusCode(statusCode){
  const CRITICAL_STATUS_CODE = [401, ]
  return CRITICAL_STATUS_CODE.includes(statusCode)
}

function processingErrorResponse(error){
  store.commit('changeLoadStatus', false)
  if(error.response === undefined)
    store.dispatch('appendErrorAlert', { status: 'no connect' })
  else if(!checkErrorStatusCode(error.response.status))
    store.dispatch('appendErrorAlert', error.response)
  return Promise.reject(error)
}

function processingSuccessResponse(response){
  store.commit('changeLoadStatus', false)
  return response.data
}

export async function getResponseAxios (url, config = {}) {
  store.commit('changeLoadStatus', true)
  return await http.get(url, config)
    .then((response) => { return processingSuccessResponse(response) })
    .catch(error => { return processingErrorResponse(error) })
}

export async function postResponseAxios (url, data, config = {}) {
  store.commit('changeLoadStatus', true)
  return await http.post(url, data, config)
    .then((response) => { return processingSuccessResponse(response) })
    .catch(error => { return processingErrorResponse(error) })
}

export async function putResponseAxios (url, data, config = {}) {
  store.commit('changeLoadStatus', true)
  return await http.put(url, data, config)
    .then((response) => { return processingSuccessResponse(response) })
    .catch(error => { return processingErrorResponse(error) })
}

export async function deleteResponseAxios (url, config = {}) {
  store.commit('changeLoadStatus', true)
  return await http.delete(url, config)
    .then((response) => { return processingSuccessResponse(response) })
    .catch(error => { return processingErrorResponse(error) })
}

export default () => {
  return http
}