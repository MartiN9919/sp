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
  return `${CONST.API.BASE_PREFIX}/files/condense_image_download/files/${generateFileLink(objectId, recId, fileName)}`
}

export function getDownloadFileLink(objectId, recId, fileName) {
  return `${CONST.API.BASE_PREFIX}/files/download/files/${generateFileLink(objectId, recId, fileName)}`
}

export function getDownloadReportLink(fileId) {
  return `${HTTP_SERVER_IP + CONST.API.BASE_PREFIX}/files/download_report/${fileId}`
}

function generateFileLink(objectId, recId, fileName) {
  return `${objectId}/${recId}/${fileName}`
}

export function checkErrorStatusCode(statusCode){
  const CRITICAL_STATUS_CODE = [401, ]
  return CRITICAL_STATUS_CODE.includes(statusCode)
}

http.interceptors.request.use(function (config) {
  store.commit('changeLoadStatus', true)
  return config
}, function (error) {
  return Promise.reject(error)
})

http.interceptors.response.use(function (response) {
  store.commit('changeLoadStatus', false)
  return response
}, function (error) {
  store.commit('changeLoadStatus', false)
  if(error.response === undefined)
    store.dispatch('appendErrorAlert', { status: 'no connect' })
  else if(!checkErrorStatusCode(error.response.status))
    store.dispatch('appendErrorAlert', error.response)
  return Promise.reject(error)
})

export default http
