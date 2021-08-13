<template>
  <div @click.right.prevent.stop="menu_show($event, null)">
    <screen ref="screen">
      <edge v-for="edge in graph.edges" :key="edge.id.toString() + 'edge'" :data="edge" :nodes="graph.nodes"></edge>
      <g v-for="node in nodes"
        @mousedown.capture.shift="startMoveGroupNodes(node)"
        @mouseup.shift="stopMoveGroupNodes()"
        @mousemove.shift="movingGroupNodes(node)"
        @wheel.prevent.stop="testScroll($event, node)"
      >
        <node :data="node" class="node">
          <v-icon
            :size="node.width * 0.7"
            :class="getIconClass(node.id)"
            @click.right.prevent.stop="menu_show($event, node)"
            @click.ctrl.left.exact="addSelectedNodes(node)"
            @click.left.exact="addSelectedNode(node)"
          >
            {{ primaryObject(parseInt(node.id.split('_')[0])).icon }}
          </v-icon>
          <v-card flat class="overflow-y-auto" style="background-color: rgba(0,0,0,0.0)" :size="node.width * 0.3">
            <p class="pa-0 object-title" :style="{ fontSize: node.width * 0.1}" style="height: auto">
              {{
                choosingObjects.find(object => object.object_id.toString() + '_' + object.rec_id.toString() === node.id).title
              }}
            </p>
          </v-card>
        </node>
      </g>
<!--      <v-label v-for="edge in graph.edges" :perc="50" :offset="{x: 0, y: -50}">-->
<!--        <h4>Content</h4>-->
<!--      </v-label>-->
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
            width: 100,
            height: 100,
          })
        }
      }
      return this.graph.nodes
    },
  },
  methods: {
    ...mapActions(['removeChoosingObject',]),
    testScroll(event, node) {
      let width = node.width
      let height = node.height
      if(event.deltaY < 0){
        node.width = node.width * 1.1
        node.height = node.height * 1.1
      }
      else{
        node.width = node.width * 0.9
        node.height = node.height * 0.9
      }
      let dx = (node.width - width)/2
      let dy = (node.height - height)/2
      node.x -= dx
      node.y -= dy
      console.log(node)
    },
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
        fromAnchor: {x: '50%', y: '50%'},
        toAnchor: {x: '50%', y: '50%'}
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
      let n = 0
      for (let j = 0; j < 200; j++) {
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
                if(offset < 500){
                  if (offset < 400) {
                    if (offset < 200) {
                      node.x -= dx;
                      node.y -= dy;
                    } else {
                        node.x -= dx / 3;
                        node.y -= dy / 3;
                      }
                  } else {
                      n++
                      node.x += dx / 6;
                      node.y += dy / 6;
                    }
                }
                else{
                  node.x += dx/3;
                  node.y += dy/3;
                }
              } else {
                let dx = otherNode.x - node.x;
                let dy = otherNode.y - node.y;
                let offset = Math.sqrt(dx * dx + dy * dy);
                if(offset < 1000){
                  if(offset < 100){
                    node.x -= dx * 2;
                    node.y -= dy * 2;
                  }
                  else{
                    if(offset < 500){
                      node.x -= dx / 3;
                      node.y -= dy / 3;
                    }
                    else{
                      node.x -= dx / 9;
                      node.y -= dy / 9;
                    }
                  }
                }
                else {
                  n++
                }
              }
            }
          }
          let dx = 0 - node.x
          let dy = 0 - node.y
          node.x += dx / 15
          node.y += dy / 15
        }
        if(n / (this.nodes.length * this.nodes.length) > 0.7){
          console.log('res', n)
          break
        }
      }
      console.log(n)
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
}

.object-icon, .object-icon-selected {
  border-radius: 90%;
  margin-top: 4px;
}

.object-icon {
  background-color: white;
}

.object-icon-selected {
  background-color: rgba(255, 0, 0, 0.3);
}
.v-icon.v-icon::after {
  opacity: 0;
}

</style>