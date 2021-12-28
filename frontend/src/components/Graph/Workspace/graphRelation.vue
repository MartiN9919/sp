<template>
  <g>
    <edge ref="edge" :data="relation" :nodes="objects"/>
    <v-label v-show="showLabel" :edge-coordinates="coordinatesEdge" :element="relation">
      <information-label :size-node="relation.size" :params="getClassifiers" :show-date="showDate"/>
    </v-label>
  </g>
</template>

<script>
import Edge from "@/components/Graph/lib/components/Edge"
import VLabel from '@/components/Graph/lib/components/Label'
import InformationLabel from "@/components/Graph/Workspace/informationLabel"
import {mapGetters} from "vuex"

export default {
  name: "graphRelation",
  components: {Edge, VLabel, InformationLabel},
  props: {
    relation: Object,
    objects: Array,
  },
  computed: {
    ...mapGetters(['globalDisplaySettingValue', 'classifiersSettings']),
    showLabel() {
      return this.globalDisplaySettingValue('showGlobalTooltipRelation')
    },
    showDate() {
      return this.globalDisplaySettingValue('showGlobalDateRelation')
    },
    coordinatesEdge(id){
      this.$nextTick(() => {
        return this.$refs.hasOwnProperty('edge') ? this.$refs.edge.pos : null
      })
    },
    getClassifiers() {
      return this.relation.relation.params.filter(
          p => p.values.length
      )
    },
  }
}
</script>

<style scoped>

</style>