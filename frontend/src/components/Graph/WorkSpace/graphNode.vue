<template>
  <g
    @mouseup.exact.stop="showDescription"
    @click.ctrl="selectObject"
    @wheel.stop="scrollObject(node, $event)"
    @mouseenter="emitHoverEvent('hover')"
    @mouseleave="emitHoverEvent('unhover')"
    @click.alt="$emit('setChoosingRelated')"
    @contextmenu.stop="$emit('ctxMenu', [$event, node])"
    oncontextmenu="return false"
  >
    <v-label v-show="showLabel" :element="node">
      <body-label :size="node.size" :params="getClassifiers" :show-date="showDate"/>
    </v-label>

    <node ref="node" :data="node" :in-selected="node.state.selected" :selected-objects="selectedObjects">
      <body-object :node="node" :showTriggers="showTriggers" :class="objectClass"/>
    </node>

    <foreignObject v-if="showTitle" v-bind="titleStyle">
      <div class="name-text" :style="titleTextStyle">{{title}}</div>
    </foreignObject>
    <foreignObject width="0" height="0">
      <description v-model="description" :params="params" :object-id="objectId" :rec-id="recId" :title="title"/>
    </foreignObject>
  </g>
</template>

<script>
import Node from '@/components/Graph/WorkSpace/lib/components/Node'
import VLabel from '@/components/Graph/WorkSpace/lib/components/Label'
import BodyObject from "@/components/Graph/WorkSpace/Modules/bodyObject"
import BodyLabel from "@/components/Graph/WorkSpace/Modules/Label/BodyLabel"
import Description from "@/components/Graph/WorkSpace/Modules/description"
import scrollMixin from "@/components/Graph/WorkSpace/Modules/scrollMixin"
import {mapGetters} from "vuex"

export default {
  name: "graphObject",
  mixins: [scrollMixin],
  components: {Description, Node, VLabel, BodyObject, BodyLabel},
  props: {
    node: Object,
    selectedObjects: Array
  },
  data: () => ({
    description: false
  }),
  computed: {
    ...mapGetters(['globalDisplaySettingValue', 'classifiersSettings', 'show']),
    objectClass() {
      if(this.node.state.selected) {
        return 'choosing-object'
      } else if(this.node.state.added) {
        return 'added-object'
        } else if(this.node.state.hover && this.globalDisplaySettingValue('linkHighlighting')) {
          return 'hover-object'
      } else return 'body-object'
    },
    showLabel() {
      let globalState = this.globalDisplaySettingValue('showGlobalTooltipObject')
      let classifiersLength = this.getClassifiers.length
      let localState = this.node.settings.showTooltip
      return globalState && classifiersLength && localState
    },
    showDate() {
      let globalCreateDate = this.globalDisplaySettingValue('showGlobalDateObject')
      let localCreateDate = this.node.settings.showCreateDate
      return globalCreateDate && localCreateDate
    },
    getClassifiers() {
      return this.params.filter(
        p => !this.classifiersSettings.includes(p.baseParam.id) && p.values.length
      )
    },
    showTitle() {
      return this.globalDisplaySettingValue('showGlobalTitle') && this.node.settings.showTitle
    },
    showTriggers() {
      return this.globalDisplaySettingValue('showGlobalTriggers') && this.node.settings.showTriggers
    },
    titleStyle() {
      return {
        x: this.node.x - this.node.size / 3,
        y: this.node.y + this.node.size / 3,
        width: `${this.node.size}px`,
        overflow: "visible",
        class: "pt-8",
        height: 1
      }
    },
    title() {
      return this.node.entity.title
    },
    titleTextStyle() {
      return {fontSize: `${this.node.size / 40}px`}
    },
    params() {
      return this.node.entity.params
    },
    objectId() {
      return this.node.ids.object_id
    },
    recId() {
      return this.node.ids.rec_id
    }
  },
  methods: {
    selectObject() {
      this.node.state.selected = !this.node.state.selected
    },
    emitHoverEvent(event) {
      if(!this.$refs.node.isMoved())
        this.$emit(event, this.node)
    },
    showDescription(event) {
      if(!event.button)
        this.description = true
    }
  }
}
</script>

<style scoped>
.hover-object {
  box-shadow: 0 0 50px blue;
  transition: box-shadow 0.3s cubic-bezier(.25,.8,.25,1);
}

.added-object {
  box-shadow: 0 0 75px purple;
  transition: box-shadow 0.3s cubic-bezier(.25,.8,.25,1);
}

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