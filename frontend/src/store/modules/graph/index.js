import classifiers from './classifiers'
import objects from './objects'
import relations from './relations'
import contextMenu from './contextMenu'
import workArea from './workArea'
import graphNodes from './graphNodes'

export function getWorkArea(rootState) {
  return rootState.graph.workArea.workAreaOfObjects
}

export function getObjectFromWorkArea(rootState, objectId) {
  return getWorkArea(rootState).find(object => object.tempId === objectId)
}

export function getActiveObject(rootState) {
  let workAreaOfObjects = getWorkArea(rootState)
  return workAreaOfObjects.find(object => object.tempId === rootState.graph.workArea.activeObjectId)
}

export default {
  modules: {
    classifiers,
    objects,
    relations,
    contextMenu,
    workArea,
    graphNodes,
  },
}