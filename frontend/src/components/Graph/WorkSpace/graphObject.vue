<template>
  <g
    @mousedown.capture="$emit('selectObject', object)"
    @mouseup.ctrl="$emit('setChoosingObject', object)"
    @mouseup.alt="$emit('setRelatedObjects', object)"
    @contextmenu.stop="$emit('ctxMenu', [$event, object])"
    @wheel.stop="scrollObject(object, $event)"
  >
    <v-label v-show="showLabel" :element="object">
      <information-label :size-node="object.size" :params="getClassifiers" :show-date="showDate"/>
    </v-label>

    <node ref="node" :data="object" :in-selected="inSelected" :selected-objects="selectedObjects">
      <body-object :object="object" :class="objectClass"/>
    </node>

    <foreignObject v-if="showTitle" v-bind="titleStyle">
      <div class="name-text" :style="titleTextStyle" oncontextmenu="return false">{{object.object.title}}</div>
    </foreignObject>
  </g>
</template>

<script>
import Node from '@/components/Graph/WorkSpace/lib/components/Node'
import VLabel from '@/components/Graph/WorkSpace/lib/components/Label'
import BodyObject from "@/components/Graph/WorkSpace/Modules/bodyObject"
import InformationLabel from "@/components/Graph/WorkSpace/Modules/informationLabel"
import scrollMixin from "@/components/Graph/WorkSpace/Modules/scrollMixin"
import {mapGetters} from "vuex"

export default {
  name: "graphObject",
  mixins: [scrollMixin],
  components: {Node, VLabel, BodyObject, InformationLabel},
  props: {
    object: Object,
    inSelected: Boolean,
    selectedObjects: Array
  },
  computed: {
    ...mapGetters(['globalDisplaySettingValue', 'classifiersSettings']),
    objectClass() {
      return this.inSelected ? 'choosing-object' : 'body-object'
    },
    showLabel() {
      let globalState = this.globalDisplaySettingValue('showGlobalTooltipObject')
      let classifiersLength = this.getClassifiers.length
      let localState = this.object.object.showTooltip
      return globalState && classifiersLength && localState
    },
    showDate() {
      let globalCreateDate = this.globalDisplaySettingValue('showGlobalDateObject')
      let localCreateDate = this.object.object.showCreateDate
      return globalCreateDate && localCreateDate
    },
    getClassifiers() {
      return this.object.object.params.filter(
        p => !this.classifiersSettings.includes(p.baseParam.id) && p.values.length
      )
    },
    showTitle() {
      return this.globalDisplaySettingValue('showGlobalTitle') && this.object.object.showTitle
    },
    titleStyle() {
      return {
        x: this.object.x + this.object.width / 2 - this.object.size / 2,
        y: this.object.y + this.object.height,
        width: `${this.object.size}px`,
        overflow: "visible",
        class: "pt-8",
        height: 1
      }
    },
    titleTextStyle() {
      return {fontSize: `${this.object.size/40}px`}
    }
  },
}
</script>

<style scoped>
.choosing-object {
  box-shadow: 0 0 50px red;
  transition: box-shadow 0.3s cubic-bezier(.25,.8,.25,1);
}

.choosing-object:hover {
  box-shadow: 0 0 80px red;
}
.body-object {
  box-shadow: 0 3px 5px -1px rgb(0 0 0 / 20%), 0 6px 10px 0 rgb(0 0 0 / 14%), 0 1px 18px 0 rgb(0 0 0 / 12%);
  transition: box-shadow 0.3s cubic-bezier(.25,.8,.25,1);
}
.body-object:hover {
  box-shadow: 0 7px 8px -4px rgb(0 0 0 / 20%), 0 12px 17px 2px rgb(0 0 0 / 14%), 0 5px 22px 4px rgb(0 0 0 / 12%);
}
.name-text {
  color: #444444;
  position: relative;
  background-color: white;
  width: fit-content;
  margin: auto;
}
</style>