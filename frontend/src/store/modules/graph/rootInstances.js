import {getResponseAxios} from '@/plugins/axios_settings'

export default {
  state: {
    objects: [],
    classifiers: [],
    relations: [],
  },
  getters: {
    baseObjects: state => { return state.objects },
    baseObject: state => id => { return state.objects.find(o => o.id === id) },
    baseClassifiers: state => id => { return state.classifiers.filter(c => c.objectId === id) },
    baseClassifier: state => id => { return state.classifiers.find(c => c.id === id) },
    baseRelation: state => id => { return state.relations.find(r => r.id === id) },
    baseRelations: state => ids => {
      return state.relations
        .filter(r => ((r.f_id === ids.f_id && r.s_id === ids.s_id) || (r.f_id === ids.s_id && r.s_id === ids.f_id)))
    },
  },
  mutations: {
    setBaseObjects: (state, objects) => state.objects.push(...objects),
    addBaseClassifiers: (state, classifiers) => state.classifiers.push(...classifiers),
    setBaseRelations: (state, relations) => state.relations.push(...relations),
  },
  actions: {
    async getBaseObjects({commit, dispatch}, config = {}) {
      await getResponseAxios('objects/list_type/', config)
        .then(r => { commit('setBaseObjects', r.data.map(o => new BaseObject(o))) })
        .catch(e => { return Promise.reject(e) })
      return Promise.resolve()
    },
    async getBaseClassifiers({getters, commit}, config = {}) {
      if (getters.baseClassifiers(config.params.object_id).length)
        return Promise.resolve()
      await getResponseAxios('objects/list_classifier/', config)
        .then(r => { commit('addBaseClassifiers', r.data.map(c => new BaseClassifier(c))) })
        .catch(e => { return Promise.reject(e) })
      return Promise.resolve()
    },
    async getBaseRelations({getters, commit}, config = {}) {
      await getResponseAxios('objects/relations/', config)
        .then(r => { commit('setBaseRelations', r.data.map(l => new BaseRelation(l))) })
        .catch(e => { return Promise.reject(e) })
      return Promise.resolve()
    },
  }
}

class BaseInstanceToObject {
  constructor(id, title) {
    this.id = id
    this.title = title
  }
}

class BaseObject extends BaseInstanceToObject {
  constructor(baseObject) {
    super(baseObject.id, baseObject.title)
    this.name = baseObject.name
    this.rels = baseObject.rels
    this.titleSingle = baseObject.title_single
    this.icon = baseObject.icon
  }
}

class BaseClassifier extends BaseInstanceToObject {
  constructor(baseClassifier) {
    super(baseClassifier.id, baseClassifier.title)
    this.objectId = baseClassifier.obj_id
    this.name = baseClassifier.name
    this.type = baseClassifier.type
    this.list = baseClassifier.list_id
  }
}

class BaseRelation extends BaseInstanceToObject {
  constructor(baseRelation) {
    super(baseRelation.id, baseRelation.title)
    this.f_id = baseRelation.object_id_1
    this.s_id = baseRelation.object_id_2
    this.hint = baseRelation.hint
    this.type = baseRelation.type
  }
}
