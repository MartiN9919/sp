<template>
  <div @click.right.prevent.stop="menu_show($event, null)">
    <screen ref="screen">
      <edge v-for="edge in graph.edges" :key="edge.id.toString() + 'edge'" :data="edge" :nodes="graph.nodes"></edge>
      <g v-for="node in nodes"
        @mousedown.capture.shift="startMoveGroupNodes(node)"
        @mouseup.shift="stopMoveGroupNodes()"
        @mousemove.shift="movingGroupNodes(node)">
        <node :data="node" class="node">
          <v-icon x-large :class="getIconClass(node.id)"
          @click.right.prevent.stop="menu_show($event, node)"
          @click.ctrl.left.exact="addSelectedNodes(node)"
          @click.left.exact="addSelectedNode(node)"
          >{{ primaryObject(parseInt(node.id.split('_')[0])).icon }}
          </v-icon>
          <v-card flat class="overflow-y-auto" style="background-color: rgba(0,0,0,0.05)">
            <v-card-text class="pa-0 object-title">
              {{
                choosingObjects.find(object => object.object_id.toString() + '_' + object.rec_id.toString() === node.id).title
              }}
            </v-card-text>
          </v-card>
        </node>
      </g>
    </screen>
    <menu-graph ref="menuGraph" :params="menuParams"
     @startRelationCreate="startCreateRelation"
     @removeNode="removeNodes"
     @updateGraph="forceRedrawCluster(graph.nodes, graph.edges)"></menu-graph>
    <v-menu v-if="isCreateRelation" v-model="isCreateRelation" :position-x="menuParams.x"
            :position-y="menuParams.y" absolute offset-y :close-on-content-click="false">
      <create-relation-menu :params="relationParams"></create-relation-menu>
    </v-menu>
  </div>
</template>

<script>
import Screen from 'vnodes/src/components/Screen'
import Node from 'vnodes/src/components/Node'
import Edge from 'vnodes/src/components/Edge'
import VLabel from 'vnodes/src/components/Label'
import graph from 'vnodes/src/graph'
import {mapActions, mapGetters} from "vuex";
import menuGraph from "./contextMenuGraph";
import CreateRelationMenu from "./createRelationMenu";

