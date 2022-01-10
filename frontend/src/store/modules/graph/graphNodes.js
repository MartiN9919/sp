import axios from '@/plugins/axiosSettings'
import Graph from "@/components/Graph/WorkSpace/lib/graph"
import UserSetting from '@/store/addition'
import {DataBaseObject, DataBaseRelation} from '@/store/modules/graph/graphMenu/recordEditor'

class GlobalSettings {
  constructor() {
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
    this.showRelations = {
      title: 'Отображение связей',
      state: new UserSetting('showRelations', true)
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
  },
  getters: {
    graphObjects: state => state.graph.nodes,
    graphRelations: state => state.graph.edges,
    classifiersSettings: state => state.classifiersSettings.value,
    globalDisplaySettings: state => state.globalDisplaySettings,
    globalDisplaySettingValue: state => identifier => {
      return state.globalDisplaySettings[identifier].state.value
    },
  },
  mutations: {
    setScreen: (state, screen) => state.screen = screen,
    deleteObjectFromGraph: (state, object) => state.graph.removeNode(object),
    updateObjectFromGraph: (state, {object, fields}) => state.graph.updateNode(object, fields),
    updateRelationFromGraph: (state, {relation, fields}) => state.graph.updateEdge(relation, fields),
    changeGlobalSettingState: (state, {id, value}) => state.globalDisplaySettings[id].state.value = value,
    setClassifiersSettings: (state, classifierId) => state.classifiersSettings.switch(classifierId),
    addObjectToGraph: (state, {editableObject, position, size}) => {
      state.graph.createNode({
        id: editableObject.getGeneratedId(),
        object: editableObject,
        size: size, x: position.x, y: position.y
      })
    },
    addRelationToGraph: (state, {objects, relation, noMove}) => {
      state.graph.createEdge(objects[0], objects[1],{relation: relation, size: 600, noMove: noMove})
    },
  },
  actions: {
    setScreen({ commit }, screen) { commit('setScreen', screen) },
    reorderGraph({ state }) {
      state.graph.reorderGraph(state.screen.getStartPosition().x, state.screen.getStartPosition().y)
    },
    changeGlobalSettingState({ commit }, payload) { commit('changeGlobalSettingState', payload) },
    setClassifiersSettings({ getters, commit }, id) { commit('setClassifiersSettings', id) },
    addRelationToGraph({getters, commit, dispatch}, {object, relations, noMove}) {
      let object1 = getters.graphObjects.find(r => r.object.object.id === object.o1 && r.object.recId === object.r1)
      let object2 = getters.graphObjects.find(r => r.object.object.id === object.o2 && r.object.recId === object.r2)
      let relation = new DataBaseRelation(object1, object2, relations)
      let findRelation = getters.graphRelations.find(r => [r.from, r.to].every(v => [object1.id, object2.id].includes(v)))
      if(findRelation)
        dispatch('updateRelationFromGraph', {relation: findRelation, fields: {relation: relation}})
      else
        commit('addRelationToGraph', {objects: [object1, object2], relation: relation, noMove: noMove})
    },
    updateRelationFromGraph({commit}, {relation, fields}) { commit('updateRelationFromGraph', {relation, fields}) },
    deleteObjectFromGraph({commit}, object) { commit('deleteObjectFromGraph', object) },
    updateObjectFromGraph({commit}, {object, fields}) { commit('updateObjectFromGraph', {object, fields}) },
    addObjectToGraph({ state, getters, commit, dispatch }, {recId, objectId, size=600, position=state.screen.getStartPosition(), noMove =false}) {
      dispatch('getObjectFromServer', {params: {record_id: recId, object_id: objectId}})
        .then(r => {
          let editableObject = new GraphObject(r)
          let findNode = getters.graphObjects.find(o => o.id === editableObject.getGeneratedId())
          let relatedObjects = Array.from(getters.graphObjects, o =>
            Object.assign({object_id: o.object.object.id, rec_id: o.object.recId})
          )
          if(findNode)
            dispatch('updateObjectFromGraph', {object: findNode, fields: {object: Object.assign(editableObject, {show: true})}})
          else {
            commit('addObjectToGraph', {editableObject, position, size})
            dispatch('getRelationFromServer', {object_id: objectId, rec_id: recId, objects: relatedObjects, noMove: noMove})
          }
        })
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
              for (let obj of response.data) {
              dispatch('addObjectToGraph', {recId: obj.rec_id, objectId: obj.object_id})
            }
            return Promise.resolve()
          })
          .catch(e => { return Promise.reject(e) })
    }
  }
}

class GraphObject extends DataBaseObject {
  constructor(object) {
    super(object)
    this.title = object.title
    this.triggers = object.triggers
    if(object.hasOwnProperty('photo'))
      this.photo = object.photo
    this.showTitle = true
    this.showTooltip = true
    this.showTriggers = true
    this.show = false
  }

  getGeneratedId() {
    return `${this.object.id}-${this.recId}`
  }
}

