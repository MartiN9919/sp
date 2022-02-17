import axios from '@/plugins/axiosSettings'
import {Node, Edge} from "@/components/Graph/WorkSpace/lib/graph"

export default {
  state: {
    timeline: [],
  },
  getters: {
    timeline: state => callTime => state.timeline.find(t => t.date === callTime),
    nodes: state => [...new Set(state.timeline.map(t => t.nodes).flat(1))],
    edges: state => [...new Set(state.timeline.map(t => t.edges).flat(1))],
  },
  mutations: {
    createTimeLine: (state, timeline) => state.timeline.push(timeline),
    addNodeToTimeLine: (state, {node, callTime}) => state.timeline.find(t => t.date === callTime).nodes.push(node),
    addEdgeToTimeLine: (state, {edge, callTime}) => state.timeline.find(t => t.date === callTime).edges.push(edge),
  },
  actions: {
    createTimeLine({getters, commit}, callTime) {
      commit('createTimeLine', {
        date: callTime,
        nodes: Array.from(getters.graphNodes),
        edges: Array.from(getters.graphEdges),
      })
    },
    createNode({getters, commit}, {object, callTime}) {
      let findNode = getters.nodes.find(n => n.id === object.id)
      if(!findNode) {
        const node = new Node(object)
        commit('addNodeToTimeLine', {node, callTime})
        return node
      } else {
        return Object.assign(findNode, {entity: object})
      }
    },
    createEdge({getters, commit}, {relation, callTime}) {
      let findEdge = getters.edges.find(n => n.id === relation.id)
      if(!findEdge) {
        const edge = new Edge(relation)
        commit('addEdgeToTimeLine', {edge, callTime})
        return edge
      } else {
        return Object.assign(findEdge, {entity: relation})
      }
    },
    createNodes({dispatch}, {objects, callTime}) {
      return Promise.all(objects.map(async o => await dispatch('createNode', {object: o, callTime})))
    },
    createEdges({dispatch}, {relations, callTime}) {
      return Promise.all(relations.map(async r => await dispatch('createEdge', {relation: r, callTime})))
    },
    addObjectsToGraph({getters, dispatch}, {payload}) {
      const callTime = new Date()
      const requestObjects = Array.isArray(payload) ? payload : [payload]
      dispatch('createTimeLine', callTime)
      dispatch('getObjectsFromServer', requestObjects).then(entityNodes => {
        dispatch('createNodes', {objects: entityNodes.map(n => n.value || []), callTime}).then(nodes => {
          dispatch('getRelationsFromServer', nodes.map(n => n.entity)).then(entityEdges => {
            nodes.forEach((node, i) => {
              const relations = entityEdges[i].value || []
              const props = requestObjects[i].props
              dispatch('addNodeToGraph', {node, relations, props})
              dispatch('createEdges', {relations, callTime}).then(edges =>
                edges.forEach(edge => dispatch('addEdgeToGraph', edge))
              )
            })
          })
        })
      })
    },
    async addRelationToGraph({dispatch}, {from, to}) {
      const callTime = new Date()
      dispatch('createTimeLine', callTime)
      await dispatch('getRelationFromServer', {from, objects: [to]}).then(relations => {
        dispatch('createEdges', {relations, callTime}).then(edges =>
          edges.forEach(edge => dispatch('addEdgeToGraph', edge))
        )
      })
    },
    async getRelationsBtwObjects({getters, dispatch}, objects) {
      let config = {}
      if(objects.length === 2)
        config.params = {
          object_id_1: objects[0].ids.object_id,
          object_id_2: objects[1].ids.object_id,
          rec_id_1: objects[0].ids.rec_id,
          rec_id_2: objects[1].ids.rec_id
        }
      return await axios.get('objects/objects_relation/', config)
        .then(response => {
          dispatch('addObjectsToGraph', {payload: response.data})
          return Promise.resolve()
        })
        .catch(e => { return Promise.reject(e) })
    }
  }
}
