import { getResponseAxios } from '@/plugins/axios_settings'
import Graph from "vnodes/src/graph"
import {DataBaseObject} from '@/store/modules/graph/graphMenu/recordEditor'
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
      let x = Math.floor(Math.random() * 500)
      let y = Math.floor(Math.random() * 500)
      state.graph.createNode({ id: editableObject.getGeneratedId(), x: x, y: y, width: 100, height: 100, object: editableObject})
      if(state.graph.nodes.length === 2)
        state.graph.createEdge(state.graph.nodes[0].id, state.graph.nodes[1].id)
    },
  },
  actions: {
    changeGlobalSettingState({ commit }, payload) { commit('changeGlobalSettingState', payload) },
    setTriggerState({ commit }, payload) { commit('setTriggerState', payload) },
    setClassifiersSettings({ commit }, payload) { commit('setClassifiersSettings', payload) },
    addObjectToGraph({ getters, commit }, object) {
      let editableObject = new DataBaseObject(object.object_id, object.rec_id, object.title, object.params)
      if(!getters.graphObjects.find(o => o.id === editableObject.getGeneratedId()))
        commit('addObjectToGraph', editableObject)
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

function getClassifiersSettings() {
  let settings = localStorage.getItem('objectClassifiersSettings')
  if(settings) return JSON.parse(settings)
  localStorage.setItem('objectClassifiersSettings', JSON.stringify({}))
  return {}
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