import { postResponseAxios } from '@/plugins/axios_settings'

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
    foundObjects: null,
  },
  getters: {
    searchTreeGraph: state => { return state.searchTreeGraph },
    foundObjects: state => { return state.foundObjects },
  },
  mutations: {
    setRootSearchTreeItem: (state, rootObject) => state.searchTreeGraph = rootObject,
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
    findObjectsOnServer({ commit, state }, config={}) {
      return postResponseAxios('objects/search', state.searchTreeGraph.getTree(), config)
        .then(response => { commit('setFoundObjects', response.data) })
        .catch(error => {  })
    },
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
  }

  getInformation() {
    return ''
  }

  getInformationActual() {
    return this.actualIcon.find(i => i.status === this.actual)
  }

  getTree(item=this) {
    let tree = {actual: item.actual, object_id: item.object.id, request: item.request, rels: []}
    for(let rel of item.rels)
      tree.rels.push(this.getTree(rel))
    return tree
  }
}

class SearchTreeItem extends SearchTreeRootItem{

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
    if (this.relValue) message += `('${this.rel.list.find(i => i.id === this.relValue).value}')`
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