import axios from '@/plugins/axiosSettings'
import {Node, Edge} from "@/components/Graph/WorkSpace/lib/graph"

export default {
  state: {
    selectedGraphObjects: [],
    lastAddedObjects: [],
    lastAddedRelations: [],
    timeline: [],
    callTime: null,
  },
  getters: {
    timeline: state => callTime => state.timeline.find(t => t.date === callTime),
    nodes: state => (callTime=null) => {
      const converter = timeline => Array.from(timeline, t => t.nodes).flat(1)
      if(callTime) {
        return converter(state.timeline.filter(t => t.date <= callTime))
      } else {
        return converter(state.timeline)
      }
    },
    edges: state => (callTime=null) => {
      const converter = timeline => Array.from(timeline, t => t.edges).flat(1)
      if(callTime) {
        return converter(state.timeline.filter(t => t.date <= callTime))
      } else {
        return converter(state.timeline)
      }
    },
    selectedGraphObjects: state => state.selectedGraphObjects,
    inSelectedGraphObject: state => object => state.selectedGraphObjects.includes(object),
    lastAddedObjects: state => state.lastAddedObjects,
    inLastAddedObjects: state => id => state.lastAddedObjects.includes(id),
    lastAddedRelations: state => state.lastAddedRelations,
    inLastAddedRelations: state => id => state.lastAddedRelations.includes(id)
  },
  mutations: {
    createTimeLine: (state, callTime) => state.timeline.push({date: callTime, nodes: [], edges: []}),
    addNodeToTimeLine: (state, {node, callTime}) => state.timeline.find(t => t.date === callTime).nodes.push(node),
    addEdgeToTimeLine: (state, {edge, callTime}) => state.timeline.find(t => t.date === callTime).edges.push(edge),
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
    createTimeLine({commit}, callTime) { commit('createTimeLine', callTime) },
    createNode({getters, commit}, {object, props}) {
      let findNode = getters.nodes().find(n => n.id === object.getGeneratedId())
      const node = findNode ? Object.assign(findNode, {entity: object}) : new Node(object, props)
      return Promise.resolve(node)
    },
    createEdge({getters, commit}, {relation}) {
      let findEdge = getters.edges().find(n => n.id === relation.getGeneratedId())
      const edge = findEdge ? Object.assign(findEdge, {entity: relation}) : new Edge(relation)
      return Promise.resolve(edge)
    },
    async addToGraph({getters, commit, dispatch}, {payload}) {
      const callTime = new Date()
      commit('createTimeLine', callTime)
      for(const {object_id, rec_id, props=getters.screen.getStartPosition()} of Array.isArray(payload) ? payload : [payload]) {
        dispatch('getObjectFromServer', {object_id, rec_id})
          .then(object => {
            dispatch('getRelationFromServer', {from: object, objects: Array.from(getters.nodes(), n => n.entity)})
              .then(relations => relations.forEach(relation =>
                dispatch('createEdge', {relation, callTime})
                  .then(edge => dispatch('addEdgeToGraph', {edge, callTime}))
              ))
            dispatch('createNode', {object, props, callTime})
              .then(node => dispatch('addNodeToGraph', {node, callTime}))
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
          dispatch('addToGraph', {payload: response.data})
          return Promise.resolve()
        })
        .catch(e => { return Promise.reject(e) })
    }
  }
}
