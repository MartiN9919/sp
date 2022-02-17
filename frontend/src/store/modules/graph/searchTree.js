import axios from '@/plugins/axiosSettings'
import UserSetting from "@/store/addition"
import store from '@/store'

function createSearchItem(getters, item) {
  return {
    object: getters.baseObject(item.id),
    actual: item.actual,
    rel: getters.baseRelation(item.relId),
    relValue: item.relValue,
    relDateTimeStart: item.relDateTimeStart,
    relDateTimeEnd: item.relDateTimeEnd
  }
}

export default {
  state: {
    defaultSearchObject: new UserSetting('defaultSearchObject', 0),
    searchTreeGraph: null,
    searchRelationTreeGraph: null,
    foundObjects: null,
  },
  getters: {
    searchTreeGraph: state => { return state.searchTreeGraph },
    searchRelationTreeGraph: state => { return state.searchRelationTreeGraph },
    foundObjects: state => { return state.foundObjects },
  },
  mutations: {
    setRootSearchTreeItem: (state, rootObject) => state.searchTreeGraph = rootObject,
    setRootSearchRelationTreeItem: (state, rootObject) => state.searchRelationTreeGraph = rootObject,
    changeActualRootSearchTreeItem: (state, actual) => state.searchTreeGraph.actual = actual,
    addSearchTreeItem: (state, {rootItem, newItem}) => rootItem.rels.unshift(newItem),
    changeSearchTreeItem: (state, {rootItem, newItem}) => rootItem.changeItem(newItem),
    removeSearchTreeItem: (state, {item, removeItem}) => item.rels.splice(item.rels.findIndex(i => i === removeItem), 1),
    setFoundObjects: (state, objects) => state.foundObjects = objects,
  },
  actions: {
    removeSearchTreeItem({ commit }, {item, removeItem}) {
      commit('removeSearchTreeItem', {item, removeItem})
    },
    changeSearchTreeItem({ getters, commit }, {rootItem, newItem}) {
      commit('changeSearchTreeItem', {rootItem : rootItem, newItem: createSearchItem(getters, newItem)})
    },
    addSearchTreeItem({ getters, commit }, {rootItem, newItem}) {
      commit('addSearchTreeItem', {rootItem: rootItem, newItem: new SearchTreeItem(createSearchItem(getters, newItem))})
    },
    setRootSearchTreeItem({ state, getters, commit }, {id = null, actual = false}) {
      const additionalId = function () {
        if(!state.defaultSearchObject.value)
          state.defaultSearchObject.value = getters.baseObjects[0].id
        return state.defaultSearchObject.value
      }
      id = id || additionalId()
      if(getters.searchTreeGraph && id === getters.searchTreeGraph.object.id)
        commit('changeActualRootSearchTreeItem', actual)
      else {
        commit('setRootSearchTreeItem', new SearchTreeRootItem({object: getters.baseObject(id), actual: actual}))
        state.defaultSearchObject.value = id
      }
    },
    setRootSearchRelationTreeItem({ getters, commit }, item) {
      commit('setRootSearchRelationTreeItem', new SearchTreeRootItem({
        object: item.base,
        title: item.title,
        recId: item.recId,
        actual: true
      }))
    },
    findObjectsOnServer({ getters, commit }, config={}) {
      config.headers = {'set-cookie': getters.cookieTriggers(getters.searchTreeGraph.object.id)}
      return axios.post('objects/search', getters.searchTreeGraph.getTree(), config)
        .then(response => commit('setFoundObjects', response.data))
        .catch(error => {  })
    },
    findRelationsOnServer({ dispatch, state }, config={}) {
      return axios.post('objects/search_relations', state.searchRelationTreeGraph.getTree(), config)
        .then(response => dispatch('addObjectsToGraph', {payload: response.data}))
        .catch(error => {  })
    },
    simpleFindObject({state}, {objectId, searchRequest}) {
      let request = {actual: false, object_id: objectId, request: searchRequest, rels: []}
      return axios.post('objects/search', request, {})
    }
  }
}

class SearchTreeRootItem {
  actualIcon = [
    {icon: 'mdi-check', color: 'green', status: true},
    {icon: 'mdi-close', color: 'red', status: false}
  ]

  constructor(item) {
    this.actual = item.actual
    this.object = item.object
    this.request = ''
    this.rels = []
    if(item.hasOwnProperty('recId')) {
      this.title = item.title
      this.recId = item.recId
    }
  }

  getInformation() {
    return ''
  }

  getInformationActual() {
    return this.actualIcon.find(i => i.status === this.actual)
  }

  getTree() {
    let tree = {actual: this.actual, object_id: this.object.id, request: this.request, rels: []}
    if(this.hasOwnProperty('recId'))
      tree['rec_id'] = this.recId
    if(this.hasOwnProperty('rel'))
      tree.rel = {
        id: this.rel?.id || 0,
        value: this.relValue || 0,
        date_time_start: this.relDateTimeStart,
        date_time_end: this.relDateTimeEnd,
      }
    for(let rel of this.rels)
      tree.rels.push(rel.getTree())
    return tree
  }
}

class SearchTreeItem extends SearchTreeRootItem {
  constructor(item) {
    super({object: item.object, actual: item.actual})
    this.rel = item.rel
    this.relValue = item.relValue
    this.relDateTimeStart = item.relDateTimeStart
    this.relDateTimeEnd = item.relDateTimeEnd
  }

  getInformation() {
    let message = ''
    if (this.rel) message += this.rel.title
    if (this.relValue) message += `('${store.getters.baseList(this.rel.type.value).values.find(i => i.id === this.relValue).value}')`
    if (this.relDateTimeStart) message += ` c ${this.relDateTimeStart}`
    if (this.relDateTimeEnd) message += ` по ${this.relDateTimeEnd}`
    return message
  }

  changeItem(newItem) {
    this.object = newItem.object
    this.actual = newItem.actual
    this.rel = newItem.rel
    this.relValue = newItem.relValue
    this.relDateTimeStart = newItem.relDateTimeStart
    this.relDateTimeEnd = newItem.relDateTimeEnd
  }
}