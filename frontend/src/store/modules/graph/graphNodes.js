import axios from '@/plugins/axiosSettings'
import {Node, Edge} from "@/components/Graph/WorkSpace/lib/graph"

export default {
  state: {
    timeline: [],
  },
  getters: {
    timeline: state => callTime => state.timeline.find(t => t.date === callTime),
    nodes: state => (callTime=null) => {
      const converter = timeline => Array.from(timeline, t => t.nodes).flat(1)
      if(callTime) {
        return converter(state.timeline.filter(t => t.date <= callTime))
      } else {
        return converter(state.timeline)
      }
    },
    edges: state => (callTime=null) => {
      const converter = timeline => Array.from(timeline, t => t.edges).flat(1)
      if(callTime) {
        return converter(state.timeline.filter(t => t.date <= callTime))
      } else {
        return converter(state.timeline)
      }
    },
  },
  mutations: {
    createTimeLine: (state, callTime) => state.timeline.push({date: callTime, nodes: [], edges: []}),
    addNodeToTimeLine: (state, {node, callTime}) => state.timeline.find(t => t.date === callTime).nodes.push(node),
    addEdgeToTimeLine: (state, {edge, callTime}) => state.timeline.find(t => t.date === callTime).edges.push(edge),
  },
  actions: {
    createTimeLine({commit}, callTime) { commit('createTimeLine', callTime) },
    createNode({getters, commit}, {object, callTime}) {
      let findNode = getters.nodes().find(n => n.id === object.getGeneratedId())
      const node = findNode ? Object.assign(findNode, {entity: object}) : new Node(object)
      commit('addNodeToTimeLine', {node, callTime})
      return Promise.resolve(node)
    },
    createEdge({getters, commit}, {relation, callTime}) {
      let findEdge = getters.edges().find(e => e.id === relation.getGeneratedId())
      const edge = findEdge ? Object.assign(findEdge, {entity: relation}) : new Edge(relation)
      commit('addEdgeToTimeLine', {edge, callTime})
      return Promise.resolve(edge)
    },
    addToGraph({getters, commit, dispatch}, {payload}) {
      const callTime = new Date() // Время запроса, к которому будут привязаны объекты
      const requests = Array.isArray(payload) ? payload : [payload] // преобразование запрашиваемых объектов в массив
      commit('createTimeLine', callTime) // создание записи о запросе
      for(const {object_id, rec_id, props} of requests) { // props = { x, y, size } || null
        dispatch('getObjectFromServer', {object_id, rec_id}) // получение объекта с сервера как entity
          .then(object => {
            dispatch('createNode', {object, callTime}) // создание Node
              .then(node => {
                const objects = Array.from(getters.nodes(), n => n.entity) // все объекты за историю графа
                dispatch('getRelationFromServer', {from: object, objects: objects}) // получение связей с сервера как entity
                  .then(relations => {
                    dispatch('addNodeToGraph', {node, props, relations})
                    relations.forEach(relation =>
                      dispatch('createEdge', {relation, callTime}) // создание Edge и помещение ее в timeline
                        .then(edge => dispatch('addEdgeToGraph', edge)) // Помещение Edge на граф и в timeline
                    )
                  })
              }) // Помещение Node на граф и в timeline
          })
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
