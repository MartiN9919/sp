<template>
  <div @click.right="menuShow($event)">
    <screen ref="screen">
      <g
        :ref="`object-${object.id}`"
        v-for="object in graphObjects" :key="object.id"
        @wheel.prevent.stop="scroll(object, $event)"
        @mousedown.ctrl.capture="addChoosingObject(object)"
        @click.right.prevent.stop="menuShow($event, object)"
        @mousedown.capture="selectObject(object)"
      >
        <node :ref="`node-${object.id}`" :data="object">
          <body-object
            :node="object"
            :selected="choosingObjects.includes(object)"
            :show-triggers="getTriggersStateObject(object)"
          ></body-object>
        </node>
        <v-label
          :ref="`label-${object.id}`"
          v-show="getTooltipStateObject(object)"
          :element="object"
        >
          <information-label
            :size-node="object.size"
            :params="getObjectClassifiers(object)"
            :show-date="globalDisplaySettings.showGlobalDateObject.state"
            @update="updateLabel(object.id)"
          ></information-label>
        </v-label>
        <name-object
          v-show="getTitleStateObject(object)"
          :position="getTitlePosition(object)"
          :title="object.object.title"
          :size-node="object.size"
        ></name-object>
      </g>
      <g
        v-show="globalDisplaySettings.showRelations.state"
        v-for="relation in graphRelations" :key="relation.id"
        @wheel.prevent.stop="scrollRelation(relation, $event)"
      >
        <v-label
          :ref="`label-${relation.id}`"
          v-show="getTooltipStateRelation(relation)"
          :edge-coordinates="getCoordinatesEdge(relation.id)"
          :element="relation"
        >
          <information-label
            :size-node="relation.size"
            :params="relation.relation.params"
            :show-date="globalDisplaySettings.showGlobalDateRelation.state"
          ></information-label>
        </v-label>
        <edge
          :ref="`edge-${relation.id}`"
          :data="relation"
          :nodes="graphObjects"
        ></edge>
      </g>
    </screen>
    <graph-search v-if="graphObjects.length" :objects="graphObjects" @findNode="findNode"></graph-search>
    <context-menu-nested
      ref="contextMenu"
      :form="this"
      :items="contextMenu"
      color="teal"
    ></context-menu-nested>
  </div>
</template>

<script>
import Screen from '@/components/Graph/lib/components/Screen'
import Node from '@/components/Graph/lib/components/Node'
import Edge from "@/components/Graph/lib/components/Edge"
import VLabel from '@/components/Graph/lib/components/Label'
import BodyObject from "@/components/Graph/WorkSpace/object/bodyObject"
import NameObject from "@/components/Graph/WorkSpace/object/nameObject"
import InformationLabel from "@/components/Graph/WorkSpace/object/informationLabel"
import ContextMenuNested from "@/components/WebsiteShell/ContextMenu/contextMenuNested"
import bodyContextMenu from "./bodyContextMenu"
import {mapActions, mapGetters} from "vuex"
import GraphSearch from "@/components/Graph/GraphMenu/graphSearch";


export default {
  name: "graphArea",
  components: {GraphSearch, ContextMenuNested, Screen, Node, Edge, VLabel, BodyObject, NameObject, InformationLabel},
  data: () => ({
    choosingObjects: [],
  }),
  mixins : [
      bodyContextMenu
  ],
  computed: {
    ...mapGetters(['graphObjects', 'graphRelations', 'globalDisplaySettings', 'objectClassifiersSettings']),
    allowRelations() { return Array.from(this.$store.state.graph.rootInstances.relations, r => {return r.id}) },
  },
  methods: {
    findNode(node) {
      this.$refs.screen.panNode(node, { offsetX: 0, offsetY: 0 })
    },
    addChoosingObject(choosingObject){
      let findIndex = this.choosingObjects.findIndex(object => object === choosingObject)
      if(findIndex === -1){
        this.choosingObjects.push(choosingObject)
      } else{
        this.choosingObjects.splice(findIndex,1)
      }
    },
    selectObject(object) {
      this.graphObjects.push(object)
      this.graphObjects.splice(this.graphObjects.findIndex(o => o === object), 1)
    },
    getObjectClassifiers(object) {
      let enabledClassifiers = this.objectClassifiersSettings(object.object.object.id)
      return object.object.params.filter(p => enabledClassifiers.includes(p.baseParam.id) && p.values.length !== 0)
    },
    getTitlePosition(object) {
      return {x: object.x + object.width / 2 - object.size / 2, y: object.y + object.height}
    },
    getTitleStateObject(object) {
      return this.globalDisplaySettings.showGlobalTitle.state && object.object.showTitle
    },
    getTooltipStateObject(object) {
      let globalState = this.globalDisplaySettings.showGlobalTooltipObject.state
      let classifiersLength = this.getObjectClassifiers(object).length
      let localState = object.object.showTooltip
      this.$nextTick(() => {
        this.updateLabel(object.id)
      })
      return globalState && classifiersLength && localState
    },
    getTooltipStateRelation(relation) {
      this.$nextTick(() => {
        this.updateLabel(relation.id)
      })
      return this.globalDisplaySettings.showGlobalTooltipRelation.state
    },
    getTriggersStateObject(object) {
      return this.globalDisplaySettings.showGlobalTriggers.state && object.object.showTriggers
    },
    scrollRelation(relation, event) {
      if(event.deltaY > 0 && relation.size / 1.05 > 300){
        relation.size /= 1.05
      }
      if (event.deltaY < 0 && relation.size * 1.05 < 1200){
        relation.size *= 1.05
      }
      this.$nextTick(() => {
        this.updateLabel(relation.id)
      })
    },
    scroll(node, event) {
      if(event.deltaY > 0 && node.size / 1.05 > 300){
        node.x += (((node.size/3) - (node.size/3)/1.05))/2
        node.y += (((node.size/3) - (node.size/3)/1.05))/2
        node.size /= 1.05
      }
      if (event.deltaY < 0 && node.size * 1.05 < 1200){
        node.x -= (((node.size/3)*1.05 - (node.size/3)))/2
        node.y -= (((node.size/3)*1.05 - (node.size/3)))/2
        node.size *= 1.05
      }
      this.$nextTick(() => {
        this.updateLabel(node.id)
        this.updateNode(node.id)
      })
    },
    getCoordinatesEdge(id){
      return this.$refs.hasOwnProperty(`edge-${id}`) ? this.$refs[`edge-${id}`][0].pos : null
    },
    updateLabel(id) {
      this.$refs[`label-${id}`][0].$refs.node.fitContent()
    },
    updateNode(id) {
      this.$refs[`node-${id}`][0].fitContent()
    },
  },
}
</script>

<style scoped>
</style>