import axios from '@/plugins/axiosSettings'

export default {
  state: {
    selectedGraphObjects: [],
    lastAddedObjects: [],
    lastAddedRelations: []
  },
  getters: {
    selectedGraphObjects: state => state.selectedGraphObjects,
    inSelectedGraphObject: state => object => state.selectedGraphObjects.includes(object),
    lastAddedObjects: state => state.lastAddedObjects,
    inLastAddedObjects: state => id => state.lastAddedObjects.includes(id),
    lastAddedRelations: state => state.lastAddedRelations,
    inLastAddedRelations: state => id => state.lastAddedRelations.includes(id)
  },
  mutations: {
    clearSelectedGraphObjects: (state) => state.selectedGraphObjects = [],
    addSelectedGraphObject: (state, object) => state.selectedGraphObjects.push(object),
    deleteSelectedGraphObject: (state, object) => {
      const positionObject = state.selectedGraphObjects.findIndex(choosingNode => choosingNode.id === object.id)
      if (positionObject !== -1)
        state.selectedGraphObjects.splice(positionObject, 1)
    },
    setLastAddedObjects: (state, objects) => state.lastAddedObjects = objects,
    setLastAddedRelations: (state, relations) => state.lastAddedRelations = relations
  },
  actions: {
    setLastAddedObjects({ commit }, objects) { commit('setLastAddedObjects', objects) },
    setLastAddedRelations({ commit }, relations) { commit('setLastAddedRelations', relations) },
    addSelectedGraphObject({ getters, commit }, object) {
      if(!getters.inSelectedGraphObject(object))
        commit('addSelectedGraphObject', object)
    },
    deleteSelectedGraphObject({ commit }, object) { commit('deleteSelectedGraphObject', object) },
    clearSelectedGraphObjects({ commit }) { commit('clearSelectedGraphObjects') },
    async addToGraphFromServer({getters, dispatch}, {payload}) {
      for(const { object_id, rec_id, props=null } of Array.isArray(payload) ? payload : [payload]) {
        const objects = getters.graphObjects.map(o => Object.assign({object_id: o.object.object.id, rec_id: o.object.recId}))
        await Promise.all([
          dispatch('getObjectFromServer', {object_id, rec_id}),
          dispatch('getRelationFromServer', Object.assign({object_id, rec_id}, {objects: objects}))
        ])
          .then(async r => {
            await dispatch('addToGraph', {object: Object.assign(r[0], {props: props}), relations: r[1]})
              .then(result => {

              })
              .catch(error => console.log('error', error))
          })
      }
    },
    async getRelationsBtwObjects({getters, dispatch}, objects) {
      let config = {}
      if(objects.length === 2)
        config.params = {
          object_id_1: objects[0].object.object.id,
          object_id_2: objects[1].object.object.id,
          rec_id_1: objects[0].object.recId,
          rec_id_2: objects[1].object.recId
        }
      return await axios.get('objects/objects_relation/', config)
        .then(response => {
          dispatch('addToGraphFromServer', {payload: response.data})
          return Promise.resolve()
        })
        .catch(e => { return Promise.reject(e) })
    }
  }
}
