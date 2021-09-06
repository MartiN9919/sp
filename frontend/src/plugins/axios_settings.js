import axios from 'axios'
import store from '../store/index'
import CONST from '@/plugins/const'

export const WS_SERVER_IP = 'ws://' + CONST.URL.SERVER_IP
export const HTTP_SERVER_IP = 'http://' + CONST.URL.SERVER_IP

const http = axios.create({
  withCredentials: true,
  baseURL: HTTP_SERVER_IP + CONST.API.BASE_PREFIX,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  headers: {
    'Content-Type': 'application/json;charset=utf-8',
    'X-Frame-Options': 'DENY'
  }
})

export function getFileLink(objectId, recId, fileName) {
  return `${CONST.API.BASE_PREFIX}/files/download_condense_image/open_files/${generateFileLink(objectId, recId, fileName)}`
}

export function getDownloadFileLink(objectId, recId, fileName) {
  return `${CONST.API.BASE_PREFIX}/files/download/open_files/${generateFileLink(objectId, recId, fileName)}`
}

function generateFileLink(objectId, recId, fileName) {
  return `${objectId}/${recId}/${fileName}`
}

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
