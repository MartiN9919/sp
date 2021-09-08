<template>
  <div>
    <screen ref="screen" class="screen">
      <edge v-for="edge in graphRelations" :key="`edge-${edge.id}`" :data="edge" :nodes="graphObjects"></edge>
      <graph-object v-for="node in graphObjects" :key="node.id" :node="node"></graph-object>
    </screen>
  </div>
</template>

<script>
import Screen from '../lib/components/Screen'
import Edge from '../lib/components/Edge'
import GraphObject from "@/components/Graph/Graph/graphObject"
import {mapGetters} from "vuex"

export default {
  name: "workPlace",
  components: {GraphObject, Screen, Edge},
  computed: mapGetters(['graphObjects', 'graphRelations']),
  methods: {
    onDrag (node, d) {
      node.offsetX += d.x || 0
      node.offsetY += d.y || 0
      node.offsetX = Math.max(Math.min(node.offsetX, 200), -200)
      node.offsetY = Math.max(Math.min(node.offsetY, 200), -200)
    }
  }
}
</script>

<style scoped>
.screen >>> .edge {
  marker-end: none;
  stroke: #aaaaaa;
  stroke-width: 2px;
}
</style>