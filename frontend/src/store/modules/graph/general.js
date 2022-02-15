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
    graphNode: state => id => state.graph.nodes.find(o => o.id === id),
    graphEdges: state => state.graph.edges,
    graphEdge: state => id => state.graph.edges.find(o => o.id === id),
    graphObjectByIds: state => ids => state.graph.nodes.find(o => ids.every(id => o.object.ids.includes(id))),
    graphRelations: state => state.graph.edges,
    graphObjectsRelation: state => ids => state.graph.edges.find(r => [r.from, r.to].every(v => ids.includes(v)))
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
      commit('clearSelectedGraphObjects') // ToDo: Избавиться от массива выбранных объектов.
    },
    reorderGraph({ commit }) {
      commit('reorderGraph')
    },
    reorderChoosingObjects({commit}) {
      commit('reorderChoosingObjects')
    }, // ToDo: Объединить две функции упорядочивания. Вынести запуск Лодера в экшен.
    deleteObjectFromGraph({commit}, object) {
      commit('deleteObjectFromGraph', object)
    },
  }
}

