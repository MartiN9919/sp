import {DataBaseObject, DataBaseRelation} from "@/store/modules/graph/general"
import axios from "@/plugins/axiosSettings"
import CONST from "@/plugins/const"

export default {
  state: {
    editableRelation: null,
    editableObjects: null,
  },
  getters: {
    editableRelation: state => { return state.editableRelation },
    editableObjects: state => { return state.editableObjects },
  },
  mutations: {
    setEditableRelation: (state, {relation, document}) => state.editableRelation = {relation, document},
    addNewParamEditableRelation: (state, id) => state.editableRelation.relation.addParam(id),
    deleteNewParamEditableRelation: (state, {id, param}) => state.editableRelation.relation.deleteParam(id, param),

    setEditableObjects: (state, object) => state.editableObjects = [object],
    resetEditableObjects: (state) => state.editableObjects = [state.editableObjects[0]],
    addEditableObjects: (state, object) => state.editableObjects.push(object),
    addNewParamEditableObject: (state, {id, position}) => state.editableObjects[position].addParam(id),
    deleteNewParamEditableObject: (state, {id, param, position}) => state.editableObjects[position].deleteParam(id, param)
  },
  actions: {
    setEditableRelation({getters, commit}, {relation, document}) {
      if(relation instanceof DataBaseRelation) {
        commit('setEditableRelation', {relation: _.cloneDeep(relation), document})
      } else {
        commit('setEditableRelation', {relation: new DataBaseRelation(...relation), document})
      }
    },
    addNewParamEditableRelation({commit}, relationId) {
      commit('addNewParamEditableRelation', relationId)
    },
    deleteNewParamEditableRelation({commit}, playLoad) {
      commit('deleteNewParamEditableRelation', playLoad)
    },
    setEditableObject({commit, dispatch}, object) {
      if(object instanceof DataBaseObject) {
        commit('setEditableObjects', object)
      } else {
        if(object.rec_id) {
          dispatch('getObject', object)
            .then(r => commit('setEditableObjects', r))
        } else {
          commit('setEditableObjects', new DataBaseObject(object))
        }
      }
      dispatch('setNavigationDrawerStatus', true)
      dispatch('setActiveTool', 'CreateObjectPage')
    },
    addEditableObjects({getters, commit}, objects) {
      commit('resetEditableObjects')
      const zeroObject = getters.editableObjects[0]
      for(let object of objects) {
        let newObject = new DataBaseObject(Object.assign(object, {recIdOld: zeroObject.recId}))
        newObject.concatParams(zeroObject)
        commit('addEditableObjects', newObject)
      }
    },
    addNewParamEditableObject({commit}, playLoad) {
      commit('addNewParamEditableObject', playLoad)
    },
    deleteNewParamEditableObject({commit}, playLoad) {
      commit('deleteNewParamEditableObject', playLoad)
    },
    async saveEditableObject({getters, dispatch}, positionObject) {
      const editableObject = getters.editableObjects[positionObject]
      return await axios.post('objects/object/',
        editableObject.getRequestStructure(),
        {headers: {
            'Content-Type': 'multipart/form-data',
            'set-cookie': getters.cookieTriggers(getters.editableObjects[positionObject].ids.object_id)
          }}
      )
        .then(r => {
          let response = r.data
          if(Array.isArray(response)) {
            dispatch('addEditableObjects', response)
          }
          else {
            dispatch('addObjectToGraph', {
              object: response,
              action: {
                name: editableObject.recId ? 'saveEditableObject' : 'saveObject',
                payload: response.title
              }
            }).then(node => {
              dispatch('setEditableObject', node.entity)
            })
          }
          return Promise.resolve(r.data)
        })
        .catch(e => { return Promise.reject(e) })
    },
    async saveEditableRelation({getters, dispatch}) {
      let request = Object.assign(
        {doc_rec_id: getters.editableRelation.document?.recId || null},
        getters.editableRelation.relation.getRequestStructure()
      )
      return await axios.post(CONST.API.OBJ.SET_RELATION, request, {})
        .then(() => {
          const relation = [getters.editableRelation.relation.o1, getters.editableRelation.relation.o2]
          dispatch('addRelationToGraph', {from: relation[0], to: relation[1]}).then(edge => {
            dispatch('setEditableRelation',{relation: edge.entity, document: getters.editableRelation.document})
          })
          return Promise.resolve()
        })
        .catch(e => { return Promise.reject(e) })
    }
  }
}