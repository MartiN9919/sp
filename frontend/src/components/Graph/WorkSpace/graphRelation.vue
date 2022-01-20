<template>
  <g @wheel.stop="scrollObject(relation, $event)" @contextmenu.stop="$emit('ctxMenu', [$event, relation])">
    <edge ref="edge" :data="relation" :nodes="objects" :in-hover="inHover"/>
    <v-label v-show="showLabel" :edge-coordinates="coordinatesEdge" :element="relation">
      <information-label :size-node="relation.size" :params="getClassifiers" :show-date="showDate"/>
    </v-label>
  </g>
</template>

<script>
import Edge from "@/components/Graph/WorkSpace/lib/components/Edge"
import VLabel from '@/components/Graph/WorkSpace/lib/components/Label'
import InformationLabel from "@/components/Graph/WorkSpace/Modules/informationLabel"
import scrollMixin from "@/components/Graph/WorkSpace/Modules/scrollMixin"
import {mapGetters} from "vuex"

export default {
  name: "graphRelation",
  mixins: [scrollMixin],
  components: {Edge, VLabel, InformationLabel},
  props: {
    relation: Object,
    objects: Array,
    inHover: Boolean
  },
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
      return this.relation.relation.params.filter(p => p.values.length)
    },
  },
  methods: {
    ctxMenu() {
      console.log(this.relation, this.objects)
    }
  }
}
</script>

<style scoped>

</style>