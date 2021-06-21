export default {
    state: {
        isStateContextMenu: false,
        typeContextMenu: 'workSpace',
        xPosition: 0,
        yPosition: 0,
    },
    getters: {
        isStateContextMenu: state => state.isStateContextMenu,
        typeContextMenu: state => state.typeContextMenu,
        coordinatesContextMenu: state => {
            return { x: state.xPosition, y: state.yPosition, }
        },
    },
    mutations: {
        setCoordinatesContextMenu: (state, event) => {
            state.xPosition = event.clientX
            state.yPosition = event.clientY
        },
        setTypeContextMenu: (state, type) => {
          state.typeContextMenu = type
        },
        activateContextMenu: (state) => {
            state.isStateContextMenu = true
        },
        deactivateContextMenu: (state) => {
            state.isStateContextMenu = false
        },
    },
    actions: {
        setCoordinatesContextMenu ({ commit }, event) {
            event.preventDefault()
            commit('setCoordinatesContextMenu', event)
            commit('activateContextMenu')
        },
        setTypeContextMenu ({ commit }, type) {
            commit('setTypeContextMenu', type)
        },
        activateContextMenu ({ commit }) {
            commit('activateContextMenu')
        },
        deactivateContextMenu ({ commit }) {
            commit('deactivateContextMenu')
        },
    }
}