<template>
  <g
    @mousedown.capture="$emit('selectObject', object)"
    @mouseup.ctrl="$emit('setChoosingObject', object.id)"
    @mouseup.alt="$emit('setRelatedObjects', object)"
    @wheel.stop="scrollObject"
    @click.stop=""
  >
    <v-label v-show="showLabel" :element="object">
      <information-label :size-node="object.size" :params="getClassifiers" :show-date="showDate"/>
    </v-label>

    <node ref="node" :data="object">
      <body-object :object="object" :class="objectClass"/>
    </node>

    <foreignObject v-if="showTitle" v-bind="titleStyle">
      <div class="name-text" :style="titleTextStyle">{{object.object.title}}</div>
    </foreignObject>
  </g>
</template>

<script>
import Node from '@/components/Graph/lib/components/Node'
import VLabel from '@/components/Graph/lib/components/Label'
import BodyObject from "@/components/Graph/Workspace/bodyObject"
import InformationLabel from "@/components/Graph/Workspace/informationLabel"
import {mapGetters} from "vuex";

export default {
  name: "graphObject",
  components: {Node, VLabel, BodyObject, InformationLabel},
  props: {
    object: Object,
    choosing: Boolean,
  },
  computed: {
    ...mapGetters(['globalDisplaySettingValue', 'classifiersSettings']),
    objectClass() {
      return this.choosing ? 'choosing-object' : 'body-object'
    },
    showLabel() {
      let globalState = this.globalDisplaySettingValue('showGlobalTooltipObject')
      let classifiersLength = this.getClassifiers.length
      let localState = this.object.object.showTooltip
      return globalState && classifiersLength && localState
    },
    showDate() {
      return this.globalDisplaySettingValue('showGlobalDateObject')
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
  methods: {
    scrollObject(event) {
      const minSize = 300
      const maxSize = 1500
      const coefficient = 1.5
      if(event.deltaY < 0 && this.object.size * coefficient < maxSize)
        this.changeObjectForScrolling(coefficient)
      else if (event.deltaY > 0 && this.object.size / coefficient > minSize)
        this.changeObjectForScrolling(1/ coefficient)
    },
    changeObjectForScrolling(coefficient) {
      const bodySize = this.object.size / 3
      const offset = (bodySize - bodySize * coefficient) / 2
      this.object.x += offset
      this.object.y += offset
      this.object.size *= coefficient
    }
  },
}
</script>

<style scoped>
.choosing-object {
  box-shadow: 0 3px 5px -1px rgb(255 0 0 / 20%), 0 6px 10px 0 rgb(255 0 0 / 14%), 0 1px 18px 0 rgb(255 0 0 / 12%);
  transition: box-shadow 0.3s cubic-bezier(.25,.8,.25,1);
}

.choosing-object:hover {
  box-shadow: 0 7px 8px -4px rgb(255 0 0 / 20%), 0 12px 17px 2px rgb(255 0 0 / 14%), 0 5px 22px 4px rgb(255 0 0 / 12%);
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