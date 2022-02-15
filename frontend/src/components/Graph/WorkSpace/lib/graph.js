import uuid from 'uuid'
import util from './util'
import { flextree } from 'd3-flextree'
import store from '../../../../store'

export default class Graph {
  constructor () {
    this.nodes = []
    this.edges = []
  }

  positionNode ({ node, parent, dir = 'right', spacing = 40, invertOffset = false } = {}) {
    node = typeof node === 'string' ? this.nodes.find(n => n.id === node) : node
    parent = typeof parent === 'string' ? this.nodes.find(n => n.id === parent) : parent
    const pos = util.findPosition(node, parent, dir, this.nodes, spacing, invertOffset)
    this.updateNode(node, { x: pos.x, y: pos.y })
  }

  graphNodes ({ nodes, edges, type = 'basic', dir = 'right', spacing = 40 } = {}) {
    nodes = nodes || this.nodes
    edges = edges || this.edges

    const dag = util.createDAG(nodes, edges) // removes cycles if any
    if (!dag.length) {
      return
    }

    if (type === 'basic' || type === 'basic-invert') {
      const visited = {}
      const findPos = (node, parent) => {
        if (visited[node.id]) {
          return
        }
        const collisions = nodes.filter(n => !!visited[n.id])
        const pos = util.findPosition(node, parent, dir, collisions, spacing, type === 'basic-invert')
        node.x = pos.x
        node.y = pos.y
        this.updateNode(node.id, {
          x: node.x,
          y: node.y
        })
        visited[node.id] = true
        node.children.forEach(n => findPos(n, node))
      }
      dag
        .filter(node => !node.parentIds.length)
        .forEach(node => findPos(node, null))
    } else

    if (type === 'tree') {
      const layout = flextree()
      const flipH = (dir === 'left' || dir === 'right')
      const roots = dag.filter(n => !n.parentIds.length)
      roots.forEach(root => {
        const graph = []
        const offsetX = root.x
        const offsetY = root.y
        util.dagToFlextree(root, graph, flipH, spacing)
        const tree = layout.hierarchy(graph[0])
        layout(tree)
        // apply layout to nodes
        const invertX = dir === 'left' ? -1 : 1
        const invertY = dir === 'up' ? -1 : 1
        const applyChanges = n => {
          this.updateNode(n.data.id, {
            x: (flipH ? n.y : n.x) * invertX + offsetX,
            y: (flipH ? n.x : n.y) * invertY + offsetY
          })
          n.children && n.children.forEach(applyChanges)
        }
        applyChanges(tree)
      })
    } else {
      throw new Error('unknown layout type ' + type)
    }
  }

  reset () {
    while (this.edges.length) { this.edges.pop() }
    while (this.nodes.length) { this.nodes.pop() }
  }

  createNode (node) {
    this.nodes.push(node)
  }

  updateNode (node, fields = {}) {
    if (typeof node === 'string') node = this.nodes.find(n => n.id === node)
    if (!node) throw new Error(`node ${node} does not exist`)
    return Object.assign(node, fields)
  }

  removeNode (node) {
    this.edges.filter(edge => edge.from === node.id || edge.to === node.id).map(edge => this.removeEdge(edge))
    const index = this.nodes.indexOf(node)
    if (index > -1) {
      this.nodes.splice(index, 1)
    }
    return index
  }

  createEdge (edge) {
    this.edges.push(edge)
  }

  updateEdge (edge, fields) {
    return Object.assign(edge, fields)
  }

  removeEdge (edge) {
    const index = this.edges.indexOf(edge)
    if (index > -1) {
      this.edges.splice(index, 1)
    }
    return index
  }

  clearGraph(){
    this.edges = []
    this.nodes = []
  }

