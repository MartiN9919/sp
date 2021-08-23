import { postResponseAxios } from '@/plugins/axios_settings'
import _ from 'lodash'

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
    editableObjects: null,
  },
  getters: {
    searchTreeGraph: state => { return state.searchTreeGraph },
    foundObjects: state => { return state.foundObjects },
    editableObjects: state => { return state.editableObjects },
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
    setEditableObjects: (state, object) => { state.editableObjects = [object] },
    addEditableObjects: (state, object) => { state.editableObjects.push(object) },
    addNewParamEditableObject: (state, {classifierId, positionEditableObject}) => {
      let classifier = state.editableObjects[positionEditableObject].params.find(param => param.id === classifierId)
      classifier.new_values.push({ value: null, date: getDateTime()})
    },
    deleteNewParamEditableObject: (state, {classifierId, param, positionEditableObject}) => {
      let foundClassifier = state.editableObjects[positionEditableObject].params.find(param => param.id === classifierId)
      if (foundClassifier) {
        let foundIndexParam = foundClassifier.new_values.findIndex(par => par === param)
        if (foundIndexParam !== -1)
          foundClassifier.new_values.splice(foundIndexParam, 1)
      }
    }
  },
  actions: {
    saveEditableObject({ dispatch, rootGetters }, {object, force}) {
      let request = {object_id: object.object_id, rec_id: object.rec_id, params: [], force: force}
      if('rec_id_old' in object)
        request.rec_id_old = object.rec_id_old
      for (let param of object.params) {
        if (param.new_values.length) {
          let classifier = rootGetters.classifierObject({objectId: request.object_id, classifierId: param.id})
          for (let valueObject of param.new_values)
            if (classifier.list_id) {
              let value = classifier.list_id.find(item => item.id === valueObject.value).value
              request.params.push({id: param.id, value: value, date: valueObject.date})
            } else request.params.push({id: param.id, value: valueObject.value, date: valueObject.date})
        }
      }
      return postResponseAxios('objects/object', request, {})
        .then(response => {
          switch (response.data.status) {
            case 1:
              let object = response.data.object
              dispatch('setEditableObject', {
                object_id: object.object_id,
                rec_id: object.rec_id,
                params: object.params
              })
              break
            case 2:
              for(let object of response.data.objects)
                dispatch('addEditableObject', {
                  object_id: object.object_id,
                  rec_id: object.rec_id,
                  params: object.params
                })
              break
          }
        })
        .catch(error => {})
    },
    setEditableObject({ rootGetters, commit }, { object_id, rec_id=0, params=[] }) {
      let object = {object_id: object_id, rec_id: rec_id, params: params}
      if (object.params.length)
        for (let param of object.params)
          param.new_values = []
      for(let classifier of rootGetters.classifiersForObject(object.object_id))
        if(!object.params.find(param => param.id === classifier.id))
          object.params.push({id: classifier.id, values: [], new_values: []})
      commit('setEditableObjects', object)
    },
    addEditableObject({ getters, commit }, { object_id, rec_id=0, params=[] }) {
      let deepCopyParams = _.cloneDeep(getters.editableObjects[0].params)
      let newObject = {
        object_id: object_id,
        rec_id: rec_id,
        rec_id_old: getters.editableObjects[0].rec_id,
        params: deepCopyParams
      }
      for (let param of newObject.params) {
        let findParam = params.find(p => p.id === param.id)
        if (findParam)
          param.values = findParam.values.concat(param.values).sort(function (a, b) { return (a.date < b.date) ? 1 : -1 })
      }
      commit('addEditableObjects', newObject)
    },
    deleteNewParamEditableObject({ commit }, playLoad) {
      commit('deleteNewParamEditableObject', playLoad)
    },
    addNewParamEditableObject({ commit }, {classifierId, positionEditableObject} ) {
      commit('addNewParamEditableObject', {classifierId, positionEditableObject})
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
