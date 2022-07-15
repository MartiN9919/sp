import {ParamObject} from "@/store/modules/graph/general"
import UserSetting from "@/store/addition"
import axios from '@/plugins/axiosSettings'
import store from '@/store'
import _ from 'lodash'


export default {
  state: {
    searchObject: new UserSetting('defaultSearchObject', []),
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
      if(state.searchObject.value !== root.baseId) {
        state.searchObject.value = root.baseId
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
        root || new SearchTreeMain({base: getters.searchObject || [getters.baseObjects[0].id]})
      )
    },
    setRootSearchRelation({getters, commit}, {base, title, recId}) {
      commit('setRootSearchRelation',
        new SearchTreeMain({base: [base.id], recId, request: title})
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
      let triggers = {}
      for(const object of getters.searchTreeGraph.base) {
        triggers[object.id] = getters.cookieTriggers(object.id)
      }
      config.headers = {'set-cookie': JSON.stringify(triggers)}
      return axios.post('objects/search', getters.searchTreeGraph.getTree, config)
      .then(response => commit('setFoundObjects', response.data))
      .catch(error => {  })
    },
    findRelationsOnServer({ dispatch, state }, config={}) {
      let tree = state.searchRelationTreeGraph.getTree
      tree.object_id = tree.object_id[0]
      return axios.post('objects/search_relations', tree, config)
        .then(response => dispatch('addObjectsToGraph', {
          payload: response.data,
          action: {name: 'findRelationsOnServer', payload: state.searchRelationTreeGraph.request}
        }))
        .catch(error => {  })
    },
    simpleFindObject({state}, {objectId, searchRequest}) {
      let request = {actual: false, object_id: [objectId], request: searchRequest, rels: []}
      return axios.post('objects/search', request, {})
    }
  }
}

const actual = [
  {icon: 'mdi-check', color: 'green', status: true},
  {icon: 'mdi-close', color: 'red', status: false}
]

export class SearchTreeBase {
  actualIcon = actual

  constructor(base, request='', actual=true) {
    this.base = this._generateBase(base)
    this.fields = this._generateFields(base)
    this.request = request
    this.actual = actual
    this.rels = []
  }

  get baseId() {
    return this.base
  }

  set baseId(base) {
    this.base = this._generateBase(base)
    this.fields = this._generateFields()
  }

  _generateBase(base) {
    return []
  }

  _generateFields(base) {
    return []
  }

  switchField(field) {
    if (field.type.title === 'date') {
      field.type.value = 'period'
    }
    if (field.type.title === 'file') {
      field.type.title = 'text'
    }
    if (field.type.title === 'geometry') {
      field.type.value = 'polygon'
    }
    return new ParamObject(field)
  }

  get getTree() {
    return Object.assign(this.baseTree, this.extraTree)
  }

  get extraTree() {
    return {}
  }

  get baseTree() {
    const fields = this.fields.map(f => f.requestStructure).filter(f => f.length).flat()
    return {
      actual: this.actual,
      request: fields.length ? fields : this.request,
      rels: this.rels.map(r => r.getTree)
    }
  }

  get fieldInformation() {
    let info = ''
    if(this.fields) {
      this.fields.forEach(f => {
        if(f.new_values.length) {
          info += [
            f.baseParam.title,
            f.new_values.map(v => v.value).filter(v => v && v.length).join(', ')
          ].join(': ') + '; '
        }
      })
    }
    return info
  }

  get actualInformation() {
    return this.actualIcon.find(i => i.status === this.actual)
  }

  get isFields() {
    if(this.fields) {
      for (const field of this.fields) {
        if (field.new_values.length) {
          return true
        }
      }
    }
    return false
  }

  get isAdditionalSettings() {
    return this.isFields
  }

  cleanAdditionalSettings() {
    this.fields = this._generateFields()
    this.actual = true
  }
}

export class SearchTreeMain extends SearchTreeBase {
  constructor({base, request = '', actual = true, recId = null}) {
    super(base, request, actual)
    this.recId = recId
  }

  _generateBase(base) {
    return base.map(id => store.getters.baseObject(id))
  }

  _generateFields() {
    if(this.base.length === 1) {
      return store.getters.baseClassifiers(this.base[0].id).map(c => this.switchField(_.cloneDeep(c)))
    } else {
      return []
    }
  }

  get baseId() {
    return this.base.map(object => object.id)
  }

  set baseId(base) {
    super.baseId = base
  }

  get extraTree() {
    if(this.recId) {
      return {'rec_id': this.recId}
    } else {
      return {}
    }
  }

  get baseTree() {
    return Object.assign(super.baseTree, {object_id: this.base.map(base => base.id)})
  }

  get information() {
    return ''
  }
}

export class SearchTreeChild extends SearchTreeBase {
  constructor({base, request, actual, rel, relValue, relDateTimeStart, relDateTimeEnd}) {
    super(base, request, actual)
    this.relId = store.getters.baseRelation(rel)
    this.relValue = relValue
    this.relDateTimeStart = relDateTimeStart
    this.relDateTimeEnd = relDateTimeEnd
  }

  _generateBase(base) {
    return store.getters.baseObject(base)
  }

  _generateFields() {
    return store.getters.baseClassifiers(this.base.id).map(c => this.switchField(_.cloneDeep(c)))
  }

  get baseId() {
    return this.base.id
  }

  set baseId(base) {
    super.baseId = base
  }

  get relId() {
    return this.rel ? this.rel.id : 0
  }

  set relId(id) {
    this.rel = store.getters.baseRelation(id)
  }

  get extraTree() {
    return {rel: {
        id: this.rel?.id || 0,
        value: this.relValue || 0,
        date_time_start: this.relDateTimeStart,
        date_time_end: this.relDateTimeEnd
      }}
  }

  get baseTree() {
    return Object.assign(super.baseTree, {object_id: this.base.id})
  }

  get information() {
    let message = ''
    if (this.rel) {
      message += this.rel.title
    }
    if (this.relValue) {
      message += ` ('${store.getters.baseList(this.rel.type.value).values.find(i => i.id === this.relValue).value}')`
    }
    if (this.relDateTimeStart) {
      message += ` c ${this.relDateTimeStart}`
    }
    if (this.relDateTimeEnd) {
      message += ` по ${this.relDateTimeEnd}`
    }
    return message
  }

  get isAdditionalSettings() {
    return super.isAdditionalSettings || this.relDateTimeStart || this.relDateTimeEnd
  }

  cleanAdditionalSettings() {
    super.cleanAdditionalSettings()
    this.relDateTimeStart = null
    this.relDateTimeEnd = null
  }

  change(newItem) {
    Object.assign(this, newItem)
  }
}