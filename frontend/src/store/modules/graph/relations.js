import { getResponseAxios } from '@/plugins/axios_settings'

export default {
  state: {
    relationsBetweenTwoObjects: [],
  },
  getters: {
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
    },
  },
  mutations: {
    addRelations: (state, relations) => { state.relationsBetweenTwoObjects.push(relations) },
  },
  actions: {
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
  },
}