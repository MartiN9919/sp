import { getResponseAxios } from '@/plugins/axios_settings'
import Graph from "@/components/Graph/lib/graph"
import {DataBaseObject, DataBaseRelation} from '@/store/modules/graph/graphMenu/recordEditor'
import Vue from 'vue'

class GlobalSettings {
  constructor() {
    this.showGlobalTitle = {
      title: 'Подписи объектов',
      subTitle: 'Подпись под объектомами на графе',
      state: this.getGlobalSettings('showGlobalTitle', true)
    }
    this.showGlobalTooltipObject = {
      title: 'Заголовки объектов',
      subTitle: 'Отображение заголовка над объектами',
      state: this.getGlobalSettings('showGlobalTooltipObject', false)
    }
    this.showGlobalTriggers = {
      title: 'Уведомления о триггерах',
      subTitle: 'Управление отображением значка уведомления о срабатывании триггеров',
      state: this.getGlobalSettings('showGlobalTriggers', false)
    }
    this.showGlobalTooltipRelation = {
      title: 'Заголовоки связей',
      subTitle: 'Отображение заголовка над связями',
      state: this.getGlobalSettings('showGlobalTooltipRelation', true)
    }
    this.showRelations = {
      title: 'Отображение связей',
      state: this.getGlobalSettings('showRelations', true)
    }
  }

  changeState(identifier, value) {
    localStorage.setItem(identifier, value)
    this[identifier].state = value
  }

  getGlobalSettings(identifier, defaultValue) {
    if(!localStorage.getItem(identifier))
      localStorage.setItem(identifier, defaultValue)
    return localStorage.getItem(identifier) === 'true'
  }
}

export default {
  state: {
    triggers: [],
    classifiersSettings: getClassifiersSettings(),
    globalDisplaySettings: new GlobalSettings(),
    graph: new Graph(),
    graphObjects: {},
  },
  getters: {
    graphObjects: state => { return state.graph.nodes },
    graphRelations: state => { return state.graph.edges },
    triggers: state => { return state.triggers },
    objectTriggers: state => objectId => { return state.triggers.filter(trigger => trigger.objectId === objectId) },
    objectClassifiersSettings: state => objectId => { return state.classifiersSettings[objectId] || [] },
    globalDisplaySettings: state => { return state.globalDisplaySettings },
  },
  mutations: {
    addTrigger: (state, trigger) => state.triggers.push(trigger),
    changeGlobalSettingState: (state, {id, value}) => state.globalDisplaySettings.changeState(id, value),
    setTriggerState: (state, {triggerId, value}) => state.triggers.find(t => t.id === triggerId).setState(value),
    setClassifiersSettings: (state, {objectId, classifierId}) => {
      if(state.classifiersSettings.hasOwnProperty(objectId)) {
        let classifierIndex = state.classifiersSettings[objectId].findIndex(id => id === classifierId)
        if (classifierIndex !== -1) {
          state.classifiersSettings[objectId].splice(classifierIndex, 1)
        } else state.classifiersSettings[objectId].push(classifierId)
      } else Vue.set(state.classifiersSettings, objectId, [classifierId])
      localStorage.setItem('objectClassifiersSettings', JSON.stringify(state.classifiersSettings))
    },
    addObjectToGraph: (state, editableObject) => {
      state.graph.createNode({
        id: editableObject.getGeneratedId(),
        offsetX: 0, offsetY: 0, size: 600,
        x: Math.random() * 1000, y: Math.random() * 1000,
        object: editableObject
      })
    },
    addRelationToGraph: (state, {objects, relation}) => {
      state.graph.createEdge(objects[0], objects[1],{relation: relation, size: 600})
    },
  },
  actions: {
    reorderGraph({ state }) { state.graph.reorderGraph() },
    changeGlobalSettingState({ commit }, payload) { commit('changeGlobalSettingState', payload) },
    setTriggerState({ commit }, payload) { commit('setTriggerState', payload) },
    setClassifiersSettings({ commit }, payload) { commit('setClassifiersSettings', payload) },
    addRelationToGraph({getters, commit}, {object, relations}) {
      let object1 = getters.graphObjects.find(r => r.object.object.id === object.o1 && r.object.recId === object.r1)
      let object2 = getters.graphObjects.find(r => r.object.object.id === object.o2 && r.object.recId === object.r2)
      let relation = new DataBaseRelation(object1, object2, relations)
      commit('addRelationToGraph', {objects: [object1, object2], relation: relation})
    },
    addObjectToGraph({ getters, commit, dispatch }, object) {
      let editableObject = new GraphObject({
        object_id: object.object_id,
        rec_id: object.rec_id,
        title: object.title,
        photo: object.photo,
        params: object.params,
        triggers: object.triggers
      })
      if(!getters.graphObjects.find(o => o.id === editableObject.getGeneratedId())) {
        for(let graphObject of getters.graphObjects) {

        }
        dispatch('getRelationFromServer', {
          object_id: object.object_id,
          rec_id: object.rec_id,
          objects: Array.from(getters.graphObjects, o =>
            Object.assign({object_id: o.object.object.id, rec_id: o.object.recId})
          )
        })
        commit('addObjectToGraph', editableObject)
      }
    },
    async getBaseTriggers({getters, commit}, config = {}) {
      if(!getters.triggers.length)
        return await getResponseAxios('script/trigger_list/', config)
          .then(r => {
            Object.entries(r.data).forEach(([k, v]) => { v.map(t => commit('addTrigger', new Trigger(k, t))) })
            let triggers = new Map(Object.entries(localStorage).filter(i => i[0].startsWith('trigger')))
            for (let [n, v] of triggers) {
              if (getters.triggers.find(t => t.getTriggerName() === n)?.setValues(JSON.parse(v)))
                continue
              localStorage.removeItem(n)
            }
          })
          .catch(e => { return Promise.reject(e) })
      return Promise.resolve()
    },
  }
}

export function getTriggers(id) {
  let cookies = []
  for (let [name, value] of Object.entries(localStorage))
    if (name.startsWith('trigger') && name.split('_')[1] === id.toString())
      cookies.push({id: name.split('_')[2], variables: JSON.parse(value)})
  return cookies
}

function getClassifiersSettings() {
  let settings = localStorage.getItem('objectClassifiersSettings')
  if(settings) return JSON.parse(settings)
  localStorage.setItem('objectClassifiersSettings', JSON.stringify({}))
  return {}
}

class GraphObject extends DataBaseObject {
  constructor(object) {
    super(object)
    this.showTitle = true
    this.showTooltip = true
    this.showTriggers = true
  }
}

class Trigger {
  constructor(objectId, trigger) {
    this.objectId = parseInt(objectId)
    this.id = trigger.id
    this.title = trigger.name
    this.subTitle = trigger.hint
    this.variables = []
    this.state = false
    for (let variable of trigger.variables) {
      variable.value = null
      this.variables.push(variable)
    }
  }

  setState(state) {
    this.state = state
    let variable = {}
    if (this.state) {
      for (let v of this.variables)
        variable[v.name] = v.value
      localStorage.setItem(this.getTriggerName(), JSON.stringify(variable))
    } else localStorage.removeItem(this.getTriggerName())
  }

  setValues(variables) {
    if(this.variables.length === Object.keys(variables).length) {
      for (let variable in variables) {
        if (!this.variables.find(v => v.name === variable)) return false
      }
      for (let [name, value] of Object.entries(variables))
        this.variables.find(variable => variable.name === name).value = value
      this.state = true
      return true
    } else return false
  }

  getTriggerName() {
    return `trigger_${this.objectId}_${this.id}`
  }
}
