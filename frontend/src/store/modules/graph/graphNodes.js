import { getResponseAxios } from '@/plugins/axios_settings'


export default {
  state: {
    choosingObjects: [],
    objectsRelations: [],
  },
  getters: {
    choosingObjects: state => { return state.choosingObjects },
    objectsRelations: state => { return state.objectsRelations },
    lastObject: state => {
      let object = state.choosingObjects[state.choosingObjects.length - 1]
      return object ? object : null
    }
  },
  mutations: {
    addChoosingObject: (state, choosingObject) => { state.choosingObjects.push(choosingObject) },
    addObjectsRelation: (state, objectsRelation) => { state.objectsRelations.push(objectsRelation) },
    removeChoosingObject: (state, {object_id, rec_id}) => {
      let removeIndex = state.choosingObjects.findIndex(
          object => object.object_id === object_id && object.rec_id === rec_id
      )
      if(removeIndex !== -1){
        state.choosingObjects.splice(removeIndex, 1)
      }
    }
  },
  actions: {
    addChoosingObject({ commit, }, choosingObject) {
        commit('addChoosingObject', choosingObject)
    },
    removeChoosingObject({ commit, }, {object_id, rec_id}) {
        commit('removeChoosingObject', {object_id, rec_id})
    },
  },
}