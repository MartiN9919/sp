import axios from '@/plugins/axiosSettings'
import UserSetting from "@/store/addition";
import CONST from '@/plugins/const'


export default {
  state: {
    objects: null,
    classifiers: null,
    relations: null,
    baseLists: null,
    triggers: [],
  },
  getters: {
    baseObjects: state => state.objects,
    baseObject: state => id => state.objects.find(o => o.id === id),
    baseClassifiers: state => id => state.classifiers.filter(c => c.objectId === id || c.objectId === 0),
    baseClassifier: state => id => state.classifiers.find(c => c.id === id),
    baseRelation: state => id => state.relations.find(r => r.id === id),
    baseRelations: state => ids => state.relations.filter(r => (r.f_id === ids.f_id && r.s_id === ids.s_id) || (r.f_id === ids.s_id && r.s_id === ids.f_id)),
    baseLists: state => state.baseLists,
    baseList: state => id => state.baseLists[id],
    triggers: state => state.triggers,
    objectTriggers: state => objectId => state.triggers.filter(trigger => trigger.objectId === objectId),
    cookieTriggers: state => id =>
      JSON.stringify(state.triggers
        .filter(trigger => trigger.objectId === id && trigger.state)
        .map(trigger => Object.assign({
          id: trigger.id,
          variables: trigger.variables.reduce(function(result, item) {
            result[item.name] = item.value
            return result;
          }, {})
        }))
      )
  },
  mutations: {
    setBaseObjects: (state, objects) => state.objects = objects,
    addBaseClassifiers: (state, classifiers) => state.classifiers = classifiers,
    setBaseRelations: (state, relations) => state.relations = relations,
    setBaseLists: (state, lists) => state.baseLists = lists,
    addTrigger: (state, trigger) => state.triggers.push(trigger),
    setTriggerState: (state, {triggerId, value}) => state.triggers.find(t => t.id === triggerId).setState(value),
  },
  actions: {
    async initialization({getters, dispatch}) {
      await Promise.all([
        getters.globalNotificationStatus ? dispatch('getNotifications') : null,
        dispatch('MAP_ACT_INI'),
        dispatch('getBaseObjects'),
        dispatch('getBaseLists'),
        dispatch('getBaseTriggers'),
        dispatch('getBaseRelations'),
        dispatch('getBaseClassifiers')
      ])
    },
    async getBaseObjects({commit, dispatch}, config = {}) {
      await axios.get(CONST.API.OBJ.GET_LIST_OBJ, config)
        .then(r => commit('setBaseObjects', r.data.map(o => new BaseObject(o))))
    },
    async getBaseClassifiers({getters, commit}, config = {}) {
      await axios.get(CONST.API.OBJ.GET_LIST_KEY_OBJ, config)
        .then(r => commit('addBaseClassifiers', r.data.map(c => new BaseClassifier(c))))
    },
    async getBaseRelations({commit}, config = {}) {
      await axios.get(CONST.API.OBJ.GET_LIST_KEY_REL, config)
        .then(r => commit('setBaseRelations', r.data.map(l => new BaseRelation(l))))
    },
    async getBaseLists({commit}, config = {}) {
      await axios.get(CONST.API.OBJ.GET_LISTS, config)
        .then(r => commit('setBaseLists', r.data))
    },
    async getBaseTriggers({getters, commit}, config = {}) {
      await axios.get(CONST.API.SCRIPT.GET_LIST_TRIGGER, config)
        .then(r => {
          Object.entries(r.data).forEach(([k, v]) => { v.map(t => commit('addTrigger', new Trigger(k, t))) })
        })
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
    this.ls = new UserSetting(this.getTriggerName())
    this.ls.value && this.setValues(this.ls.value)
  }

  setState(state) {
    this.state = state
    let variable = {}
    if (this.state) {
      for (let v of this.variables)
        variable[v.name] = v.value
      this.ls.value = variable
    } else this.ls.removeFromLocalstorage()
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
