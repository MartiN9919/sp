import { getResponseAxios, postResponseAxios } from '@/plugins/axios_settings'
import store from "@/store"
import _ from 'lodash'

export default {
  state: {
    editableRelation: null,
    editableObjects: null,
  },
  getters: {
    editableRelation: state => { return state.editableRelation },
    editableObjects: state => { return state.editableObjects },
  },
  mutations: {
    setEditableRelation: (state, relation) => state.editableRelation = relation,
    addNewParamEditableRelation: (state, id) => state.editableRelation.addParam(id),
    deleteNewParamEditableRelation: (state, {id, param}) => state.editableRelation.deleteParam(id, param),

    setEditableObjects: (state, object) => {
      state.editableObjects = [object]
    },
    resetEditableObjects: (state) => state.editableObjects = [state.editableObjects[0]],
    addEditableObjects: (state, object) => state.editableObjects.push(object),
    addNewParamEditableObject: (state, {id, position}) => {
      state.editableObjects[position].addParam(id)
    },
    deleteNewParamEditableObject: (state, {id, param, position}) => {
      state.editableObjects[position].deleteParam(id, param)
    }
  },
  actions: {
    setEditableRelation({getters, commit}, relation) {
      commit('setEditableRelation', new DataBaseRelation(
        relation.o1, relation.o2, relation.r1, relation.r2,
        getters.relations(relation)?.relations
      ))
    },
    addNewParamEditableRelation({commit}, relationId) {
      commit('addNewParamEditableRelation', relationId)
    },
    deleteNewParamEditableRelation({commit}, playLoad) {
      commit('deleteNewParamEditableRelation', playLoad)
    },
    setEditableObject({commit}, object) {
      commit('setEditableObjects', new DataBaseObject(object.object_id, object.rec_id, object.title, object.params))
    },
    addEditableObjects({getters, commit}, objects) {
      commit('resetEditableObjects')
      for(let object of objects) {
        let zeroObject = getters.editableObjects[0]
        let newObject = new DataBaseObject(object.object_id, object.rec_id, object.title, object.params, zeroObject.recId)
        newObject.concatParams(zeroObject)
        commit('addEditableObjects', newObject)
      }
    },
    addNewParamEditableObject({commit}, playLoad) {
      commit('addNewParamEditableObject', playLoad)
    },
    deleteNewParamEditableObject({commit}, playLoad) {
      commit('deleteNewParamEditableObject', playLoad)
    },
    async getObjectFromServer({commit, dispatch}, config = {}) {
      config.headers = {'set-cookie': JSON.stringify(getTriggers(config.params.object_id))}
      return await getResponseAxios('objects/object/', config)
        .then(r => { return Promise.resolve(r.data) })
        .catch(e => { return Promise.reject(e) })
    },
    async getRelationFromServer({commit, dispatch}, {params, config}) {
      return await postResponseAxios('objects/object_relation/', params, config)
        .then(r => {
          for(let relation of r.data) {
            let object = {o1: params.object_id, r1: params.rec_id, o2: relation.object_id, r2: relation.rec_id}
            dispatch('addChoosingRelation', {object: object, relations: relation.relations})
          }
          return Promise.resolve(r.data)
        })
        .catch(e => { return Promise.reject(e) })

    },
    async saveEditableObject({getters, dispatch}, positionObject) {
      return await postResponseAxios('objects/object',
        getters.editableObjects[positionObject].getRequestStructure(),
        {headers: {
          'Content-Type': 'multipart/form-data',
          'set-cookie': JSON.stringify(getTriggers(getters.editableObjects[positionObject].object.id))
        }}
      )
        .then(r => {
          if(r.data.hasOwnProperty('object')) {
            dispatch('setEditableObject', r.data.object)
            // dispatch('addChoosingObject', r.data.object)
          }
          if(r.data.hasOwnProperty('objects'))
            dispatch('addEditableObjects', r.data.objects)
          return Promise.resolve(r.data)
        })
        .catch(e => { return Promise.reject(e) })
    },
    async saveEditableRelation({getters, dispatch}) {
      let relation = getters.editableRelation
      return await postResponseAxios('objects/relation', relation.getRequestStructure(), {})
        .then(r => {
          let object = {o1: relation.o1.id, r1: relation.o1Object.rec_id, o2: relation.o2.id, r2: relation.o2Object.rec_id}
          dispatch('addChoosingRelation', {object: object, relations: r.data})
          dispatch('setEditableRelation', Object.assign({}, object, r.data))
          return Promise.resolve(r.data)
        })
        .catch(e => { return Promise.reject(e) })
    }
  }
}

