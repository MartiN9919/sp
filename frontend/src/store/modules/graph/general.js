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
    reorderGraph: (state) => {
      const startPosition = state.screen.getStartPosition()
      state.graph.reorderGraph(startPosition.x, startPosition.y)
    },
    reorderChoosingObjects: (state) => {
      const center = state.graph.getNodesCenter(state.selectedGraphObjects)
      state.graph.reorderGraph(center.x, center.y, state.selectedGraphObjects)
    }, // ToDo: Объединить две функции упорядочивания. Вынести запуск Лодера в экшен.
    deleteObjectFromGraph: (state, object) => state.graph.removeNode(object),
  },
  actions: {
    setScreen({ commit }, screen) {
      commit('setScreen', screen)
    },
    addNodeToGraph({getters, commit}, {node, callTime}) {
      if(!getters.graphNode(node.id)) {
        commit('addNode', node)
      }
      commit('addNodeToTimeLine', {node, callTime})
    },
    addEdgeToGraph({getters, commit}, {edge, callTime}) {
      if(!getters.graphEdge(edge.id)) {
        commit('addEdge', edge)
      }
      commit('addEdgeToTimeLine', {edge, callTime})
    },
    clearGraph({commit}) {
      commit('clearGraph')
    },
    reorderGraph({ commit }) {
      commit('reorderGraph')
    },
    reorderChoosingObjects({commit}) {
      commit('reorderChoosingObjects')
    } // ToDo: Объединить две функции упорядочивания. Вынести запуск Лодера в экшен.
  }
}

