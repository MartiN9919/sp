import { getResponseAxios } from '@/plugins/axios_settings'

export default {
  state: {
    relationsBetweenTwoObjects: [],
  },
  getters: {
    relationsTwoObjects: state => objectsId => {
      return state.relationsBetweenTwoObjects.find(object =>
        ((object.firstId === objectsId.firstId && object.secondId === objectsId.secondId) ||
          (object.firstId === objectsId.secondId && object.secondId === objectsId.firstId))
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
      if(!getters.relationsTwoObjects({ firstId: config.params.object_1_id, secondId: config.params.object_2_id, }))
        return getResponseAxios('objects/relations/', config)
          .then(response => { commit('addRelations', {
            firstId: config.params.object_1_id,
            secondId: config.params.object_2_id,
            relations: response.data
          }) })
          .catch(() => {})
    },
  },
}