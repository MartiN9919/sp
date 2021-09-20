<template>
  <div>
    <screen ref="screen">
      <g
        :ref="`object-${object.id}`"
        v-for="object in graphObjects" :key="object.id"
        @wheel.prevent.stop="scroll(object, $event)"
        @click.right="menuShow(object, $event)"
        @mousedown.capture="selectObject(object)"
      >
        <node :ref="`node-${object.id}`" :data="object">
          <body-object
            :node="object"
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
            @update="updateLabel(object.id)"
          ></information-label>
        </v-label>
        <name-object
          :visible="getTitleStateObject(object)"
          :position="getTitlePosition(object)"
          :title="object.object.title"
          :size-node="object.size"
        ></name-object>
      </g>
      <g
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
          ></information-label>
        </v-label>
        <edge
          :ref="`edge-${relation.id}`"
          :data="relation"
          :nodes="graphObjects"
        ></edge>
      </g>
    </screen>
    <context-menu-nested
      ref="contextMenu"
      :form="this"
      :items="contextMenu"
      color="teal"
    ></context-menu-nested>
  </div>
</template>

<script>
import Graph from "@/components/Graph/lib/graph"
import Screen from '@/components/Graph/lib/components/Screen'
import Node from '@/components/Graph/lib/components/Node'
import Edge from "@/components/Graph/lib/components/Edge"
import VLabel from '@/components/Graph/lib/components/Label'
import BodyObject from "@/components/Graph/WorkSpace/object/bodyObject"
import NameObject from "@/components/Graph/WorkSpace/object/nameObject"
import InformationLabel from "@/components/Graph/WorkSpace/object/informationLabel"
import ContextMenuNested from "@/components/WebsiteShell/ContextMenu/contextMenuNested"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "graphArea",
  components: {ContextMenuNested, Screen, Node, Edge, VLabel, BodyObject, NameObject, InformationLabel},
  data: () => ({
    graph: new Graph(),
    objectWithActivatedMenu: null,
  }),
  computed: {
    ...mapGetters(['graphObjects', 'graphRelations', 'globalDisplaySettings', 'objectClassifiersSettings']),
    allowRelations() { return Array.from(this.$store.state.graph.rootInstances.relations, r => {return r.id}) },
    changeTitle: {
      get: function () { return this.objectWithActivatedMenu.object.showTitle },
      set: function (value) { this.objectWithActivatedMenu.object.showTitle = value }
    },
    changeTooltip: {
      get: function () { return this.objectWithActivatedMenu.object.showTooltip },
      set: function (value) { this.objectWithActivatedMenu.object.showTooltip = value }
    },
    changeTriggers: {
      get: function () { return this.objectWithActivatedMenu.object.showTriggers },
      set: function (value) { this.objectWithActivatedMenu.object.showTriggers = value }
    },
    contextMenu: function () {
      return [
        {
          icon: 'mdi-pencil',
          title: 'Изменить',
          subtitle: 'Редактировать данный объект',
          action: 'setChangeObject'
        },
        {
          icon: 'mdi-cog-outline',
          title: 'Настройки',
          subtitle: 'Индивидуальные настройки объекта',
          menu: [
            {
              title: 'Отображение',
              menu: [
                {
                  title: 'Подпись',
                  model: 'changeTitle',
                },
                {
                  title: 'Заголовок',
                  model: 'changeTooltip'
                },
                {
                  title: 'Триггеры',
                  model: 'changeTriggers'
                }
              ]
            },
            {
              title: 'Классификаторы',
            },
          ],
        }
      ]
    }
  },
  methods: {
    selectObject(object) {
      this.graphObjects.push(object)
      this.graphObjects.splice(this.graphObjects.findIndex(o => o === object), 1)
    },
    setChangeObject(event) {
      console.log(event)
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
    menuShow(object, event) {
      this.objectWithActivatedMenu = object
      this.$refs.contextMenu.show_root(event.x, event.y)
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