function getTriggers(id) {
  let cookies = []
  for (let [name, value] of Object.entries(localStorage))
    if (name.startsWith('trigger') && name.split('_')[1] === id.toString())
      cookies.push({id: name.split('_')[2], variables: JSON.parse(value)})
  return cookies
}

class BaseDbObject {
  constructor(getter, baseObjects, params, recIdOld=null) {
    this.params = []
    if(recIdOld)
      this.recIdOld = recIdOld
    for(let param of params)
      this.params.push(new ParamObject(getter(param.id), param.values))
    for(let object of baseObjects)
      if(!this.params.find(c => c.baseParam.id === object.id))
        this.params.push(new ParamObject(getter(object.id)))
  }

  addParam(id) {
    this.params.find(param => param.baseParam.id === id).new_values.push(new ValueParam())
  }

  deleteParam(id, param) {
    let foundParam = this.params.find(param => param.baseParam.id === id)
    foundParam.new_values.splice(foundParam.new_values.findIndex(par => par === param), 1)
  }
}


class DataBaseRelation extends BaseDbObject {
  constructor(object_id_1, object_id_2, rec_id_1, rec_id_2, params=[]) {
    super(store.getters.baseRelation, store.getters.baseRelations({f_id: object_id_1, s_id: object_id_2}), params)
    this.o1 = store.getters.baseObject(object_id_1)
    this.o2 = store.getters.baseObject(object_id_2)
    this.o1Object = store.getters.choosingObject(rec_id_1)
    this.o2Object = store.getters.choosingObject(rec_id_2)
  }

  getRequestStructure() {
    let params = []
    for(let param of this.params)
      for (let newValue of param.new_values) {
        let value = newValue.value
        params.push({id: param.baseParam.id, value: value, date: newValue.date})
      }
    return {
      object_1_id: this.o1.id,
      object_2_id: this.o2.id,
      rec_1_id: this.o1Object.rec_id,
      rec_2_id: this.o2Object.rec_id,
      params: params,
    }
  }
}


class DataBaseObject extends BaseDbObject {
  constructor(object_id, rec_id=0, title='', params=[], recIdOld=null) {
    super(store.getters.baseClassifier, store.getters.baseClassifiers(object_id), params, recIdOld)
    this.object = store.getters.baseObject(object_id)
    this.recId = rec_id
    this.title = title
  }

  getRequestStructure() {
    let formData = new FormData()
    let params = []
    for(let param of this.params) {
      for (let newValue of param.new_values) {
        if(param.baseParam.type !== "file_photo") {
          let value = newValue.value
          params.push({value: value, date: newValue.date})
        } else {
          params.push({value: newValue.value.file.name, date: newValue.date})
          formData.append(newValue.value.file.name, newValue.value.file)
        }
      }
    }
    let request = {
      rec_id: this.recId,
      object_id: this.object.id,
      force: store.getters.editableObjects.length > 1,
      params: params,
    }
    if(this.hasOwnProperty('recIdOld'))
      request.rec_id_old = this.recIdOld
    formData.append('data', JSON.stringify(request))
    return formData
  }

  concatParams(concatObject) {
    for(let param of concatObject.params) {
      let findParam = this.params.find(p => p.baseParam.id === param.baseParam.id)
      findParam.values = findParam.values.concat(_.cloneDeep(param.values))
      findParam.new_values = findParam.new_values.concat(_.cloneDeep(param.new_values))
    }
  }
}

class ParamObject {
  constructor(baseParam, values=[], newValues=[]) {
    this.baseParam = baseParam
    this.new_values = newValues
    this.values = []
    for(let v of values)
      this.values.push(new ValueParam(v.value, v.date))
  }
}

class ValueParam {
  constructor(value=null, date=this.getDateTime()) {
    this.value = value
    this.date = date
  }

  getDateTime() {
    let dateTime = new Date()
    let time = dateTime.toLocaleTimeString('ru-RU').split(':')
    let date = dateTime.toLocaleDateString('ru-RU').split('.')
    return date[2] + '-' + date[1] + '-' + date[0] + ' ' + time[0] + ':' + time[1]
  }
}