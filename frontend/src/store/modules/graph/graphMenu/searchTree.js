import axios from '@/plugins/axios_settings'
import {getTriggers} from "@/store/modules/graph/graphNodes"
import store from'@/store'

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
    setRootSearchTreeItem({ getters, commit }, {id = null, actual = false}) {
      id = id || parseInt(localStorage.getItem('searchDefaultIdGraph')) || getters.baseObjects[0].id
      if(getters.searchTreeGraph && id === getters.searchTreeGraph.object.id)
        commit('changeActualRootSearchTreeItem', actual)
      else {
        commit('setRootSearchTreeItem', new SearchTreeRootItem({object: getters.baseObject(id), actual: actual}))
        localStorage.setItem('searchDefaultIdGraph', id)
      }
    },
    setRootSearchRelationTreeItem({ getters, commit }, item) {
      commit('setRootSearchRelationTreeItem', new SearchTreeRootItem({
        object: item.object.object,
        title: item.object.title,
        recId: item.object.recId,
        actual: true
      }))
    },
    findObjectsOnServer({ commit, state }, config={}) {
      config.headers = {'set-cookie': JSON.stringify(getTriggers(state.searchTreeGraph.object.id))}
      return axios.post('objects/search', state.searchTreeGraph.getTree(), config)
        .then(response => { commit('setFoundObjects', response.data) })
        .catch(error => {  })
    },
    findRelationsOnServer({ dispatch, state }, config={}) {
      return axios.post('objects/search_relations', state.searchRelationTreeGraph.getTree(), config)
        .then(response => {
          for (let obj of response.data) {
            dispatch('addObjectToGraph', {recId: obj.rec_id, objectId: obj.object_id})
          }
        })
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