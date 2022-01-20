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

  // refs
  // https://gojs.net

  // TODO
  // dagLoad - set [nodes] and [edges] from dag
  // dagBuild - builds and saves dag info into nodes
  // dagBuildEdges - delete all edges and build them from Dag
  // dagSetParent - change dag parent (string or array[string] => array[string])

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

  createNode (fields = {}) {
    if (typeof fields === 'string') {
      fields = { id: fields } // support a single id string or an object as params
    }
    const node = Object.assign({
      id: uuid(),
      x: 0,
      y: 0,
      width: 50,
      height: 50,
    }, fields)

    this.nodes.push(node)
    return node
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

  createEdge (from, to, fields = {}) {
    if (arguments.length === 1) {
      // support calling with single argument
      fields = arguments[0]
      from = fields.from
      to = fields.to
    } else {
      // support passing node objects instead of ids
      if (typeof from === 'object') from = from.id
      if (typeof to === 'object') to = to.id
    }
    if (!from) throw new Error('orig required')
    if (!to) throw new Error('dest required')

    const edge = Object.assign({
      id: fields.id || `${from}@${to}`,
      from,
      to,
      fromAnchor: { x: '50%', y: '50%' },
      toAnchor: { x: '50%', y: '50%' },
      type: 'linear',
      pathd: '', // reactive path
    }, fields)

    this.edges.push(edge)
    return edge
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
            let dx = otherNode.x - node.x;
            let dy = otherNode.y - node.y;
            let offset = Math.sqrt(dx * dx + dy * dy);
            // if nodes is linked
            if (this.edges.find(edge => {
              return (edge.to === node.id && edge.from === otherNode.id) ||
                  (edge.from === node.id && edge.to === otherNode.id)
            })) {
              let springForce = 0.25 * Math.log2(offset / 750)
              node.x += dx * springForce
              node.y += dy * springForce
            }
            let upForce = 10000 / Math.pow(offset, 2)
            node.x -= dx * upForce
            node.y -= dy * upForce
            dx = node.x - x0
            dy = node.y - y0
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
  reorderGraph(x, y, nodes=this.nodes) {
    store.commit('changeLoadStatus', true)
    let tempNodes = []
    for(let node of nodes) {
      tempNodes.push({id: node.id, x: node.x, y: node.y, width: node.width})
    }
    this.reorderStep(0, 200, tempNodes, 10000, x, y)
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
