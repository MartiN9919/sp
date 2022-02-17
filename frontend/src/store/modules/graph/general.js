import Graph from "@/components/Graph/WorkSpace/lib/graph"
import {DataBaseObject, DataBaseRelation} from "@/store/modules/graph/recordEditor"

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
    hoverNodes: state => state.graph.nodes.filter(n => n.state.hover),
    selectedNodes: state => state.graph.nodes.filter(n => n.state.selected),
    graphEdges: state => state.graph.edges,
    graphEdge: state => id => state.graph.edges.find(e => e.id === id),
    hoverEdges: state => state.graph.edges.filter(e => e.state.hover),
    selectedEdges: state => state.graph.edges.filter(e => e.state.selected)
  },
  mutations: {
    setScreen: (state, screen) => state.screen = screen,
    addNode: (state, node) => state.graph.nodes.push(node),
    addEdge: (state, edge) => state.graph.edges.push(edge),
    clearGraph: (state) => state.graph.clearGraph(),
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
    clearGraph({commit}) {
      commit('clearGraph')
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

