<template>
  <div @click.right.prevent.stop="menuShow($event)" @mousedown="clearSelectors" class="h-100">
    <screen ref="screen">
      <group v-if="relatedObjects.length" :nodes="relatedObjects"></group>
      <g
        v-show="globalDisplaySettingValue('showRelations')"
        v-for="relation in graphRelations" :key="relation.id"
        @wheel.stop="scrollRelation(relation, $event)"
        @click.right.prevent.stop="menuShow($event, relation)"
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
            :show-date="globalDisplaySettingValue('showGlobalDateRelation')"
          ></information-label>
        </v-label>
        <edge
          :ref="`edge-${relation.id}`"
          :data="relation"
          :nodes="graphObjects"
        ></edge>
      </g>
      <g
        :ref="`object-${object.id}`"
        v-for="object in graphObjects" :key="object.id"
        v-if="object.object.show"
        @wheel.stop="scroll(object, $event)"
        @click.ctrl.stop="addChoosingObject(object)"
        @click.alt.stop="getRelatedObjects(object, $event)"
        @click.right.prevent.stop="menuShow($event, object)"
        @click.stop="selectObject(object)"
      >
        <v-label
            :ref="`label-${object.id}`"
            v-show="getTooltipStateObject(object)"
            :element="object"
        >
          <information-label
              :size-node="object.size"
              :params="getObjectClassifiers(object)"
              :show-date="globalDisplaySettingValue('showGlobalDateObject')"
          ></information-label>
        </v-label>
        <node :ref="`node-${object.id}`" :data="object">
          <body-object
            :node="object"
            :selector="typeSelectorNode(object)"
            :show-triggers="getTriggersStateObject(object)"
          ></body-object>
        </node>
        <name-object
          v-show="getTitleStateObject(object)"
          :position="getTitlePosition(object)"
          :title="object.object.title"
          :size-node="object.size"
        ></name-object>
      </g>
    </screen>
    <graph-search v-if="graphObjects.length" :objects="graphObjects" @findNode="findNode"></graph-search>
    <context-menu-nested
      ref="contextMenu"
      :form="this"
      :items="contextMenu"
      :color="$CONST.APP.COLOR_OBJ"
    ></context-menu-nested>
  </div>
</template>

<script>
import dragMixin from '@/components/Graph/lib/mixins/drag'
import Screen from '@/components/Graph/lib/components/Screen'
import Node from '@/components/Graph/lib/components/Node'
import Edge from "@/components/Graph/lib/components/Edge"
import Group from "@/components/Graph/lib/components/Group"
import VLabel from '@/components/Graph/lib/components/Label'
import BodyObject from "@/components/Graph/WorkSpace/object/bodyObject"
import NameObject from "@/components/Graph/WorkSpace/object/nameObject"
import InformationLabel from "@/components/Graph/WorkSpace/object/informationLabel"
const GraphSearch = () => import("@/components/Graph/GraphMenu/graphSearch")
const ContextMenuNested = () => import("@/components/WebsiteShell/UIMainComponents/contextMenuNested")
import bodyContextMenu from "@/components/Graph/WorkSpace/bodyContextMenu"
import {mapActions, mapGetters} from "vuex"


export default {
  name: "graphArea",
  components: {GraphSearch, ContextMenuNested, Screen, Node, Edge, VLabel, Group, BodyObject, NameObject, InformationLabel},
  data: () => ({
    choosingObjects: [],
    relatedObjects: []
  }),
  mixins: [bodyContextMenu, dragMixin],
  computed: {
    ...mapGetters(['graphObjects', 'graphRelations', 'globalDisplaySettingValue', 'objectClassifiersSettings']),
    allowRelations() { return Array.from(this.$store.state.graph.rootInstances.relations, r => {return r.id}) },
  },
  methods: {
    ...mapActions(['setScreen']),
    typeSelectorNode(node) {
      if(this.choosingObjects.includes(node))
        return 'choosing'
      if(this.relatedObjects.includes(node))
        return 'related'
    },
    clearSelectors() {
      // this.choosingObjects = []
      this.relatedObjects = []
    },
    getRelatedObjects(node, e) {
      this.relatedObjects = []
      if (!this.relatedObjects.length) {
        let relations = this.graphRelations.filter(relation => relation.to === node.id || relation.from === node.id)
        for (let relation of relations) {
          this.relatedObjects.push(this.graphObjects.find(n => (n.id === relation.to || n.id === relation.from) && n.id !== node.id))
        }
        this.relatedObjects.push(node)
      }
    },
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
      return this.globalDisplaySettingValue('showGlobalTitle') && object.object.showTitle
    },
    getTooltipStateObject(object) {
      let globalState = this.globalDisplaySettingValue('showGlobalTooltipObject')
      let classifiersLength = this.getObjectClassifiers(object).length
      let localState = object.object.showTooltip
      return globalState && classifiersLength && localState
    },
    getTooltipStateRelation(relation) {
      return this.globalDisplaySettingValue('showGlobalTooltipRelation')
    },
    getTriggersStateObject(object) {
      return this.globalDisplaySettingValue('showGlobalTriggers') && object.object.showTriggers
    },
    scrollRelation(relation, event) {
      if(event.deltaY > 0 && relation.size / 1.5 > 300){
        relation.size /= 1.5
      }
      if (event.deltaY < 0 && relation.size * 1.5 < 1500){
        relation.size *= 1.5
      }
      this.$nextTick(() => {
        this.updateLabel(relation.id)
      })
    },
    scroll(node, event) {
      if(event.deltaY > 0 && node.size / 1.5 > 300){
        node.x += (((node.size/3) - (node.size/3)/1.5))/2
        node.y += (((node.size/3) - (node.size/3)/1.5))/2
        node.size /= 1.5
      }
      if (event.deltaY < 0 && node.size * 1.5 < 1500){
        node.x -= (((node.size/3)*1.5 - (node.size/3)))/2
        node.y -= (((node.size/3)*1.5 - (node.size/3)))/2
        node.size *= 1.5
      }
      this.$nextTick(() => {
        this.updateLabel(node.id)
        this.updateNode(node.id)
      })
    },
    getCoordinatesEdge(id){
      this.$nextTick(() => {
        return this.$refs.hasOwnProperty(`edge-${id}`) ? this.$refs[`edge-${id}`][0].pos : null
      })
    },
    updateLabel(id) {
      this.$refs[`label-${id}`][0].$refs.node.fitContent()
    },
    updateNode(id) {
      this.$refs[`node-${id}`][0].fitContent()
    },
  },
  mounted() {
    this.setScreen(this.$refs.screen)
  }
}
</script>

<style scoped>
</style>