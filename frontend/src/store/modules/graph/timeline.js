import {Node, Edge} from "@/components/Graph/WorkSpace/lib/graph"

export default {
  state: {
    point: null,
    timeline: [],
  },
  getters: {
    timeline: state => state.timeline,
    timelineNodes: state => callTime => state.timeline.find(t => t.date === callTime).nodes,
    timelineEdges: state => callTime => state.timeline.find(t => t.date === callTime).edges,
    timelinePoint: state => state.timeline.find(t => t.date === state.point),
    timelineDiff: state => {
      const index = state.timeline.findIndex(t => t.date === state.point)
      const point = state.timeline[index]
      const prevPoint = state.timeline[index - 1]
      if(index > 0) {
        const diff = (name) => point[name].filter(e => !prevPoint[name].includes(e))
        return {
          nodes: diff('nodes').concat(point.updatedNodes),
          edges: diff('edges').concat(point.updatedEdges),
        }
      } else if(index === 0) {
        return {
          nodes: point.nodes.concat(point.updatedNodes),
          edges: point.edges.concat(point.updatedEdges)
        }
      } else {
        return null
      }
    },
    nodes: state => [...new Set(state.timeline.map(t => t.nodes).flat(1))],
    edges: state => [...new Set(state.timeline.map(t => t.edges).flat(1))],
  },
  mutations: {
    setPoint: (state, date) => state.point = date,
    createTimeLine: (state, timeline) => state.timeline.push(timeline),
    addNodeToTimeLine: (state, {node, callTime, updated=false}) =>
      state.timeline.find(t => t.date === callTime)[updated ? 'updatedNodes' : 'nodes'].push(node),
    addEdgeToTimeLine: (state, {edge, callTime, updated=false}) =>
      state.timeline.find(t => t.date === callTime)[updated ? 'updatedEdges' : 'edges'].push(edge),
    deleteNodeFromTimeLine: (state, {node, edges, callTime}) => {
      const point = state.timeline.find(t => t.date === callTime)
      point.updatedNodes.push(node)
      point.updatedEdges = point.updatedEdges.concat(edges)
    }
  },
  actions: {
    setPoint({commit}, date) {
      commit('setPoint', date)
    },
    goToTimeline({commit}, point) {
      commit('createTimeLine', {
        action: {
          name: 'goToTimeline',
          payload: point.date.toLocaleString('ru-RU', {
            dateStyle: "medium",
            timeStyle: "medium"
          }).split(',').reverse().join(' ')
        },
        date: new Date(),
        nodes: [...point.nodes],
        edges: [...point.edges],
        updatedNodes: [...point.nodes],
        updatedEdges: [...point.edges]
      })
      commit('clearGraph')
      point.nodes.forEach(node => {
        commit('addNode', node)
      })
      point.edges.forEach(edge => {
        commit('addEdge', edge)
      })
    },
    createTimeLine({getters, commit}, {callTime, action}) {
      commit('createTimeLine', {
        action,
        date: callTime,
        nodes: Array.from(getters.graphNodes),
        edges: Array.from(getters.graphEdges),
        updatedNodes: [],
        updatedEdges: []
      })
    },
    createNode({getters, commit}, {object, callTime}) {
      let findNode = getters.timelineNodes(callTime).find(n => n.id === object.id)
      const node = findNode ? Object.assign(findNode, {entity: object}) : new Node(object)
      commit('addNodeToTimeLine', {node, callTime, updated: !!findNode})
      return node
    },
    createEdge({getters, commit}, {relation, callTime}) {
      let findEdge = getters.timelineEdges(callTime).find(e => e.id === relation.id)
      const edge = findEdge ? Object.assign(findEdge, {entity: relation}) : new Edge(relation)
      commit('addEdgeToTimeLine', {edge, callTime, updated: !!findEdge})
      return edge
    },
    deleteNode({getters, commit, dispatch}, node) {
      const callTime = new Date()
      dispatch('createTimeLine', {callTime, action: {name: 'deleteNode', payload: node.entity.title}})
      const edges = getters.graphEdges.filter(edge => [edge.to, edge.from].includes(node.id))
      commit('deleteNodeFromTimeLine', {node, edges, callTime})
      commit('deleteNode', node)
    },
    deleteSelectedNodes({getters, commit, dispatch}) {
      const callTime = new Date()
      dispatch('createTimeLine', {callTime, action: {name: 'deleteSelectedNodes'}})
      getters.selectedNodes.forEach(node => {
        const edges = getters.graphEdges.filter(edge => [edge.to, edge.from].includes(node.id))
        commit('deleteNodeFromTimeLine', {node, edges, callTime})
      })
      commit('deleteSelectedNodes')
    },
    clearGraph({getters, commit, dispatch}, timeline=true) {
      const callTime = new Date()
      if(timeline) {
        dispatch('createTimeLine', {callTime, action: {name: 'clearGraph'}})
      }
      commit('clearSelectedNodes')
      getters.graphNodes.forEach(node => {
        const edges = getters.graphEdges.filter(edge => [edge.to, edge.from].includes(node.id))
        if(timeline){
          commit('deleteNodeFromTimeLine', {node, edges, callTime})
        }
      })
      commit('clearGraph')
    },
    createNodes({dispatch}, {objects, callTime}) {
      return Promise.all(objects.map(async o => await dispatch('createNode', {object: o, callTime})))
    },
    createEdges({dispatch}, {relations, callTime}) {
      return Promise.all(relations.map(async r => await dispatch('createEdge', {relation: r, callTime})))
    }
  }
}