  reorderStep (i, size, tempNodes, lastSpeed=10000, x, y) {
    setTimeout(() => {
      let speed = 0
      let speedNums = 0
      for(let node of tempNodes) {
        for (let otherNode of tempNodes) {
          if (otherNode.id !== node.id) {
            // distance(offset) between two nodes
            let x0 = node.x
            let y0 = node.y
            this.forceMoveNode(node, otherNode, [])
            let dx = node.x - x0
            let dy = node.y - y0
            speed += Math.sqrt(dx * dx + dy * dy) / 100
            speedNums++
          }
        }
        // move all nodes to start of coordinates
        let dx = x - node.x
        let dy = y - node.y
        node.x += dx / 30
        node.y += dy / 30
      }
      let averageSpeed = (speed / speedNums) * 100
      let dif = Math.abs((lastSpeed - averageSpeed)/lastSpeed*100)
      if(dif < 0.005 || i >= size-1){
        for(let node of tempNodes){
          let tempNode = this.nodes.find((item) => {return item.id === node.id})
          tempNode.x = node.x
          tempNode.y = node.y
        }
        store.commit('changeLoadStatus', false)
      }
      else {
        lastSpeed = averageSpeed
        this.reorderStep(i+1, size, tempNodes, lastSpeed, x, y)
      }
    }, 0)
  }
  reorderGraph(x, y, nodes) {
    store.commit('changeLoadStatus', true)
    let tempNodes = []
    for(let node of nodes) {
      tempNodes.push({id: node.id, x: node.x, y: node.y, width: node.width})
    }
    this.reorderStep(0, 200, tempNodes, 10000, x, y)
  }
  getNewNodePosition(edges, position) {
    let startPosition = {id:'', size: 300}
    if(edges.length === 0){
      return Object.assign(startPosition, this.getStartPosition(position))
    }
    startPosition = Object.assign(this.getNodesCenter(this.nodes.filter(n => edges.find(e => e === n.id))), startPosition)
    let startSpeed = 0
    for(let i=0; i < 30; i++) {
      const temp = {x: startPosition.x, y: startPosition.y}
      for(const node of this.nodes)
        this.forceMoveNode(startPosition, node, edges)
      const speed = Math.sqrt(Math.pow(Math.abs(temp.x - startPosition.x),2) + Math.pow(temp.y - startPosition.y,2))
      if(startSpeed === 0) {
        startSpeed = speed
      }
      else {
        if (speed / startSpeed < 0.05) {
          break
        }
      }
    }
    return startPosition
  }
  forceMoveNode(node, otherNode, edges) {
    let dx = otherNode.x - node.x
    let dy = otherNode.y - node.y
    dx === 0 ? dx = Math.random() * 20 - 10 : dx
    dy === 0 ? dy = Math.random() * 20 - 10 : dy
    let offset = Math.sqrt(dx * dx + dy * dy);
    if (edges.find(edge => edge === node.id)
        || this.edges.find(edge => {
              return (edge.to === node.id && edge.from === otherNode.id) ||
                  (edge.from === node.id && edge.to === otherNode.id)
            })) {
      const springForce = 0.25 * Math.log2(offset / 450)
      node.x += dx * springForce
      node.y += dy * springForce
    }
    const upCoefficient = Math.pow(node.size/300 * otherNode.size/300, 1)
    const upForce = upCoefficient * 3000 / Math.pow(offset, 2)
    node.x -= dx * upForce
    node.y -= dy * upForce
  }
  getStartPosition(position) {
    return {
      x: position.x - Math.random() * position.width,
      y: position.y - Math.random() * position.height,
    }
  }
  getNodesCenter(nodes){
    let x = 0
    let y = 0
    for(const node of nodes)  {
      x += node.x
      y += node.y
    }
    return {x: x / nodes.length, y: y / nodes.length}
  }
}

class GraphElementStateBase {
  constructor() {
    this.added = false
    this.hover = false
  }
}

class GraphObjectState extends GraphElementStateBase {
  constructor() {
    super()
    this.selected = false
  }
}

class GraphRelationState extends GraphElementStateBase {
  constructor() {
    super()
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

class GraphRelationSettings extends GraphElementSettingsBase{
  constructor() {
    super()
  }
}

export class Node {
  constructor(entity, {x, y, size=300}) {
    this.x = x
    this.y = y
    this.size = size
    this.entity = entity
    this.state = new GraphObjectState()
    this.settings = new GraphObjectSettings()
  }

  get id() {
    return this.entity.getGeneratedId()
  }

  get ids() {
    return this.entity.ids
  }
}

export class Edge {
  constructor(entity) {
    this.size = 300
    this.pathd = ''
    this.entity = entity
    this.state = new GraphRelationState()
    this.settings = new GraphRelationSettings()
  }

  get from() {
    return this.entity.o1.getGeneratedId()
  }

  get to() {
    return this.entity.o2.getGeneratedId()
  }

  get id() {
    return this.entity.getGeneratedId()
  }

  get ids() {
    return this.entity.ids
  }
}
