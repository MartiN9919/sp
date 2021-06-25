import { getResponseAxios, postResponseAxios } from '@/plugins/axios_settings'

export default {
  state: {
    listObjectTemplates: [],
    workAreaAboveObjects: [],
    activeObjectId: null,
    templatesClassifiersForObjects: {},
    relationsBetweenTwoObjects: [],
  },
  getters: {
    listObjectTemplates: state => {
      return state.listObjectTemplates
    },
    objectTemplates: state => id => {
      return state.listObjectTemplates.find(object => object.id === id)
    },
    workAreaAboveObjects: state => {
      return state.workAreaAboveObjects
    },
    activeObject: state => {
      return state.workAreaAboveObjects.find(object => object.tempId === state.activeObjectId)
    },
    templatesClassifiersForObjects: state => id => {
      return state.templatesClassifiersForObjects[id]
    },
    foundObjects: state => id => {
      return state.workAreaAboveObjects.find(object => object.tempId === id).foundObjects
    },
    relationsBetweenTwoObjects: state => objectsId => {
      return state.relationsBetweenTwoObjects.find(object =>
        ((object.objectId1 === objectsId.objectId1 && object.objectId2 === objectsId.objectId2) ||
        (object.objectId1 === objectsId.objectId2 && object.objectId2 === objectsId.objectId1))
      )?.relations
    },
    relationObject: state => id => {
      for (let object of state.relationsBetweenTwoObjects) {
        let findRelation = object.relations.find(relation => relation.id === id)
        if (findRelation) return findRelation
      }
      return null
    }
  },
  mutations: {
    addListObjectTemplates: (state, listObjectTemplates) => {
      state.listObjectTemplates = listObjectTemplates
    },
    addObjectInWorkAreaAboveObjects: (state, object) => {
      state.workAreaAboveObjects.push(object)
    },
    removeObjectInWorkAreaAboveObjects: (state, id) => {
      let objectIndex = state.workAreaAboveObjects.findIndex(object => object.tempId === id)
      state.workAreaAboveObjects.splice(objectIndex, 1)
    },
    setActiveObjectId: (state, id) => {
      state.activeObjectId = id
    },
    setWindowForActiveObject: (state, window) => {
      let findActiveObject = state.workAreaAboveObjects.find(object => object.tempId === state.activeObjectId)
      if (findActiveObject) findActiveObject.activeWindow = window
    },
    addClassifier: (state, { objectId, classifiers }) => {
      state.templatesClassifiersForObjects[objectId] = classifiers
    },
    findObjectOnServer: (state, objects) => {
      state.workAreaAboveObjects.find(object => object.tempId === state.activeObjectId).foundObjects = objects
    },
    addRelations: (state, relations) => { state.relationsBetweenTwoObjects.push(relations) },
  },
  actions: {
    getListObjectTemplates ({ commit }, config = {}) {
      return getResponseAxios('objects/list_type/', config)
        .then(response => { commit('addListObjectTemplates', response.data) })
        .catch(() => {})
    },
    addObjectInWorkAreaAboveObjects ({ commit, state }, id) {
      let tempId = Number(Date.now().toString() + state.workAreaAboveObjects.length.toString())
      commit('addObjectInWorkAreaAboveObjects', {
        tempId: tempId,
        objectId: id,
        activeWindow: 'searchTree',
        searchTree: { object_id: id, rel_id: 0, request: '', rels: [], },
        foundObjects: [],
        objectConstructor: [],
      })
      commit('setActiveObjectId', tempId)
    },
    removeObjectInWorkAreaAboveObjects ({ commit, state }, id) {
      commit('removeObjectInWorkAreaAboveObjects', id)
      if (state.workAreaAboveObjects.length)
        commit('setActiveObjectId', state.workAreaAboveObjects[state.workAreaAboveObjects.length - 1].tempId)
      else commit('setActiveObjectId')
    },
    setActiveObjectId ({commit}, id) {
      commit('setActiveObjectId', id)
    },
    setWindowForActiveObject ({ commit }, window) {
      commit('setWindowForActiveObject', window)
    },
    getClassifiersForObject ({ commit, state }, config = {}) {
      let objectId = config.params.object_id
      if (!(objectId in state.templatesClassifiersForObjects))
        return getResponseAxios('objects/list_classifier/', config)
          .then(response => {
            commit('addClassifier', { objectId: objectId, classifiers: response.data, })
            return Promise.resolve(response)
          })
          .catch(error => { return Promise.reject(error) })
    },
    getRelationsForObjects ({ commit, state, getters }, config = {}) {
      if(!getters.relationsBetweenTwoObjects({
        objectId1: config.params.object_1_id,
        objectId2: config.params.object_2_id,
      }))
        return getResponseAxios('objects/relations/', config)
          .then(response => { commit('addRelations', {
            objectId1: config.params.object_1_id,
            objectId2: config.params.object_2_id,
            relations: response.data
          }) })
          .catch(() => {})
    },
    findObjectOnServer({ commit, state }, config = {}) {
      let searchTree = state.workAreaAboveObjects.find(object => object.tempId === state.activeObjectId)
      return postResponseAxios('objects/search', searchTree.searchTree, config)
        .then(response => {
          commit('findObjectOnServer', response.data)
          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) })
},
  }
}
