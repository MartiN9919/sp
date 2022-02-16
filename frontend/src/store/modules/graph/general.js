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
    addNode: (state, node) => state.graph.createNode(node),
    addEdge: (state, edge) => state.graph.createEdge(edge),
    clearGraph: (state) => state.graph.clearGraph(),
    reorderGraph: (state, {nodes, position}) => state.graph.reorderGraph(position.x, position.y, nodes),
    deleteObjectFromGraph: (state, object) => state.graph.removeNode(object),
  },
  actions: {
    setScreen({ commit }, screen) {
      commit('setScreen', screen)
    },
    addNodeToGraph({getters, commit}, {node, props, relations}) {
      if(!getters.graphNode(node.id)) {
        if(!props) {
          const edges = relations.map(r => r.o2.getGeneratedId())
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
    reorderGraph({getters, commit}, nodes=null) {
      if(nodes) {
        const position = getters.graph.getNodesCenter(nodes)
      } else {
        nodes = getters.graphNodes
        let position = getters.screen.visibleArea()
        position = {x: position.x - position.width / 2, y: position.y - position.height / 2}
      }
      commit('reorderGraph', {position, nodes})
    },
  }
}

