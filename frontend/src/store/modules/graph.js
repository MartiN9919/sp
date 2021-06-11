import { getResponseAxios } from '@/plugins/axios_settings'

export default {
    state: {
        listObjects: [],
        classifiers: {},
        workPlace: [],
        activeObject: {
            objectId: '',
            recId: '',
            classifiers: [
                {
                    id: '',
                    value: '',
                    type: '',
                    hint: '',
                    need: '',
                }
            ],
        },
    },
    getters: {
        classifiers: state => state.classifiers,
        listObjects: state => state.listObjects,
        workPlace: state => state.workPlace,
    },
    mutations: {
        addListObjects: (state, objects) => { state.listObjects = objects },
        addObjectInWorkPlace: (state, objects) => { state.workPlace.push(objects) },
        addClassifier: (state, {objectId, classifiers}) => { state.classifiers[objectId] = classifiers },
    },
    actions: {
        addListObjects ({ commit }, config = {}) {
            return getResponseAxios('objects/list_type/', config)
                .then(response => { commit('addListObjects', response.data); return response.data })
                .catch(() => {})
        },
        activateObject ({ commit, state }, config = {}) {
            if (!(config.params.object_id in state.classifiers))
                return getResponseAxios('objects/list_classifier/', config)
                    .then(response => {
                        commit('addObjectInWorkPlace', {
                            objectId: config.params.object_id,
                            classifiers: [],
                        })
                        commit('addClassifier', {
                            objectId: config.params.object_id,
                            classifiers: response.data,
                        })
                    })
                    .catch(() => {})
            else
                commit('addObjectInWorkPlace', {
                    objectId: config.params.object_id,
                    classifiers: [],
                })
        },
    }
}
