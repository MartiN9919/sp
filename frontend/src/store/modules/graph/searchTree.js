import {ParamObject} from "@/store/modules/graph/general"
import UserSetting from "@/store/addition"
import axios from '@/plugins/axiosSettings'
import store from '@/store'


export default {
  state: {
    searchObject: new UserSetting('defaultSearchObject', 0),
    searchTreeGraph: null,
    searchRelationTreeGraph: null,
    foundObjects: null,
  },
  getters: {
    searchTreeGraph: state => state.searchTreeGraph,
    searchObject: state => state.searchObject.value,
    searchRelationTreeGraph: state => state.searchRelationTreeGraph,
    foundObjects: state => state.foundObjects,
  },
  mutations: {
    setRootSearch: (state, root) => {
      if(state.searchObject.value !== root.objectId) {
        state.searchObject.value = root.objectId
        root.rels = []
      }
      state.searchTreeGraph = root
    },
    setRootSearchRelation: (state, root) => state.searchRelationTreeGraph = root,

    addSearchTreeItem: (state, {rootItem, newItem}) => rootItem.rels.unshift(newItem),
    changeSearchTreeItem: (state, {rootItem, newItem}) => rootItem.change(newItem),
    removeSearchTreeItem: (state, {item, removeItem}) => item.rels.splice(item.rels.findIndex(i => i === removeItem), 1),

    setFoundObjects: (state, objects) => state.foundObjects = objects,
  },
  actions: {
    setRootSearch({getters, commit}, root=null) {
      commit('setRootSearch',
        root || new SearchTreeRootItem({id: getters.searchObject || getters.baseObjects[0].id})
      )
    },
    setRootSearchRelation({getters, commit}, {base, title, recId}) {
      commit('setRootSearchRelation',
        new SearchTreeRootItem({id: base.id, recId, request: title})
      )
    },
    addSearchTreeItem({ getters, commit }, {rootItem, newItem}) {
      commit('addSearchTreeItem', {rootItem: rootItem, newItem: newItem})
    },
    changeSearchTreeItem({ getters, commit }, {rootItem, newItem}) {
      commit('changeSearchTreeItem', {rootItem : rootItem, newItem: newItem})
    },
    removeSearchTreeItem({ commit }, {item, removeItem}) {
      commit('removeSearchTreeItem', {item, removeItem})
    },

    findObjectsOnServer({ getters, commit }, config={}) {
      config.headers = {'set-cookie': getters.cookieTriggers(getters.searchTreeGraph.object.id)}
      return axios.post('objects/search', getters.searchTreeGraph.getTree, config)
        .then(response => commit('setFoundObjects', response.data))
        .catch(error => {  })
    },
    findRelationsOnServer({ dispatch, state }, config={}) {
      return axios.post('objects/search_relations', state.searchRelationTreeGraph.getTree, config)
        .then(response => dispatch('addObjectsToGraph', {
          payload: response.data,
          action: {name: 'findRelationsOnServer', payload: state.searchRelationTreeGraph.title}
        }))
        .catch(error => {  })
    },
    simpleFindObject({state}, {objectId, searchRequest}) {
      let request = {actual: false, object_id: objectId, request: searchRequest, rels: []}
      return axios.post('objects/search', request, {})
    }
  }
}

export class SearchTreeRootItem {
  actualIcon = [
    {icon: 'mdi-check', color: 'green', status: true},
    {icon: 'mdi-close', color: 'red', status: false}
  ]

  constructor({id, actual = true, recId = null, request = ''}) {
    this.object = store.getters.baseObject(id)
    this.actual = actual
    this.recId = recId
    this.request = request
    this.rels = []
    this.fields = this.initFields()
  }

  get objectId() {
    return this.object.id
  }

  set objectId(id) {
    this.object = store.getters.baseObject(id)
    this.fields = this.initFields()
  }

  get isFields() {
    for(const field of this.fields) {
      if(field.new_values.length) {
        return true
      }
    }
    return false
  }

  get isAdditionalSettings() {
    return this.isFields || this.relDateTimeStart || this.relDateTimeEnd
  }

  get fieldInformation() {
    let info = ''
    this.fields.forEach(f => {
      if(f.new_values.length) {
        info += [f.baseParam.title, f.new_values.map(v => v.value).filter(v => v && v.length).join(', ')].join(': ') + '; '
      }
    })
    return info
  }

  get information() {
    return ''
  }

  get actualInformation() {
    return this.actualIcon.find(i => i.status === this.actual)
  }

  get baseTree() {
    const fields = this.fields.map(f => f.requestStructure).filter(f => f.length).flat()
    return {
      actual: this.actual,
      object_id: this.objectId,
      request: fields.length ? fields : this.request,
      rels: this.rels.map(r => r.getTree)
    }
  }

  get extraTree() {
    if(this.recId) {
      return {'rec_id': this.recId}
    } else {
      return {}
    }
  }

  get getTree() {
    return Object.assign(this.baseTree, this.extraTree)
  }

  initFields() {
    return store.getters.baseClassifiers(this.objectId).map(c => {
      if(c.type.title === 'date') {
        c.type.value = 'period'
      }
      if(c.type.title === 'file') {
        c.type.title = 'text'
      }
      if(c.type.title === 'geometry') {

        c.type.value = 'polygon'
      }
      return new ParamObject(c)
    })
  }

  cleanAdditionalSettings() {
    this.fields = this.initFields()
    this.actual = true
    if(this.relDateTimeStart || this.relDateTimeEnd) {
      this.relDateTimeStart = null
      this.relDateTimeEnd = null
    }
  }
}

export class SearchTreeItem extends SearchTreeRootItem {
  constructor(item) {
    super({id: item.id, actual: item.actual, recId: item.recId, request: item.request})
    this.relId = store.getters.baseRelation(item.rel)
    this.relValue = item.relValue
    this.relDateTimeStart = item.relDateTimeStart
    this.relDateTimeEnd = item.relDateTimeEnd
  }

  get relId() {
    return this.rel ? this.rel.id : 0
  }

  set relId(id) {
    this.rel = store.getters.baseRelation(id)
  }

  get information() {
    let message = ''
    if (this.rel) message += this.rel.title
    if (this.relValue) message += ` ('${store.getters.baseList(this.rel.type.value).values.find(i => i.id === this.relValue).value}')`
    if (this.relDateTimeStart) message += ` c ${this.relDateTimeStart}`
    if (this.relDateTimeEnd) message += ` по ${this.relDateTimeEnd}`
    return message
  }

  get extraTree() {
    return {rel: {
      id: this.rel?.id || 0,
      value: this.relValue || 0,
      date_time_start: this.relDateTimeStart,
      date_time_end: this.relDateTimeEnd
    }}
  }

  change(newItem) {
    Object.assign(this, newItem)
  }
}