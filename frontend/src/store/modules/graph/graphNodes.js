import {postResponseAxios} from '@/plugins/axios_settings'


export default {
  state: {
    choosingObjects: [],
    objectsRelations: [],
  },
  getters: {
    choosingObjects: state => {
      return state.choosingObjects
    },
    choosingObject: state => recId => {
      return state.choosingObjects.find(object => object.rec_id === recId)
    },
    objectsRelations: state => {
      return state.objectsRelations
    },
    relations: state => ids => {
      return state.objectsRelations.find(relations =>
        ((relations.object_id1 === ids.object_id1 && relations.rec_id1 === ids.rec_id1) &&
          (relations.object_id2 === ids.object_id2 && relations.rec_id2 === ids.rec_id2)) ||
        ((relations.object_id1 === ids.object_id2 && relations.rec_id1 === ids.rec_id2) &&
          (relations.object_id2 === ids.object_id1 && relations.rec_id2 === ids.rec_id1))
      )
    },
    lastObject: state => {
      let object = state.choosingObjects[state.choosingObjects.length - 1]
      return object ? object : null
    }
  },
  mutations: {
    addChoosingObject: (state, choosingObject) => {
      let findObjectIndex = state.choosingObjects.findIndex(object => object.object_id === choosingObject.object_id && object.rec_id === choosingObject.rec_id)
      if(findObjectIndex !== -1)
        state.choosingObjects.splice(findObjectIndex, 1)
      state.choosingObjects.push(choosingObject)
    },
    addObjectsRelation: (state, objectsRelation) => {
      let findRelation = state.objectsRelations.find(relations =>
        ((relations.object_id1 === objectsRelation.object_id1 && relations.rec_id1 === objectsRelation.rec_id1) &&
          (relations.object_id2 === objectsRelation.object_id2 && relations.rec_id2 === objectsRelation.rec_id2)) ||
        ((relations.object_id1 === objectsRelation.object_id2 && relations.rec_id1 === objectsRelation.rec_id2) &&
          (relations.object_id2 === objectsRelation.object_id1 && relations.rec_id2 === objectsRelation.rec_id1))
      )
      if (findRelation)
        findRelation.relations.push(objectsRelation.relations)
      else state.objectsRelations.push(objectsRelation)
    },
    removeChoosingObject: (state, {object_id, rec_id}) => {
      let removeIndex = state.choosingObjects.findIndex(
        object => object.object_id === object_id && object.rec_id === rec_id
      )
      if (removeIndex !== -1) {
        state.choosingObjects.splice(removeIndex, 1)
      }
    }
  },
  actions: {
    addChoosingObject({getters, commit, dispatch}, choosingObject) {
      let request = {
        object_id: choosingObject.object_id,
        rec_id: choosingObject.rec_id,
        objects: Array.from(getters.choosingObjects, object => {
          return {object_id: object.object_id, rec_id: object.rec_id}
        })
      }
      commit('addChoosingObject', choosingObject)
      dispatch('getRelationFromServer', {params: request})
    },
    addChoosingRelation({commit}, {object, relations}) {
      for(let relation of relations)
        commit('addObjectsRelation', {
          object_id1: object.o1,
          rec_id1: object.r1,
          object_id2: object.o2,
          rec_id2: object.r2,
          relations: relation,
        })
    },
    getObjectRelations({commit}, {params, config = {}}) {
      return postResponseAxios('objects/object_relation/', params, config)
        .then(response => {
          for (let relation of response.data)
            commit('addObjectsRelation', {
              object_id1: params.object_id,
              rec_id1: params.rec_id,
              object_id2: relation.object_id,
              rec_id2: relation.rec_id,
              relations: relation.relations,
            })
        })
        .catch(error => {
        })
    },
    removeChoosingObject({commit,}, {object_id, rec_id}) {
      commit('removeChoosingObject', {object_id, rec_id})
    },
  },
}