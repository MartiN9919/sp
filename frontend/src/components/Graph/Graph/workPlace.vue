<template>
  <screen ref="screen">
    <g v-for="node in nodes">
      <node :data="node" class="node">
        <v-icon x-large>{{ primaryObject(parseInt(node.id.split('_')[0])).icon }}</v-icon>
        <v-card flat class="overflow-y-auto">
          <v-card-text class="pa-0">
            {{choosingObjects.find(object => object.object_id.toString() + '_' + object.rec_id.toString() === node.id).title}}
          </v-card-text>
        </v-card>
      </node>
    </g>
  </screen>
</template>

<script>
import Screen from 'vnodes/src/components/Screen'
import Node from 'vnodes/src/components/Node'
import Edge from 'vnodes/src/components/Edge'
import VLabel from 'vnodes/src/components/Label'
import graph from 'vnodes/src/graph'
import {mapActions, mapGetters} from "vuex";

export default {
  name: "workPlace",
  components: { Screen, Node, Edge, VLabel },
  data: () => ({
    graph: new graph(),
  }),
  computed: {
    ...mapGetters(['choosingObjects', 'lastObject', 'primaryObject']),
    nodes: {
      get: function () {
        for(let object of this.choosingObjects){
          if(this.graph.nodes.find(node => node.id === object.object_id.toString() + '_' + object.rec_id.toString()) === undefined){
            this.graph.createNode({
              id: object.object_id.toString() + '_' + object.rec_id.toString(),
              x: Math.floor(Math.random() * 500),
              y: Math.floor(Math.random() * 500),
            })
          }
        }
        return this.graph.nodes
      },
      set: function (node) {
        console.log(node)
      }
    }
  },
}
</script>

<style scoped>
.node >>> .outer {
  padding: 0 !important;
}
.node >>> .content {
  background-color: rgba(0, 0, 0, 0);
}
.node {
  display: flex;
  flex-direction: column;
  text-align: center;
  width: 300px;
  height: 150px;
}
</style>