export default {
  name: "workPlace",
  components: {CreateRelationMenu, menuGraph, Screen, Node, Edge, VLabel},
  data: () => ({
    menuParams: null,
    relationParams: null,
    graph: new graph(),
    createRelationStatus: false,
    tempNode: null,
    isCreateRelation: false,
    selectedNodes: [],
    movingNode: {x0:0, y:0, node:null},
    moveNode: false,
  }),
  computed: {
    ...mapGetters(['choosingObjects', 'lastObject', 'primaryObject']),
    nodes: function () {
      for (let object of this.choosingObjects) {
        if (this.graph.nodes.find(node => node.id === object.object_id.toString() + '_' + object.rec_id.toString()) === undefined) {
          this.graph.createNode({
            id: object.object_id.toString() + '_' + object.rec_id.toString(),
            x: Math.floor(Math.random() * 500),
            y: Math.floor(Math.random() * 500),
          })
        }
      }
      return this.graph.nodes
    },
  },
  methods: {
    ...mapActions(['removeChoosingObject',]),
    test() {
      console.log('abc')
    },
    addSelectedNode(node) {
      if (this.selectedNodes.length === 1 && this.selectedNodes[0].id === node.id) {
        this.selectedNodes = []
      } else {
        this.selectedNodes = []
        this.selectedNodes.push(node)
      }
    },
    addSelectedNodes(node) {
      if (this.selectedNodes.find(item => item.id === node.id)) {
        let removeIndex = this.selectedNodes.findIndex(item => item.id === node.id)
        this.selectedNodes.splice(removeIndex, 1)
      } else {
        this.selectedNodes.push(node)
      }

    },
    getIconClass(id) {
      return this.selectedNodes.find(node => node.id === id) ? 'object-icon-selected' : 'object-icon'
    },
    createRelation(object1, id1, object2, id2) {
      this.relationParams = {object1_id: object1, rec_id1: id1, object2_id: object2, rec_id2: id2}
      this.isCreateRelation = true
    },
    createEdge(node1, node2) {
      // this.createRelation(parseInt(node1.split('_')[0]), parseInt(node1.split('_')[1]), parseInt(node2.split('_')[0]), parseInt(node2.split('_')[1]))
      this.graph.createEdge(node1, node2, {
        fromAnchor: {x: (node1.width * 0.5) - 10, y: '9%'},
        toAnchor: {x: (node2.width * 0.5) - 10, y: '9%'}
      })
    },
    menu_show(e, node) {
      if (node === null) {
        this.menuParams = {x: e.clientX, y: e.clientY}
        return
      }
      this.tempNode = node
      if (this.selectedNodes.length === 0 || this.selectedNodes.length > 2) {
        this.menuParams = {x: e.clientX, y: e.clientY, creationEdge: 'no', node: true}
      }
      if (this.selectedNodes.length === 1) {
        this.menuParams = {x: e.clientX, y: e.clientY, creationEdge: 'oneNode', node: true}
      }
      if (this.selectedNodes.length === 2) {
        this.menuParams = {x: e.clientX, y: e.clientY, creationEdge: 'twoNodes', node: true}
      }

    },
    startCreateRelation() {
      if (this.selectedNodes.length === 2) {
        this.createEdge(this.selectedNodes[0], this.selectedNodes[1])
        this.selectedNodes = []
      } else {
        this.createEdge(this.selectedNodes[0], this.tempNode)
        this.selectedNodes = []
      }
    },
    removeNodes() {
      if (this.selectedNodes.length > 0 && this.selectedNodes.find(item => item.id === this.tempNode.id)) {
        for (let node of this.selectedNodes) {
          this.removeNode(node)
        }
        this.selectedNodes = []
      } else {
        this.removeNode(this.tempNode)
      }
    },
    removeNode(node) {
      let object_id = parseInt(node.id.split('_')[0])
      let rec_id = parseInt(node.id.split('_')[1])
      this.removeChoosingObject({object_id, rec_id})
      let removeEdges = []
      for (let edge of this.graph.edges) {
        if (edge.from === node.id || edge.to === node.id) {
          removeEdges.push(edge)
        }
      }
      for (let removeEdge of removeEdges) {
        this.graph.removeEdge(removeEdge)
      }
      this.graph.removeNode(node)
    },
    getRelationByNode(node){
      let tempResultList = []
      for(let edge of this.graph.edges){
        if(edge.from === node.id){
          tempResultList.push(edge.to)
        }
        if(edge.to === node.id){
          tempResultList.push(edge.from)
        }
      }
      let resultList = []
      for(let node of this.graph.nodes){
        if(tempResultList.indexOf(node.id) !== -1){
          resultList.push(node)
        }
      }
      return resultList
    },
    movingGroupNodes(node){
      if(this.moveNode){
        let dx = node.x - this.movingNode.x0
        let dy = node.y - this.movingNode.y0
        this.movingNode.x0 = node.x
        this.movingNode.y0 = node.y
        let nodesToMove = this.getRelationByNode(node)
        for(let tempNode of nodesToMove){
          tempNode.x += dx
          tempNode.y += dy
          let tempSubNodes = this.getRelationByNode(tempNode)
          for(let tempSubNode of tempSubNodes){
            if(tempSubNode.id !== node.id && nodesToMove.indexOf(tempSubNode) === -1){
              tempSubNode.x += dx/2
              tempSubNode.y += dy/2
            }
          }
        }
      }
    },
    startMoveGroupNodes(node){
      this.moveNode = true
      this.movingNode.node = node
      this.movingNode.x0 = node.x
      this.movingNode.y0 = node.y
    },
    stopMoveGroupNodes(){
      this.moveNode = false
    },
    forceRedrawCluster(nodes, links) {
      for (let j = 0; j < 100; j++) {
        for (let node of nodes) {
          for (let otherNode of nodes) {
            if (otherNode.id === node.id) {
              continue;
            } else {
              if (links.find((link) => {
                return (link.to === node.id && link.from === otherNode.id) ||
                    (link.from === node.id && link.to === otherNode.id)
              })) {
                let dx = otherNode.x - node.x;
                let dy = otherNode.y - node.y;
                let offset = Math.sqrt(dx * dx + dy * dy);
                if (offset < 500 && offset > 450) {
                  continue;
                }
                if (offset < 449) {
                  if (offset < 200) {
                    node.x -= dx;
                    node.y -= dy;
                  } else {
                    node.x -= dx / 3;
                    node.y -= dy / 3;
                  }
                } else {
                  node.x += dx / 6;
                  node.y += dy / 6;
                }
              } else {
                let dx = otherNode.x - node.x;
                let dy = otherNode.y - node.y;
                let offset = Math.sqrt(dx * dx + dy * dy);
                if (offset < 1000) {
                  node.x -= dx / 9;
                  node.y -= dy / 9;
                }
                if (offset < 500) {
                  node.x -= dx / 3;
                  node.y -= dy / 3;
                }
                if (offset < 100) {
                  node.x -= dx * 3;
                  node.y -= dy * 3;
                }
              }
            }
          }
          let dx = 0 - node.x
          let dy = 0 - node.y
          node.x += dx / 15
          node.y += dy / 15
        }
      }
    },
  }
}
</script>

<style scoped>
.node >>> .outer {
  padding: 0 !important;
}

.node >>> .content {
  background-color: rgba(0, 0, 0, 0);
  width: 100%;
  height: 100%;
}

.edge {
  stroke-width: 2;
  marker-end: none;
}

.node {
  display: flex;
  flex-direction: column;
  text-align: center;
  width: 300px;
  height: 150px;
}

.object-icon, .object-icon-selected {
  border-radius: 90px;
  margin-top: 4px;
}

.object-icon {
  background-color: white;
}

.object-icon-selected {
  background-color: red;
}

</style>