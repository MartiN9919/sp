<template>
  <div class="h-100 disable-optimize select-off" @mouseup.exact="clearSelectors" @contextmenu="menuShow">
    <screen id="screen" ref="screen" @selectNodes="setChoosingObjects" oncontextmenu="return false">
      <graph-relation
        v-for="edge in graphEdges"
        :key="edge.id"
        :edge="edge"
        :nodes="graphNodes"
        @hover="hover"
        @unhover="unHover"
        @setChoosingRelated="setChoosingRelated"
      />
      <graph-object
        v-for="node in graphNodes"
        :key="node.id"
        :node="node"
        :selected-objects="selectedNodes"
        @hover="hover"
        @unhover="unHover"
        @setChoosingRelated="setChoosingRelated"
      />
    </screen>
    <search-object v-if="graphNodes.length" :nodes="graphNodes" @findNode="findNode"/>
    <context-menu-nested ref="contextMenu" :form="this" :items="contextMenu" :color="$CONST.APP.COLOR_OBJ"/>
  </div>
</template>

<script>
import Screen from '@/components/Graph/WorkSpace/lib/components/Screen'
import GraphObject from "@/components/Graph/WorkSpace/graphObject"
import GraphRelation from "@/components/Graph/WorkSpace/graphRelation"
import bodyContextMenu from "@/components/Graph/WorkSpace/Modules/bodyContextMenu"
import SearchObject from "@/components/Graph/WorkSpace/Modules/searchObject"
const ContextMenuNested = () => import("@/components/WebsiteShell/UIMainComponents/contextMenuNested")
import {Node, Edge} from '@/components/Graph/WorkSpace/lib/graph'
import {mapActions, mapGetters} from "vuex"

export default {
  name: "graphArea",
  mixins: [bodyContextMenu],
  components: {SearchObject, GraphRelation, GraphObject, Screen, ContextMenuNested},
  computed: {
    ...mapGetters(['graphNodes', 'graphEdges', 'selectedNodes', 'hoverNodes', 'hoverEdges', 'globalDisplaySettingValue']),
  },
  methods: {
    ...mapActions(['setScreen']),
    isNode(element) {
      return element instanceof Node
    },
    findNode(node) {
      this.$refs.screen.zoomNode(node,2.5)
    },
    setChoosingRelated() {
      this.hoverNodes.forEach(n => n.state.selected = true)
    },
    setChoosingObjects(frame) {
      const xMax = frame.x + frame.width
      const yMax = frame.y + frame.height
      for(const node of this.graphNodes){
        const x = node.x + node.size / 6
        const y = node.y + node.size / 6
        if(x > frame.x && x < xMax && y > frame.y && y < yMax) {
          node.state.selected = true
        }
      }
    },
    pickUp(element) {
      let ar = this.isNode(element) ? this.graphNodes : this.graphEdges
      ar.splice(ar.findIndex(r => r === element), 1)
      ar.push(element)
      element.state.hover = true
    },
    getRelatedForNode(node) {
      const edges = this.graphEdges.filter(edge => [edge.to, edge.from].includes(node.id))
      const nodes = edges.map(e => this.graphNodes.find(n => [e.to, e.from].includes(n.id) && n.id !== node.id))
      return {nodes, edges}
    },
    getRelatedForRelation(edge) {
      return this.graphNodes.filter(n => [edge.to, edge.from].includes(n.id))
    },
    hover(element) {
      if(this.isNode(element)) {
        const elements = this.getRelatedForNode(element)
        elements.nodes.forEach(n => this.pickUp(n))
        elements.edges.forEach(e => this.pickUp(e))
      } else {
        const nodes = this.getRelatedForRelation(element)
        nodes.forEach(n => this.pickUp(n))
      }
      this.pickUp(element)
    },
    unHover() {
      this.hoverNodes.forEach(n => n.state.hover = false)
      this.hoverEdges.forEach(e => e.state.hover = false)
    },
    clearSelectors(evt) {
      // if(!evt.button && !this.$refs.contextMenu.$children[0].isActive) { ToDo: Вернуть
        this.selectedNodes.forEach(n => n.state.selected = false)
      // }
    },
    menuShow(event, object=null) {
      this.objectCtxMenu = object
      this.$refs.contextMenu.show_root(event.x, event.y)
    },
  },
  mounted() {
    this.setScreen(this.$refs.screen)
  }
}
</script>

<style scoped>
.disable-optimize {
  will-change: transform;
}
</style>