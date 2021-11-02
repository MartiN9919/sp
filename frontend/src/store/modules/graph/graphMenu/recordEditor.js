import axios from '@/plugins/axios_settings'
import {getTriggers} from "@/store/modules/graph/graphNodes"
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
    setEditableRelation: (state, {relation, document}) => state.editableRelation = {relation, document},
    addNewParamEditableRelation: (state, id) => state.editableRelation.relation.addParam(id),
    deleteNewParamEditableRelation: (state, {id, param}) => state.editableRelation.relation.deleteParam(id, param),

    setEditableObjects: (state, object) => state.editableObjects = [object],
    resetEditableObjects: (state) => state.editableObjects = [state.editableObjects[0]],
    addEditableObjects: (state, object) => state.editableObjects.push(object),
    addNewParamEditableObject: (state, {id, position}) => state.editableObjects[position].addParam(id),
    deleteNewParamEditableObject: (state, {id, param, position}) => state.editableObjects[position].deleteParam(id, param)
  },
  actions: {
    setEditableRelation({getters, commit}, {relations, document}) {
      let edge = getters.graphRelations.find(
        e => [e.relation.o1.id, e.relation.o2.id].every(r => Array.from(relations, o => o.id).includes(r)))
      commit('setEditableRelation', {
        relation: _.cloneDeep(edge?.relation) || new DataBaseRelation(...relations),
        document: document
      })
    },
    addNewParamEditableRelation({commit}, relationId) {
      commit('addNewParamEditableRelation', relationId)
    },
    deleteNewParamEditableRelation({commit}, playLoad) {
      commit('deleteNewParamEditableRelation', playLoad)
    },
    setEditableObject({commit, dispatch}, {objectId, recId=null}) {
      if(!recId)
        commit('setEditableObjects', new DataBaseObject({object_id: objectId}))
      else
        dispatch('getObjectFromServer', {params: {record_id: recId, object_id: objectId}})
          .then(r => {
            commit('setEditableObjects', new DataBaseObject(r))
            dispatch('setNavigationDrawerStatus', true)
            dispatch('setActiveTool', 'createObjectPage')
          })
    },
    addEditableObjects({getters, commit}, objects) {
      commit('resetEditableObjects')
      const zeroObject = getters.editableObjects[0]
      for(let object of objects) {
        let newObject = new DataBaseObject(Object.assign(object, {recIdOld: zeroObject.recId}))
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
      return await axios.get('objects/object/', config)
        .then(r => { return Promise.resolve(r.data) })
        .catch(e => { return Promise.reject(e) })
    },
    async getRelationFromServer({getters, commit, dispatch}, params, config={}) {
      return await axios.post('objects/object_relation/', params, config)
        .then(r => {
          if(r.data.length === 0){
            let findNode = getters.graphObjects.find(o => o.id === params.object_id.toString() + '-' + params.rec_id.toString())
            findNode.object.show = true
            dispatch('updateObjectFromGraph', {object: findNode, fields: {object: findNode.object}})
          }
          for(let relation of r.data) {
            let object = {o1: params.object_id, r1: params.rec_id, o2: relation.object_id, r2: relation.rec_id}
            dispatch('addRelationToGraph', {object: object, relations: relation.relations, noMove: params.noMove})
          }
          return Promise.resolve(r.data)
        })
        .catch(e => { return Promise.reject(e) })

    },
    async saveEditableObject({getters, dispatch}, positionObject) {
      return await axios.post('objects/object',
        getters.editableObjects[positionObject].getRequestStructure(),
        {headers: {
          'Content-Type': 'multipart/form-data',
          'set-cookie': JSON.stringify(getTriggers(getters.editableObjects[positionObject].object.id))
        }}
      )
        .then(r => {
          let response = r.data
          if(Array.isArray(response)) {
            dispatch('addEditableObjects', response)
          }
          else {
            dispatch('setEditableObject', {objectId: response.object_id, recId: response.rec_id})
            dispatch('addObjectToGraph', {objectId: response.object_id, recId: response.rec_id})
          }
          return Promise.resolve(r.data)
        })
        .catch(e => { return Promise.reject(e) })
    },
    async saveEditableRelation({getters, dispatch}) {
      let relation = getters.editableRelation
      let request = Object.assign(
          {doc_rec_id: relation.document ? relation.document.object.recId : null},
          relation.relation.getRequestStructure()
      )
      return await axios.post('objects/relation', request, {})
        .then(r => {
          let object = {o1: r.data.object_id_1, r1: r.data.rec_id_1, o2: r.data.object_id_2, r2: r.data.rec_id_2}
          dispatch('addRelationToGraph', {object: object, relations: r.data.params, noMove: true})
          dispatch('setEditableRelation',
            {
              relations: [relation.relation.o1, relation.relation.o2],
              document: relation.document
            })
          return Promise.resolve(r.data)
        })
        .catch(e => { return Promise.reject(e) })
    }
  }
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


export class DataBaseRelation extends BaseDbObject {
  constructor(o1, o2, params=[]) {
    let getter = store.getters.baseRelation
    let baseObject = store.getters.baseRelations({f_id: o1.object.object.id, s_id: o2.object.object.id})
    super(getter, baseObject, params)
    this.o1 = o1
    this.o2 = o2
  }

  getRequestStructure() {
    let params = []
    for(let param of this.params)
      for (let newValue of param.new_values) {
        let value = newValue.value
        params.push({id: param.baseParam.id, value: value, date: newValue.date})
      }
    return {
      object_1_id: this.o1.object.object.id,
      object_2_id: this.o2.object.object.id,
      rec_1_id: this.o1.object.recId,
      rec_2_id: this.o2.object.recId,
      params: params,
    }
  }
}


export class DataBaseObject extends BaseDbObject {
  constructor({object_id, rec_id = 0, params = [], recIdOld = null}) {
    super(store.getters.baseClassifier, store.getters.baseClassifiers(object_id), params, recIdOld)
    this.object = store.getters.baseObject(object_id)
    this.recId = rec_id
  }

  getRequestStructure() {
    let formData = new FormData()
    let params = []
    for(let param of this.params) {
      for (let newValue of param.new_values) {
        if(param.baseParam.type.title.startsWith('file')){
          params.push({id: param.baseParam.id, value: params.length.toString(), date: newValue.date})
          formData.append(params.length - 1, newValue.value.file)
        } else params.push({id: param.baseParam.id, value: newValue.value, date: newValue.date})
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
      this.values.push(new ValueParam(v.value, v.date, v.doc))
  }
}

class ValueParam {
  constructor(value=null, date=this.getDateTime(), doc=null) {
    this.value = value
    this.date = date
    if(doc)
      this.doc = doc
  }

  getDateTime() {
    let dateTime = new Date()
    let time = dateTime.toLocaleTimeString('ru-RU').split(':')
    let date = dateTime.toLocaleDateString('ru-RU').split('.')
    return date[2] + '-' + date[1] + '-' + date[0] + ' ' + time[0] + ':' + time[1]
  }
}