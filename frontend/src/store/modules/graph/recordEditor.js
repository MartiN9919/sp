import CONST from '@/plugins/const'
import axios from '@/plugins/axiosSettings'
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
        relation: _.cloneDeep(edge.relation) || new DataBaseRelation(...relations),
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
        dispatch('getObjectFromServer', {rec_id: recId, object_id: objectId})
          .then(r => {
            commit('setEditableObjects', r)
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
    async getObjectFromServer({getters, commit, dispatch}, {rec_id, object_id, config = {}}) {
      config.headers = {'set-cookie': getters.cookieTriggers(object_id)}
      return await axios.get('objects/object/', Object.assign(config, {params: {rec_id, object_id}}))
        .then(r => Promise.resolve(new DataBaseObject(r.data)))
        .catch(e => Promise.reject(e))
    },
    async getRelationFromServer({getters, commit, dispatch}, {from, objects, config = {}}) {
      const params = Object.assign(from.ids, {objects: Array.from(objects, n => n.ids)})
      return await axios.post('objects/object_relation/', params, config)
        .then(r => Promise.resolve(r.data.map(relation => {
          const object = objects.find(o => o.ids.object_id === relation.object_id && o.ids.rec_id === relation.rec_id)
          return new DataBaseRelation(from, object, relation.relations)
        })))
        .catch(e => Promise.reject(e))
    },
    async saveEditableObject({getters, dispatch}, positionObject) {
      return await axios.post('objects/object/',
        getters.editableObjects[positionObject].getRequestStructure(),
        {headers: {
          'Content-Type': 'multipart/form-data',
          'set-cookie': getters.cookieTriggers(getters.editableObjects[positionObject].object.id)
        }}
      )
        .then(r => {
          let response = r.data
          if(Array.isArray(response)) {
            dispatch('addEditableObjects', response)
          }
          else {
            dispatch('setEditableObject', {objectId: response.object_id, recId: response.rec_id})
            dispatch('addToGraph', {payload: response})
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
      return await axios.post(CONST.API.OBJ.SET_RELATION, request, {})
        .then(r => {
          let object = {o1: r.data.object_id_1, r1: r.data.rec_id_1, o2: r.data.object_id_2, r2: r.data.rec_id_2}
          dispatch('addRelationToGraph', {object: object, relations: r.data.params, noMove: true})
          const relations = [relation.relation.o1, relation.relation.o2]
          dispatch('setEditableRelation',{relations, document: relation.document})
          return Promise.resolve(r.data)
        })
        .catch(e => { return Promise.reject(e) })
    }
  }
}

class BaseDbObject {
  constructor(getter, baseObjects, params) {
    this.params = baseObjects.map(p => new ParamObject(getter(p.id), params.find(n => n.id === p.id)?.values))
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
    let baseObject = store.getters.baseRelations({f_id: o1.base.id, s_id: o2.base.id})
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
      ...this.ids,
      params: params,
    }
  }

  get ids() {
    return {
      object_1_id: this.o1.base.id,
      rec_1_id: this.o1.recId,
      object_2_id: this.o2.base.id,
      rec_2_id: this.o2.recId
    }
  }

  getGeneratedId() {
    return `${this.o1.base.id}-${this.o1.recId}@${this.o2.base.id}-${this.o2.recId}`
  }
}


export class DataBaseObject extends BaseDbObject {
  constructor({object_id, rec_id = 0, recIdOld = null, params = [], triggers=[], title='', photo=''}) {
    super(store.getters.baseClassifier, store.getters.baseClassifiers(object_id), params)
    this.base = store.getters.baseObject(object_id)
    this.recIdOld = recIdOld
    this.recId = rec_id
    this.title = title
    this.photo = photo
    this.triggers = triggers
  }

  get ids() {
    return {object_id: this.base.id, rec_id: this.recId}
  }

  getGeneratedId() {
    return `${this.base.id}-${this.recId}`
  }

  getRequestStructure() {
    let formData = new FormData()
    let params = []
    for(let param of this.params) {
      for (let newValue of param.new_values) {
        if(param.baseParam.type.title.startsWith('file')){
          params.push({id: param.baseParam.id, value: params.length.toString(), date: newValue.date})
          formData.append(params.length - 1, newValue.value.file)
        } else {
          params.push({id: param.baseParam.id, value: newValue.value, date: newValue.date})
        }
      }
    }
    formData.append('data', JSON.stringify({
      rec_id: this.recId,
      object_id: this.object.id,
      rec_id_old: this.recIdOld,
      force: store.getters.editableObjects.length > 1,
      params: params,
    }))
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
    this.values = values.map(v => new ValueParam(v.value, v.date, v.doc))
  }
}

class ValueParam {
  constructor(value=null, date=this.getDateTime(), doc=null) {
    this.value = value
    this.date = date
    this.doc = doc
  }

  getDateTime() {
    let dateTime = new Date()
    let time = dateTime.toLocaleTimeString('ru-RU').split(':')
    let date = dateTime.toLocaleDateString('ru-RU')
    return date + ' ' + time[0] + ':' + time[1]
  }
}