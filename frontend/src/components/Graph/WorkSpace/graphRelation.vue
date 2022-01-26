<template>
  <g
    @wheel.stop="scrollObject(relation, $event)"
    @contextmenu.stop="$emit('ctxMenu', [$event, relation])"
    @mouseup.exact.stop="showDescription"
    @mouseenter="emitHoverEvent('hover')"
    @mouseleave="emitHoverEvent('unhover')"
    @click.alt="$emit('setChoosingRelated', relation)"
  >
    <edge ref="edge" :data="relation" :nodes="objects" :in-hover="inHover" :in-added="inAdded"/>
    <v-label ref="label" v-show="showLabel" :edge-coordinates="coordinatesEdge" :element="relation">
      <information-label :size-node="relation.size" :params="getClassifiers" :show-date="showDate"/>
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
    relation: Object,
    objects: Array,
    inAdded: Boolean,
    inHover: Boolean
  },
  data: () => ({
    description: false
  }),
  computed: {
    ...mapGetters(['globalDisplaySettingValue', 'classifiersSettings']),
    showLabel() {
      let globalState = this.globalDisplaySettingValue('showGlobalTooltipRelation')
      let classifiersLength = this.getClassifiers.length
      let localState = this.relation.relation.showTooltip
      return globalState && classifiersLength && localState
    },
    showDate() {
      let globalCreateDate = this.globalDisplaySettingValue('showGlobalDateRelation')
      let localCreateDate = this.relation.relation.showCreateDate
      return globalCreateDate && localCreateDate
    },
    coordinatesEdge(id){
      this.$nextTick(() => {
        return this.$refs.hasOwnProperty('edge') ? this.$refs.edge.pos : null
      })
    },
    getClassifiers() {
      return this.params.filter(p => p.values.length)
    },
    params() {
      return this.relation.relation.params
    },
  },
  methods: {
    emitHoverEvent(event) {
      !this.$refs.label.$refs.node.isMoved() && this.$emit(event, this.relation)
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