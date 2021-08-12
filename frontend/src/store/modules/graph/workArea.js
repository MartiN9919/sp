import { postResponseAxios } from '@/plugins/axios_settings'

function getDateTime() {
  let dateTime = new Date()
  let time = dateTime.toLocaleTimeString('ru-RU').split(':')
  let date = dateTime.toLocaleDateString('ru-RU').split('.')
  return date[2] + '-' + date[1] + '-' + date[0] + ' ' + time[0] + ':' + time[1]
}

export default {
  state: {
    searchTreeGraph: null,
    foundObjects: null,
    editableObject: null,
  },
  getters: {
    searchTreeGraph: state => { return state.searchTreeGraph },
    foundObjects: state => { return state.foundObjects },
    editableObject: state => { return state.editableObject },
  },
  mutations: {
    setRootSearchTreeGraph: (state, rootObject) => { state.searchTreeGraph = rootObject },
    setActualRootSearchTree: (state, actual) => { state.searchTreeGraph.actual = actual },
    setNewItemSearchTreeGraph: (state, {item, newItem}) => {
      item.rels.unshift({
        object_id: newItem.id,
        actual: newItem.actual,
        request: null,
        rels: [],
        rel: {
          id: newItem.relId,
          value: newItem.relValue,
          date_time_start: newItem.relDateTimeStart,
          date_time_end: newItem.relDateTimeEnd,
        }
      })
    },
    changeItemSearchTreeGraph: (state, {item, newItem}) =>{
      item.object_id = newItem.id
      item.actual = newItem.actual
      item.rel.id = newItem.relId
      item.rel.value = newItem.relValue
      item.rel.date_time_start = newItem.relDateTimeStart
      item.rel.date_time_end = newItem.relDateTimeEnd
    },
    removeItemSearchTreeGraph: (state, {item, removeItem}) =>{
      item.rels.splice(item.rels.findIndex(i => i === removeItem), 1)
    },
    setFoundObjects: (state, objects) => { state.foundObjects = objects },
    setEditableObject: (state, object) => { state.editableObject = object },
    addNewParamEditableObject: (state, classifierId) => {
      let foundClassifier = state.editableObject.params.find(param => param.id === classifierId)
      foundClassifier.new_values.push({ value: null, date: getDateTime()})
    },
    deleteNewParamEditableObject: (state, playLoad) => {
      let foundClassifier = state.editableObject.params.find(param => param.id === playLoad.classifierId)
      if (foundClassifier) {
        let foundIndexParam = foundClassifier.new_values.findIndex(par => par === playLoad.param)
        if (foundIndexParam)
          foundClassifier.new_values.splice(foundIndexParam, 1)
      }
    }
  },
  actions: {
    saveEditableObject({ commit, getters }) {
      console.log(getters.editableObject)
    },
    deleteNewParamEditableObject({ commit }, playLoad) {
      commit('deleteNewParamEditableObject', playLoad)
    },
    addNewParamEditableObject({ commit }, classifierId ) {
      commit('addNewParamEditableObject', classifierId)
    },
    setEditableObject({ state, rootGetters, commit }, { object_id, rec_id=0, params=[] }) {
      let object = { object_id: object_id, rec_id: rec_id, params: params }
      if (params.length)
        object.params.concat(params)
      else
        for(let classifier of rootGetters.classifiersForObject(object_id))
          object.params.push({id: classifier.id, values: [], new_values: [] })
      commit('setEditableObject', object)
    },
    removeItemSearchTreeGraph({ commit }, {item, removeItem}) {
      commit('removeItemSearchTreeGraph', {item, removeItem})
    },
    changeItemSearchTreeGraph({ commit }, {item, newItem}) {
      commit('changeItemSearchTreeGraph', {item, newItem})
    },
    setNewItemSearchTreeGraph({ commit }, {item, newItem}) {
      commit('setNewItemSearchTreeGraph', {item, newItem})
    },
    setRootSearchTreeGraph({ state, commit }, {objectId, actual=false}) {
      if (state.searchTreeGraph?.object_id !== objectId) {
        let rootObject = { object_id: objectId, rel: null, request: null, actual: actual, rels: [] }
        localStorage.setItem('searchDefaultIdGraph', objectId)
        commit('setRootSearchTreeGraph', rootObject)
      } else {
        commit('setActualRootSearchTree', actual)
      }
    },
    setDefaultRootSearchTreeGraph({ dispatch, rootGetters }) {
      let searchDefaultId = parseInt(localStorage.getItem('searchDefaultIdGraph')) || rootGetters.listOfPrimaryObjects[0].id
      dispatch('setRootSearchTreeGraph', { objectId: searchDefaultId })
    },
    findObjectsOnServer({ commit, state }, config={}) {
      return postResponseAxios('objects/search', state.searchTreeGraph, config)
        .then(response => { commit('setFoundObjects', response.data) })
        .catch(error => {  })
    },
  }
}
