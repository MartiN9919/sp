import { getResponseAxios } from '@/plugins/axios_settings'

export default {
    state: {
        listObjects: [],
        classifiers: {},
        relations: [],
        workPlace: [],
    },
    getters: {
        classifiers: state => state.classifiers,
        listObjects: state => state.listObjects,
        workPlace: state => state.workPlace,
        relations: state => state.relations,
    },
    mutations: {
        addListObjects: (state, objects) => { state.listObjects = objects },
        addObjectInWorkPlace: (state, objects) => { state.workPlace.push(objects) },
        addClassifier: (state, {objectId, classifiers}) => { state.classifiers[objectId] = classifiers },
        addClassifiersToObject: (state, { index, objectId }) => {
            console.log(index, objectId)
            for (let classifier of state.classifiers[objectId])
                if (classifier.need === 1)
                    state.workPlace[index].classifiers.push(classifier)
        },
    },
    actions: {
        createNewObject({ commit, state }, object) {
            let index = state.workPlace.findIndex(obj => obj === object)
            index !== -1 ? commit('addClassifiersToObject', { index: index, objectId: object.objectId}) :  console.log('error')
        },
        activateObject ({ commit, state }, config = {}) {
            if (!(config.params.object_id in state.classifiers))
                return getResponseAxios('objects/list_classifier/', config)
                    .then(response => {
                        commit('addObjectInWorkPlace', { objectId: config.params.object_id, classifiers: [], })
                        commit('addClassifier', { objectId: config.params.object_id, classifiers: response.data, })
                    })
                    .catch(() => {})
            else
                commit('addObjectInWorkPlace', { objectId: config.params.object_id, classifiers: [], })
        },
        addListObjects ({ commit }, config = {}) {
            return getResponseAxios('objects/list_type/', config)
                .then(response => { commit('addListObjects', response.data); return response.data })
                .catch(() => {})
        },
    }
}
