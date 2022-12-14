import Graph from "@/components/Graph/WorkSpace/lib/graph"

export default {
  state: {
    screen: null,
    graph: new Graph()
  },
  getters: {
    screen: state => state.screen,
    graph: state => state.graph,
    graphNodes: state => state.graph.nodes,
    graphNode: state => id => state.graph.nodes.find(n => n.id === id),
    graphNodesEntity: state => state.graph.nodes.map(n => n.entity),
    hoverNodes: state => state.graph.nodes.filter(n => n.state.hover),
    selectedNodes: state => state.graph.nodes.filter(n => n.state.selected),
    graphEdges: state => state.graph.edges,
    graphEdge: state => id => state.graph.edges.find(e => e.id === id),
    graphEdgesEntity: state => state.graph.edges.map(e => e.entity),
    hoverEdges: state => state.graph.edges.filter(e => e.state.hover),
  },
  mutations: {
    setScreen: (state, screen) => state.screen = screen,
    addNode: (state, node) => state.graph.nodes.push(node),
    addEdge: (state, edge) => state.graph.edges.push(edge),
    clearGraph: (state) => state.graph.clearGraph(),
    deleteNode: (state, node) => state.graph.removeNode(node),
    deleteSelectedNodes: (state) => state.graph.nodes
      .filter(n => n.state.selected)
      .forEach(n => state.graph.removeNode(n)),
    clearSelectedNodes: (state) => state.graph.nodes.forEach(n => n.state.selected = false),
    reorderNodes: (state, {nodes, position}) => state.graph.reorderGraph(position.x, position.y, nodes),
  },
  actions: {
    setScreen({ commit }, screen) {
      commit('setScreen', screen)
    },
    addNodeToGraph({getters, commit}, {node, props, relations}) {
      if(!getters.graphNode(node.id)) {
        if(!props) {
          const edges = relations.map(r => r.o2.id)
          props = getters.graph.getNewNodePosition(edges, getters.screen.visibleArea())
        }
        node = Object.assign(node, props)
        commit('addNode', node)
      }
    },
    addEdgeToGraph({getters, commit}, edge) {
      if(!getters.graphEdge(edge.id)) {
        commit('addEdge', edge)
      }
    },
    addObjectsToGraph({getters, dispatch}, {payload, action}) {
      const callTime = new Date()
      dispatch('createTimeLine', {callTime, action})
      dispatch('getObjects', payload).then(entityNodes => {
        entityNodes = entityNodes.filter(n => n.status === 'fulfilled').map(n => n.value)
        dispatch('createNodes', {objects: entityNodes, callTime}).then(nodes => {
          dispatch('getRelationsForObjects', nodes.map(n => n.entity)).then(entityEdges => {
            nodes.forEach((node, i) => {
              const relations = entityEdges[i].value || []
              const props = payload[i].props
              dispatch('addNodeToGraph', {node, relations, props})
              dispatch('createEdges', {relations, callTime}).then(edges =>
                edges.forEach(edge => dispatch('addEdgeToGraph', edge))
              )
            })
          })
        })
      })
    },
    addObjectToGraph({getters, dispatch}, {object, action}) {
      const callTime = new Date()
      dispatch('createTimeLine', {callTime, action})
      return dispatch('getObject', object).then(object => {
        return dispatch('createNode', {object, callTime}).then(node => {
          return dispatch('getRelations', {from: object, objects: getters.graphNodesEntity}).then(relations => {
            dispatch('addNodeToGraph', {node, relations})
            dispatch('createEdges', {relations, callTime}).then(edges =>
              edges.forEach(edge => dispatch('addEdgeToGraph', edge))
            )
            return node
          })
        })
      })
    },
    addRelationToGraph({dispatch}, {from, to}) {
      const callTime = new Date()
      dispatch('createTimeLine', {
        callTime,
        action: {
          name: 'addRelationToGraph',
          payload: `${to.title} ?? ${from.title}`
        }
      })
      return dispatch('getRelation', {from, to}).then(relation => {
        return dispatch('createEdge', {relation, callTime}).then(edge => {
          dispatch('addEdgeToGraph', edge)
          return edge
        })
      })
    },
    clearSelectedNodes({commit}) {
      commit('clearSelectedNodes')
    },
    reorderNodes({getters, commit}, nodes=null) {
      let position
      if(Array.isArray(nodes)) {
        position = getters.graph.getNodesCenter(nodes)
      } else {
        nodes = getters.graphNodes
        position = getters.screen.visibleArea()
        position = {x: position.x - position.width / 2, y: position.y - position.height / 2}
      }
      commit('reorderNodes', {position, nodes})
    },
  }
}

