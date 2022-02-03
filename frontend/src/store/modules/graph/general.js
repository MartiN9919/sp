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
    graphObjects: state => state.graph.nodes,
    graphObject: state => id => state.graph.nodes.find(o => o.id === id),
    graphObjectByIds: state => ids => state.graph.nodes.find(o => ids.every(id => o.object.ids.includes(id))),
    graphRelations: state => state.graph.edges,
    graphObjectsRelation: state => ids => state.graph.edges.find(r => [r.from, r.to].every(v => ids.includes(v)))
  },
  mutations: {
    setScreen: (state, screen) => state.screen = screen,
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
    updateObjectFromGraph: (state, {object, fields}) => state.graph.updateNode(object, fields) // ToDo: Избавиться
  },
  actions: {
    setScreen({ commit }, screen) {
      commit('setScreen', screen)
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
    updateObjectFromGraph({commit}, {object, fields}) { // ToDo: Избавиться от этого
      commit('updateObjectFromGraph', {object, fields})
    },
    async addToGraph({getters, dispatch}, {object, relations}) {
      if(object.props === null) {
        const startPosition = getters.screen.getStartPosition() // ToDo: Установка стартовой позиции относительно связей

        object.props = Object.assign({size: 300}, startPosition)
      }
      const addedObject = await dispatch('addObjectToGraph', object)
      let addedRelations = []
      for(let relation of relations) {
        const data = {objects: [object, relation].map(o => [o.object_id, o.rec_id]), relations: relation.relations}
        addedRelations.push(await dispatch('addRelationToGraph', data))
      }
      return {addedObject, addedRelations}
    },
    addObjectToGraph({getters}, object) {
      let editableObject = new GraphObject(object)
      let findObject = getters.graphObject(editableObject.getGeneratedId())
      if(findObject) {
        return Promise.resolve({
          type: 'updateObjectFromGraph',
          object: getters.graph.updateNode(findObject, {object: editableObject})
        })
      } else {
        return Promise.resolve({
          type: 'addObjectToGraph',
          object: getters.graph.createNode({
            id: editableObject.getGeneratedId(),
            object: editableObject,
            x: object.props.x,
            y: object.props.y,
            size: object.props.size
          })
        })
      }
    },
    addRelationToGraph({getters}, {objects, relations}) {
      const graphObjects = objects.map(o => getters.graphObjectByIds(o))
      let findRelation = getters.graphObjectsRelation(Array.from(graphObjects, o => o.id))
      let relation = new GraphRelation(...graphObjects, relations)
      if(findRelation) {
        return Promise.resolve({
          type: 'updateRelationFromGraph',
          relation: getters.graph.updateEdge(findRelation, {relation: relation})
        })
      }
      else {
        return Promise.resolve({
          type: 'addRelationToGraph',
          relation: getters.graph.createEdge(...graphObjects, {
            id: relation.getGeneratedId(),
            relation: relation,
            size: 300
          })
        })
      }
    }
  }
}

class GraphElementStateBase {
  constructor() {
    this.added = false
  }
}

class GraphObjectState extends GraphElementStateBase {
  constructor() {
    super()
    this.selected = false
  }
}

class GraphElementSettingsBase {
  constructor() {
    this.showTooltip = true
    this.showCreateDate = true
  }
}

class GraphObjectSettings extends GraphElementSettingsBase{
  constructor() {
    super()
    this.showTitle = true
    this.showTriggers = true
  }
}

class GraphRelation extends DataBaseRelation {
  constructor(o1, o2, params=[]) {
    super(o1, o2, params)
    this.state = new GraphElementStateBase()
    this.settings = new GraphElementSettingsBase()
  }

  getGeneratedId() {
    return `${this.o1.id}@${this.o2.id}`
  }
}

class GraphObject extends DataBaseObject {
  constructor(object) {
    super(object)
    this.triggers = object.triggers
    this.photo = object.photo || null
    this.state = new GraphObjectState()
    this.settings = new GraphObjectSettings()
  }

  get ids() {
    return [this.object.id, this.recId]
  }

  getGeneratedId() {
    return `${this.object.id}-${this.recId}`
  }
}