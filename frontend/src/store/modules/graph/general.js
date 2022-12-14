import axios from '@/plugins/axiosSettings'
import store from "@/store"
import _ from 'lodash'

export default {
  state: {},
  getters: {},
  mutations: {},
  actions: {
    async getObject({getters}, {rec_id, object_id, config = {}}) {
      config.headers = {'set-cookie': JSON.stringify(getters.cookieTriggers(object_id))}
      return await axios.get('objects/object/', Object.assign(config, {params: {rec_id, object_id}}))
        .then(r => r.data ? Promise.resolve(new DataBaseObject(r.data)) : Promise.reject(r))
        .catch(e => Promise.reject(e))
    },
    async getRelation({getters}, {from, to, config = {}}) {
      const params = Object.assign(from.ids, {objects: [to.ids]})
      return await axios.post('objects/object_relation/', params, config)
        .then(r => Promise.resolve(new DataBaseRelation(from, to, r.data[0].relation_types)))
        .catch(e => Promise.reject(e))
    },
    async getRelations({getters}, {from, objects, config = {}}) {
      const params = Object.assign(from.ids, {objects: Array.from(objects, n => n.ids)})
      return await axios.post('objects/object_relation/', params, config)
        .then(r => Promise.resolve(r.data.map(relation => {
          const object = objects.find(o => o.ids.object_id === relation.object_id && o.ids.rec_id === relation.rec_id)
          return new DataBaseRelation(from, object, relation.relation_types)
        })))
        .catch(e => Promise.reject(e))
    },
    getObjects({dispatch}, objects) {
      const promises = objects.map(({object_id, rec_id}) => dispatch('getObject', {object_id, rec_id}))
      return Promise.allSettled(promises)
    },
    getRelationsForObjects({getters, dispatch}, objects) {
      const promiseRelations = objects.map((n, i) => {
        const availableObjects = getters.graphNodesEntity.concat(objects.slice(0, i))
        return dispatch('getRelations', {from: n, objects: availableObjects})
      })
      return Promise.allSettled(promiseRelations)
    },
    async getRelationsBtwObjects({getters, dispatch}, objects) {
      let config = {}
      if(objects.length === 2)
        config.params = {
          object_id_1: objects[0].ids.object_id,
          object_id_2: objects[1].ids.object_id,
          rec_id_1: objects[0].ids.rec_id,
          rec_id_2: objects[1].ids.rec_id,
          search_deep: getters.searchSettingsValue('searchDeep'),
          search_count: getters.searchSettingsValue('searchCount'),
          search_short: getters.searchSettingsValue('searchShort')
        }
      return await axios.get('objects/objects_relation/', config)
        .then(response => {
          dispatch('addObjectsToGraph', {
            payload: response.data,
            action: {
              name: 'getRelationsBtwObjects',
              payload: `${objects[0].entity.title} ?? ${objects[1].entity.title}`
            }
          })
          return Promise.resolve()
        })
        .catch(e => { return Promise.reject(e) })
    }
  }
}


class BaseDbObject {
  constructor(getter, baseObjects, params) {
    this.params = baseObjects.map(p => new ParamObject(getter(p.id), params.find(n => n.id === p.id)?.values))
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

  get id() {
    return [this.o1.id, this.o2.id].sort().join('@')
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

  get id() {
    return `${this.base.id}-${this.recId}`
  }

  static requestParams(formData, params) {
    const request = []
    params.forEach(param => {
      param.new_values.forEach(newValue => {
        if(param.baseParam.type.title.startsWith('file')){
          request.push({id: param.baseParam.id, value: request.length.toString(), date: newValue.date})
          formData.append((request.length - 1).toString(), newValue.value.file)
        } else {
          request.push({id: param.baseParam.id, value: newValue.value, date: newValue.date})
        }
      })
    })
    return request
  }

  static arrayRequest(objects, file) {
    let formData = new FormData()
    formData.append(file.name, file)
    formData.append('data', JSON.stringify(
      objects.map(object => {
        return {
          rec_id: object.ids.rec_id,
          object_id: object.ids.object_id,
          id_str: object.id_str,
          name: object.name,
          params: DataBaseObject.requestParams(formData, object.params),
        }
      })
    ))
    return formData
  }

  getRequestStructure() {
    let formData = new FormData()
    formData.append('data', JSON.stringify({
      rec_id: this.ids.rec_id,
      object_id: this.ids.object_id,
      rec_id_old: this.recIdOld,
      force: store.getters.editableObjects.length > 1,
      params: DataBaseObject.requestParams(formData, this.params),
    }))
    return formData
  }

  concatParams(concatObject) {
    for(let param of concatObject.params) {
      let findParam = this.params.find(p => p.baseParam.id === param.baseParam.id)
      findParam.new_values = findParam.new_values.concat(param.values, _.cloneDeep(param.new_values))
    }
  }
}

export class ParamObject {
  constructor(baseParam, values=[], newValues=[]) {
    this.baseParam = baseParam
    this.new_values = newValues
    this.values = values.map(v => new ValueParam(v.value, v.date, v.doc))
  }

  add({value = null, date = null, doc = null, period = false}) {
    this.new_values.push(new ValueParam(value, date, doc, period))
  }

  remove(param) {
    this.new_values.splice(this.new_values.findIndex(par => par === param), 1)
  }

  get requestStructure() {
    return this.new_values.map(v => {
      return {id: this.baseParam.id, value: v.value, date: v.date}
    })
  }
}

class ValueParam {
  constructor(value=null, date=null, doc=null, period=false) {
    this.value = value
    this.date = date || (period ? this.period : this.dateTime)
    this.doc = doc
  }

  get dateTime() {
    let dateTime = new Date()
    let time = dateTime.toLocaleTimeString('ru-RU').split(':')
    let date = dateTime.toLocaleDateString('ru-RU')
    return date + ' ' + time[0] + ':' + time[1]
  }

  get period() {
    const dateStart = new Date('01.01.1900').toLocaleDateString('ru-RU')
    const dateEnd = new Date().toLocaleDateString('ru-RU')
    return `${dateStart}-${dateEnd}`
  }
}