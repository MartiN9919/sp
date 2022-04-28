import {DataBaseObject, DataBaseRelation} from "@/store/modules/graph/general"
import axios from "@/plugins/axiosSettings"
import CONST from "@/plugins/const"

export default {
  state: {
    editableRelation: null,
    editableObjects: null,
    formFile: null,
    turnConflicts: null,
    resolvedConflicts: []
  },
  getters: {
    editableRelation: state => state.editableRelation,
    editableObjects: state => state.editableObjects,
    formFile: state => state.formFile,
    turnConflicts: state => state.turnConflicts,
    resolvedConflicts: state => state.resolvedConflicts
  },
  mutations: {
    setEditableRelation: (state, {relation, document}) => state.editableRelation = {relation, document},
    addNewParamEditableRelation: (state, id) => state.editableRelation.relation.addParam(id),
    deleteNewParamEditableRelation: (state, {id, param}) => state.editableRelation.relation.deleteParam(id, param),

    setEditableObjects: (state, object) => state.editableObjects = [object],
    resetEditableObjects: (state) => state.editableObjects = [state.editableObjects[0]],
    addEditableObjects: (state, object) => state.editableObjects.push(object),
    clearEditableObjects: (state, object) => state.editableObjects = null,
    addNewParamEditableObject: (state, {id, position}) => state.editableObjects[position].addParam(id),
    deleteNewParamEditableObject: (state, {id, param, position}) => state.editableObjects[position].deleteParam(id, param),

    setFormFile: (state, file) => state.formFile = file,
    setTurnConflicts: (state, conflicts) => state.turnConflicts = conflicts,
    addResolvedConflict: (state, resolvedConflict) => {
      let conflict = state.turnConflicts.shift()
      resolvedConflict.id_str = conflict.object.id_str
      resolvedConflict.name = conflict.object.name
      state.resolvedConflicts.push(resolvedConflict)
    },
    clearResolvedConflict: (state) => state.resolvedConflicts = []
  },
  actions: {
    addResolvedConflict({getters, commit}, position) {
      commit('addResolvedConflict', getters.editableObjects[position])
    },
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
    async saveFormFile({getters, commit, dispatch}, file=null) {
      const formFile = file || getters.formFile
      const request = DataBaseObject.arrayRequest(getters.resolvedConflicts, formFile)
      const config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      return await axios.post('objects/load/', request, config)
        .then(r => {
          if(r.data.hasOwnProperty('conflicts')) {
            commit('setFormFile', formFile)
            commit('setTurnConflicts', r.data.conflicts)
          } else if(r.data.hasOwnProperty('result')) {
            commit('clearEditableObjects')
            dispatch('addObjectsToGraph', {
              payload: r.data.result,
              action: {
                name: 'saveFormFile',
                payload: formFile.name
              }
            })
            commit('setFormFile', null)
            commit('setTurnConflicts', null)
            commit('clearResolvedConflict')
          }
          return Promise.resolve(r.data)
        })
        .catch(e => {
          return Promise.reject(e)
        })
    },
    async saveEditableObject({getters, dispatch}, positionObject) {
      const editableObject = getters.editableObjects[positionObject]
      return await axios.post('objects/object/',
        editableObject.getRequestStructure(),
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            'set-cookie': getters.cookieTriggers(getters.editableObjects[positionObject].ids.object_id)
          }
        }
      )
        .then(r => {
          const response = r.data
          if(Array.isArray(response)) {
            dispatch('addEditableObjects', response)
          } else {
            const actionName = editableObject.recId ? 'saveEditableObject' : 'saveObject'
            dispatch('addObjectToGraph', {object: response, action: {name: actionName, payload: response.title}})
              .then(node => dispatch('setEditableObject', node.entity))
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