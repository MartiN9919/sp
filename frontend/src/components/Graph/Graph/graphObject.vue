<template>
  <g class="graph-object">
    <node :data="node">
      <v-img v-if="node.object.hasOwnProperty('photo')" width="200" height="200" class="elevation-15 mx-8 mb-8" style="border-radius: 90%;" :src="getPhoto(node)"></v-img>
      <v-icon v-else size="200" class="elevation-15 mx-8 mb-8" style="border-radius: 90%; background-color: white" >{{ node.object.object.icon }}</v-icon>
    </node>
    <foreignObject height="1" width="400" overflow="visible" :x="node.x + node.width / 2 - 200" :y="node.y + node.height">
      <div style="text-align: center; font-size: 0.8em; color: #444444">{{node.object.title}}</div>
    </foreignObject>
    <v-label :element="node" :offset="{x: parseInt(offsetX), y: parseInt(offsetY)}" align="bottom" useDrag @drag="onDrag">
      <div class="v-card v-card--hover v-sheet theme--light elevation-15 ma-8 pa-2" style="width: 440px; opacity: 0.8">
          <table style="width: 100%">
            <tr v-for="param in node.object.params" :key="param.id" v-if="param.values.length" style="font-size: 0.8em; word-wrap: anywhere">
              <template>
                <td>{{param.baseParam.title}}</td>
                <td style="text-align: end">{{param.values[0].value}}</td>
              </template>
            </tr>
          </table>
      </div>
    </v-label>
  </g>
</template>

<script>
import Node from '../lib/components/Node'
import VLabel from '../lib/components/Label'
import {getFileLink} from '@/plugins/axios_settings'

export default {
  name: "graphObject",
  components: {Node, VLabel},
  props: {
    node: Object,
  },
  data: () => ({
    offsetX: 0,
    offsetY: 0,
  }),
  methods: {
    getPhoto(node) {
      return getFileLink(node.object.object.id, node.object.recId, node.object.photo)
    },
    onDrag (d) {
      this.offsetX += d.x || 0
      this.offsetY += d.y || 0
      this.offsetX = Math.max(Math.min(this.offsetX, 200), -200)
      this.offsetY = Math.max(Math.min(this.offsetY, 200), -200)
    }
  }
}
</script>

<style scoped>
.graph-object >>> .label, .graph-object >>> .content{
  background-color: rgba(255, 255, 255, 0.1);
}
</style>