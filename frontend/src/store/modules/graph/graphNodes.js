import axios from '@/plugins/axiosSettings'
import Graph from "@/components/Graph/WorkSpace/lib/graph"
import UserSetting from '@/store/addition'
import {DataBaseObject, DataBaseRelation} from '@/store/modules/graph/graphMenu/recordEditor'

class GlobalSettings {
  constructor() {
    this.linkHighlighting = {
      title: 'Подсветка связей',
      subTitle: 'Подсвечивать объекты и связи при наведении',
      state: new UserSetting('linkHighlighting', true)
    }
    this.showGlobalTitle = {
      title: 'Подписи объектов',
      subTitle: 'Подпись под объектами на графе',
      state: new UserSetting('showGlobalTitle', true)
    }
    this.showGlobalTooltipObject = {
      title: 'Заголовки объектов',
      subTitle: 'Отображение заголовка над объектами',
      state: new UserSetting('showGlobalTooltipObject', true)
    }
    this.showGlobalTriggers = {
      title: 'Уведомления о триггерах',
      subTitle: 'Управление отображением значка уведомления о срабатывании триггеров',
      state: new UserSetting('showGlobalTriggers', true)
    }
    this.showGlobalDateObject = {
      title: 'Время записи объекта',
      subTitle: 'Управление отображением даты классификатора',
      state: new UserSetting('showGlobalDateObject', true)
    }
    this.showGlobalTooltipRelation = {
      title: 'Заголовки связей',
      subTitle: 'Отображение заголовка над связями',
      state: new UserSetting('showGlobalTooltipRelation', true)
    }
    this.showGlobalDateRelation = {
      title: 'Время записи связи',
      subTitle: 'Управление отображением даты связи',
      state: new UserSetting('showGlobalDateRelation', true)
    }
  }
}

