import axios from '@/plugins/axiosSettings'

export default {
  state: {
    objects: [],
    classifiers: [],
    relations: [],
    baseLists: [],
    triggers: [],
  },
  getters: {
    baseObjects: state => state.objects,
    baseObject: state => id => state.objects.find(o => o.id === id),
    baseClassifiers: state => id => state.classifiers.filter(c => c.objectId === id),
    baseClassifier: state => id => state.classifiers.find(c => c.id === id),
    baseRelation: state => id => state.relations.find(r => r.id === id),
    baseRelations: state => ids => state.relations.filter(r => [r.f_id, r.s_id].every(i => Object.values(ids).includes(i))),
    baseLists: state => state.baseLists,
    baseList: state => id => state.baseLists[id],
    triggers: state => state.triggers,
    objectTriggers: state => objectId => state.triggers.filter(trigger => trigger.objectId === objectId),
  },
  mutations: {
    setBaseObjects: (state, objects) => state.objects.push(...objects),
    addBaseClassifiers: (state, classifiers) => state.classifiers.push(...classifiers),
    setBaseRelations: (state, relations) => state.relations.push(...relations),
    setBaseLists: (state, lists) => state.baseLists = lists,
    addTrigger: (state, trigger) => state.triggers.push(trigger),
    setTriggerState: (state, {triggerId, value}) => state.triggers.find(t => t.id === triggerId).setState(value),
  },
  actions: {
    async initialization({getters, dispatch}) {
      if (!getters.userInformation)
        await Promise.all([
          getters.globalNotificationStatus ? dispatch('getNotifications') : null,
          dispatch('getBaseObjects'),
          dispatch('getBaseLists'),
          dispatch('getBaseTriggers'),
          dispatch('getBaseRelations'),
          dispatch('getBaseClassifiers')
        ])
    },
    async getBaseObjects({commit, dispatch}, config = {}) {
      await axios.get('objects/list_type/', config)
        .then(r => { commit('setBaseObjects', r.data.map(o => new BaseObject(o))) })
        .catch(e => { return Promise.reject(e) })
      return Promise.resolve()
    },
    async getBaseClassifiers({getters, commit}, config = {}) {
      await axios.get('objects/list_classifier/', config)
        .then(r => { commit('addBaseClassifiers', r.data.map(c => new BaseClassifier(c))) })
        .catch(e => { return Promise.reject(e) })
      return Promise.resolve()
    },
    async getBaseRelations({commit}, config = {}) {
      await axios.get('objects/relations/', config)
        .then(r => { commit('setBaseRelations', r.data.map(l => new BaseRelation(l))) })
        .catch(e => { return Promise.reject(e) })
      return Promise.resolve()
    },
    async getBaseLists({commit}, config = {}) {
      await axios.get('objects/lists/', config)
        .then(r => { commit('setBaseLists', r.data) })
        .catch(e => { return Promise.reject(e) })
      return Promise.resolve()
    },
    async getBaseTriggers({getters, commit}, config = {}) {
      await axios.get('script/trigger_list/', config)
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
    setTriggerState({ commit }, payload) { commit('setTriggerState', payload) },
  }
}

class BaseInstanceToObject {
  constructor(id, title) {
    this.id = id
    this.title = title
  }
}

class BaseObject extends BaseInstanceToObject {
  constructor(baseObject) {
    super(baseObject.id, baseObject.title)
    this.name = baseObject.name
    this.rels = baseObject.rels
    this.titleSingle = baseObject.title_single
    this.icon = baseObject.icon
  }
}

class BaseClassifier extends BaseInstanceToObject {
  constructor(baseClassifier) {
    super(baseClassifier.id, baseClassifier.title)
    this.objectId = baseClassifier.obj_id
    this.name = baseClassifier.name
    this.type = baseClassifier.type
    this.list = baseClassifier.list_id
  }
}

class BaseRelation extends BaseInstanceToObject {
  constructor(baseRelation) {
    super(baseRelation.id, baseRelation.title)
    this.f_id = baseRelation.object_id_1
    this.s_id = baseRelation.object_id_2
    this.hint = baseRelation.hint
    this.type = baseRelation.type
  }
}

export function getTriggers(id) {
  let cookies = []
  for (let [name, value] of Object.entries(localStorage))
    if (name.startsWith('trigger') && name.split('_')[1] === id.toString())
      cookies.push({id: name.split('_')[2], variables: JSON.parse(value)})
  return cookies
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