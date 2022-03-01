<template>
  <g
    @wheel.stop="scrollObject(edge, $event)"
    @mouseup.exact.stop="showDescription"
    @mouseenter="emitHoverEvent('hover')"
    @mouseleave="emitHoverEvent('unhover')"
    @click.alt="$emit('setChoosingRelated')"
    @contextmenu.stop="$emit('ctxMenu', [$event, edge])"
    oncontextmenu="return false"
  >
    <edge ref="edge" :edge="edge" :nodes="nodes" :in-hover="inHover"/>
    <v-label ref="label" v-show="showLabel" :element="edge">
      <information-label :size="edge.size" :params="getClassifiers" :show-date="showDate"/>
    </v-label>
    <foreignObject width="0" height="0">
      <description v-model="description" :params="params"/>
    </foreignObject>
  </g>
</template>

<script>
import Edge from "@/components/Graph/WorkSpace/lib/components/Edge"
import VLabel from '@/components/Graph/WorkSpace/lib/components/Label'
import InformationLabel from "@/components/Graph/WorkSpace/Modules/informationLabel"
import scrollMixin from "@/components/Graph/WorkSpace/Modules/scrollMixin"
import {mapGetters} from "vuex"
import Description from "@/components/Graph/WorkSpace/Modules/description";

export default {
  name: "graphRelation",
  mixins: [scrollMixin],
  components: {Description, Edge, VLabel, InformationLabel},
  props: {
    edge: Object,
    nodes: Array,
  },
  data: () => ({
    description: false
  }),
  computed: {
    ...mapGetters(['globalDisplaySettingValue', 'classifiersSettings']),
    showLabel() {
      let globalState = this.globalDisplaySettingValue('showGlobalTooltipRelation')
      let classifiersLength = this.getClassifiers.length
      let localState = this.edge.settings.showTooltip
      return globalState && classifiersLength && localState
    },
    showDate() {
      let globalCreateDate = this.globalDisplaySettingValue('showGlobalDateRelation')
      let localCreateDate = this.edge.settings.showCreateDate
      return globalCreateDate && localCreateDate
    },
    inHover() {
      return this.edge.state.hover && this.globalDisplaySettingValue('linkHighlighting')
    },
    getClassifiers() {
      return this.params.filter(p => p.values.length)
    },
    params() {
      return this.edge.entity.params
    },
  },
  methods: {
    emitHoverEvent(event) {
      if(!this.$refs.label.$refs.node.isMoved())
        this.$emit(event, this.edge)
    },
    showDescription(event) {
      if(!event.button)
        this.description = true
    }
  }
}
</script>

<style scoped>

</style>