export default {
  state: {
    screen: null,
    classifiersSettings: new UserSetting('classifiersSettings', []),
    globalDisplaySettings: new GlobalSettings(),
    graph: new Graph(),
    graphObjects: {},
    selectedGraphObjects: [],
    lastAddedObjects: [],
    lastAddedRelations: []
  },
  getters: {
    graphObjects: state => state.graph.nodes,
    graphRelations: state => state.graph.edges,
    classifiersSettings: state => state.classifiersSettings.value,
    globalDisplaySettings: state => state.globalDisplaySettings,
    globalDisplaySettingValue: state => identifier => state.globalDisplaySettings[identifier].state.value,
    selectedGraphObjects: state => state.selectedGraphObjects,
    inSelectedGraphObject: state => object => state.selectedGraphObjects.includes(object),
    lastAddedObjects: state => state.lastAddedObjects,
    inLastAddedObjects: state => id => state.lastAddedObjects.includes(id),
    lastAddedRelations: state => state.lastAddedRelations,
    inLastAddedRelations: state => id => state.lastAddedRelations.includes(id)
  },
  mutations: {
    setScreen: (state, screen) => state.screen = screen,
    deleteObjectFromGraph: (state, object) => state.graph.removeNode(object),
    updateObjectFromGraph: (state, {object, fields}) => state.graph.updateNode(object, fields),
    updateRelationFromGraph: (state, {relation, fields}) => state.graph.updateEdge(relation, fields),
    changeGlobalSettingState: (state, {id, value}) => state.globalDisplaySettings[id].state.value = value,
    setClassifiersSettings: (state, classifierId) => state.classifiersSettings.switch(classifierId),
    clearSelectedGraphObjects: (state) => state.selectedGraphObjects = [],
    reorderGraph: (state) => state.graph.reorderGraph(state.screen.getStartPosition().x, state.screen.getStartPosition().y),
    reorderChoosingObjects: (state) => {
      const center = state.graph.getNodesCenter(state.selectedGraphObjects)
      state.graph.reorderGraph(center.x, center.y, state.selectedGraphObjects)
    },
    clearGraph: (state) => state.graph.clearGraph(),
    addSelectedGraphObject: (state, object) => state.selectedGraphObjects.push(object),
    deleteSelectedGraphObject: (state, object) => {
      const positionObject = state.selectedGraphObjects.findIndex(choosingNode => choosingNode.id === object.id)
      if (positionObject !== -1)
        state.selectedGraphObjects.splice(positionObject, 1)
    },
    addObjectToGraph: (state, {editableObject, position, size}) => {
      state.graph.createNode({
        id: editableObject.getGeneratedId(),
        object: editableObject,
        size: size, x: position.x, y: position.y
      })
    },
    addRelationToGraph: (state, {objects, relation, noMove}) => {
      state.graph.createEdge(objects[0], objects[1], {id: relation.getGeneratedId(), relation: relation, size: 300, noMove: noMove})
    },
    setLastAddedObjects: (state, objects) => state.lastAddedObjects = objects,
    setLastAddedRelations: (state, relations) => state.lastAddedRelations = relations
  },
  actions: {
    setLastAddedObjects({ commit }, objects) { commit('setLastAddedObjects', objects) },
    setLastAddedRelations({ commit }, relations) { commit('setLastAddedRelations', relations) },
    setScreen({ commit }, screen) { commit('setScreen', screen) },
    addSelectedGraphObject({ getters, commit }, object) {
      if(!getters.inSelectedGraphObject(object))
        commit('addSelectedGraphObject', object)
    },
    deleteSelectedGraphObject({ commit }, object) { commit('deleteSelectedGraphObject', object) },
    clearSelectedGraphObjects({ commit }) { commit('clearSelectedGraphObjects') },
    reorderGraph({ commit }) { commit('reorderGraph') },
    reorderChoosingObjects({commit}) { commit('reorderChoosingObjects') },
    clearGraph({commit}) {
      commit('clearGraph')
      commit('clearSelectedGraphObjects')
    },
    changeGlobalSettingState({ commit }, payload) { commit('changeGlobalSettingState', payload) },
    setClassifiersSettings({ getters, commit }, id) { commit('setClassifiersSettings', id) },
    updateRelationFromGraph({commit}, {relation, fields}) { commit('updateRelationFromGraph', {relation, fields}) },
    deleteObjectFromGraph({commit}, object) { commit('deleteObjectFromGraph', object) },
    updateObjectFromGraph({commit}, {object, fields}) { commit('updateObjectFromGraph', {object, fields}) },
    async addToGraph({getters, dispatch}, {payload, noMove=false}) {
      let lastAddedObjects = []
      let lastAddedRelations = []
      for(const object of Array.isArray(payload) ? payload : [payload]) {
        const objects = getters.graphObjects.map(o => Object.assign({object_id: o.object.object.id, rec_id: o.object.recId}))
        const payloadObject = {object_id: object.object_id, rec_id: object.rec_id}
        await Promise.all([
          dispatch('getObjectFromServer', payloadObject),
          dispatch('getRelationFromServer', Object.assign(payloadObject, {objects: objects}))
        ])
          .then(async r => {
            await dispatch('addObjectToGraph', Object.assign({object: r[0]}, object))
              .then(value => {
                if(value.type === 'addObjectToGraph') {
                  lastAddedObjects.push(value.object.getGeneratedId())
                }
              })
          for(let relation of r[1]) {
            let object = {o1: r[0].object_id, r1: r[0].rec_id, o2: relation.object_id, r2: relation.rec_id}
            dispatch('addRelationToGraph', {object: object, relations: relation.relations, noMove: noMove})
              .then(value => {
                if(value.type === 'addRelationToGraph') {
                  lastAddedRelations.push(value.relation.getGeneratedId())
                }
              })
          }
        })
      }
      dispatch('setLastAddedObjects', lastAddedObjects)
      dispatch('setLastAddedRelations', lastAddedRelations)
    },
    addObjectToGraph({state, getters, commit, dispatch}, {object, size=300, position=state.screen.getStartPosition()}) {
      let editableObject = new GraphObject(object)
      let findNode = getters.graphObjects.find(o => o.id === editableObject.getGeneratedId())
      if(findNode) {
        const fields = {object: Object.assign(editableObject, {show: true})}
        dispatch('updateObjectFromGraph', {object: findNode, fields})
        return Promise.resolve({type: 'updateObjectFromGraph', object: findNode})
      } else {
        commit('addObjectToGraph', {editableObject, position, size})
        return Promise.resolve({type: 'addObjectToGraph', object: editableObject})
      }
    },
    addRelationToGraph({getters, commit, dispatch}, {object, relations, noMove}) {
      let object1 = getters.graphObjects.find(r => r.object.object.id === object.o1 && r.object.recId === object.r1)
      let object2 = getters.graphObjects.find(r => r.object.object.id === object.o2 && r.object.recId === object.r2)
      let relation = new GraphRelation(object1, object2, relations)
      let findRelation = getters.graphRelations.find(r => [r.from, r.to].every(v => [object1.id, object2.id].includes(v)))
      if(findRelation) {
        dispatch('updateRelationFromGraph', {relation: findRelation, fields: {relation: relation}})
        return Promise.resolve({type: 'updateRelationFromGraph', relation: findRelation})
      }
      else {
        commit('addRelationToGraph', {objects: [object1, object2], relation: relation, noMove: noMove})
        return Promise.resolve({type: 'addRelationToGraph', relation: relation})
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

class GraphRelation extends DataBaseRelation {
  constructor(o1, o2, params=[]) {
    super(o1, o2, params)
    this.showTooltip = true
    this.showCreateDate = true
  }

  getGeneratedId() {
    return `${this.o1.id}@${this.o2.id}`
  }
}

class GraphObject extends DataBaseObject {
  constructor(object) {
    super(object)
    this.triggers = object.triggers
    if(object.hasOwnProperty('photo'))
      this.photo = object.photo
    this.showTitle = true
    this.showTooltip = true
    this.showTriggers = true
    this.showCreateDate = true
    this.show = false
  }

  getGeneratedId() {
    return `${this.object.id}-${this.recId}`
  }
}

