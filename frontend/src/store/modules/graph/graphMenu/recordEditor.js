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
    addNewParamEditableRelation: (state, relationId) => state.editableRelation.addParam(relationId),
    setEditableObjects: (state, object) => state.editableObjects = [object],
    resetEditableObjects: (state) => state.editableObjects = [state.editableObjects[0]],
    addEditableObjects: (state, object) => state.editableObjects.push(object),
    addNewParamEditableObject: (state, {classifierId, positionEditableObject, value=null}) => {
      state.editableObjects[positionEditableObject].addParam(classifierId, value)
    },
    deleteNewParamEditableObject: (state, {classifierId, param, positionEditableObject}) => {
      state.editableObjects[positionEditableObject].deleteParam(classifierId, param)
    }
  },
  actions: {
    setEditableRelation({getters, commit}, relation) {
      commit('setEditableRelation', new DataBaseRelation(
        relation.object_id1,
        relation.object_id2,
        relation.rec_id1,
        relation.rec_id2,
        getters.relations(relation)?.relations
      ))
    },
    addNewParamEditableRelation({commit}, relationId) {
      commit('addNewParamEditableRelation', relationId)
    },
    async getObjectFromServer({commit, dispatch}, config = {}) {
      return await getResponseAxios('objects/object/', config)
        .then(r => { return Promise.resolve(r.data) })
        .catch(e => { return Promise.reject(e) })
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
    addNewParamEditableObject({commit}, {classifierId, positionEditableObject}) {
      commit('addNewParamEditableObject', {classifierId, positionEditableObject})
    },
    deleteNewParamEditableObject({commit}, playLoad) {
      commit('deleteNewParamEditableObject', playLoad)
    },
    async saveEditableObject({getters, dispatch}, positionObject) {
      return await postResponseAxios('objects/object', getters.editableObjects[positionObject].getRequestStructure(), {})
        .then(r => {
          if(r.data.hasOwnProperty('object'))
            dispatch('setEditableObject', r.data.object)
          if(r.data.hasOwnProperty('objects'))
            dispatch('addEditableObjects', r.data.objects)
          return Promise.resolve(r.data)
        })
        .catch(e => { return Promise.reject(e) })
    }
  }
}


class DataBaseRelation {
  constructor(object_id_1, object_id_2, rec_id_1, rec_id_2, params=[]) {
    this.o1 = store.getters.baseObject(object_id_1)
    this.o2 = store.getters.baseObject(object_id_2)
    this.o1Object = store.getters.choosingObject(rec_id_1)
    this.o2Object = store.getters.choosingObject(rec_id_2)
    this.params = []
    for(let param of params)
      this.params.push(new ParamObject(store.getters.baseRelation(param.id), param.values))
    for(let relation of store.getters.baseRelations({f_id: object_id_1, s_id: object_id_2}))
      if(!this.params.find(c => c.classifier.id === relation.id))
        this.params.push(new ParamObject(store.getters.baseRelation(relation.id)))
  }

  addParam(relationId) {
    let foundRelation = this.params.find(param => param.classifier.id === relationId)
    foundRelation.new_values.push(new ValueParam())
  }
}


class DataBaseObject {
  constructor(object_id, rec_id=0, title='', params=[], recIdOld=null) {
    this.object = store.getters.baseObject(object_id)
    this.recId = rec_id
    this.title = title
    this.params = []
    if(recIdOld)
      this.recIdOld = recIdOld
    for(let param of params)
      this.params.push(new ParamObject(store.getters.baseClassifier(param.id), param.values))
    for(let classifier of store.getters.baseClassifiers(object_id))
      if(!this.params.find(c => c.classifier.id === classifier.id))
        this.params.push(new ParamObject(store.getters.baseClassifier(classifier.id)))
  }

  addParam(classifierId, value) {
    let foundClassifier = this.params.find(param => param.classifier.id === classifierId)
    foundClassifier.new_values.push(new ValueParam(value))
  }

  deleteParam(classifierId, param) {
    let foundClassifier = this.params.find(param => param.classifier.id === classifierId)
    foundClassifier.new_values.splice(foundClassifier.new_values.findIndex(par => par === param), 1)
  }

  getRequestStructure() {
    let params = []
    for(let param of this.params)
      for (let newValue of param.new_values) {
        let value = param.classifier.list ? param.classifier.list.find(item => item.id === newValue.value).value : newValue.value
        params.push({id: param.classifier.id, value: value, date: newValue.date})
      }
    let request = {
      rec_id: this.recId,
      object_id: this.object.id,
      force: store.getters.editableObjects.length > 1,
      params: params,
    }
    if(this.hasOwnProperty('recIdOld'))
      request.rec_id_old = this.recIdOld
    return request
  }

  concatParams(concatObject) {
    for(let param of concatObject.params) {
      let findParam = this.params.find(p => p.classifier.id === param.classifier.id)
      findParam.values = findParam.values.concat(_.cloneDeep(param.values))
      findParam.new_values = findParam.new_values.concat(_.cloneDeep(param.new_values))
    }
  }
}

class ParamObject {
  constructor(id, values=[], newValues=[]) {
    this.classifier = id
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