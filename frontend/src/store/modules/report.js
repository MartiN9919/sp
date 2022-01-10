import CONST from '@/plugins/const'
import axios from '@/plugins/axiosSettings'

export default {
  state: {
    reportsSlice: [],
    inProgressReports: [],
    reportTableOptions: {},
    numsTotalReports: 0,
    checkingReportStatusesInterval: null,
  },
  getters: {
    reportsSlice: state => state.reportsSlice,
    inProgressReports: state => state.inProgressReports,
    reportTableOptions: state => state.reportTableOptions,
    numsTotalReports: state => state.numsTotalReports,
    sliceParams: state => { return {size: state.reportTableOptions.itemsPerPage, offset: state.reportTableOptions.page} }
  },
  mutations: {
    setReportTableData: (state, response) => {
      if(response.hasOwnProperty('list'))
        state.reportsSlice = response.list
      if(response.hasOwnProperty('total'))
        state.numsTotalReports = response.total
      state.inProgressReports = response.in_progress
    },
    setInProgressReports: (state, inProgressReports) => state.inProgressReports = inProgressReports,
    setReportTableOptions: (state, reportTableOptions) => state.reportTableOptions = reportTableOptions,
    setCheckingReportStatusesInterval: (state, interval) => state.checkingReportStatusesInterval = interval,
    stopCheckingReportStatusesInterval: (state) => {
      if(state.checkingReportStatusesInterval) {
        clearInterval(state.checkingReportStatusesInterval)
        state.checkingReportStatusesInterval = null
      }
    },
  },
  actions: {
    setReportTableData({state, commit, dispatch}, response) {
      commit('setReportTableData', response)
      if(state.checkingReportStatusesInterval && response.in_progress.length === 0)
        commit('stopCheckingReportStatusesInterval')
      if(!state.checkingReportStatusesInterval && response.in_progress.length !== 0)
        dispatch('checkingReportStatuses')
    },
    getReportsSlice ({state, getters, dispatch}, config = {}) {
      config.params = getters.sliceParams
      return axios.get(CONST.API.REPORT.GET_LIST, config)
        .then(response => dispatch('setReportTableData', response.data))
        .catch(() => {})
    },
    setReportTableOptions ({commit, dispatch}, reportTableOptions) {
      commit('setReportTableOptions', reportTableOptions)
      dispatch('getReportsSlice')
    },
    checkingReportStatuses ({getters, commit, dispatch}, config={}) {
      const interval = setInterval(() => {
        config.params = Object.assign(getters.sliceParams, {list: getters.inProgressReports})
        axios.get(CONST.API.REPORT.CHECK_PROGRESS, config)
          .then(response => dispatch('setReportTableData', response.data))
      }, 1000)
      commit('setCheckingReportStatusesInterval', interval)
    },
    executeReportScript ({state, getters, commit, dispatch}, parameters = {}) {
      Object.assign(parameters.config, {params: getters.sliceParams})
      return axios.post(CONST.API.SCRIPT.EXEC_REPORT, parameters.request, parameters.config)
        .then(response => {
          commit('changeSelectedTreeViewItem', {})
          dispatch('setReportTableData', response.data)
        })
        .catch(() => {})
    }
  }
}
