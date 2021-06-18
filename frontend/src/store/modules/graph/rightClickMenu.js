export default {
    state: {
        showRightClickMenu: false,
        positionsRightClickMenu: {
            xRightClickMenuPosition: 0,
            yRightClickMenuPosition: 0,
        },
        bodyRightClickMenu: [],
    },
    getters: {
        showRightClickMenu: state => state.showRightClickMenu,
        positionsRightClickMenu: state => state.positionsRightClickMenu,
        bodyRightClickMenu: state => state.bodyRightClickMenu,
    },
    mutations: {
        stateMenuSettings: (state, menuSettings) => {
            state.bodyRightClickMenu = menuSettings.body
            state.positionsRightClickMenu = {
                xRightClickMenuPosition: menuSettings.event.clientX,
                yRightClickMenuPosition: menuSettings.event.clientY,
            }
        },
        activateRightClickMenu: (state) => {
            state.showRightClickMenu = true
        },
        deactivateRightClickMenu: (state) => {
            state.showRightClickMenu = false
        },
    },
    actions: {
        activateRightClickMenu ({ commit }, menuSettings) {
            menuSettings.event.preventDefault()
            commit('stateMenuSettings', menuSettings)
            commit('activateRightClickMenu')
        },
        deactivateRightClickMenu ({ commit }) {
            commit('deactivateRightClickMenu')
        },
    }
}