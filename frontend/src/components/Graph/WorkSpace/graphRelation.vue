<template>
  <g>
    <edge :data="relation" :nodes="objects"></edge>
    <v-label :element="relation" align="bottom" useDrag>
      <div class="v-card v-sheet theme--light v-card--hover" style="width: 440px; background-color: rgba(255, 255, 255, 0.5)">
        Hello
      </div>
    </v-label>
  </g>
</template>

<script>
import Edge from '../lib/components/Edge'
import VLabel from '../lib/components/Label'

export default {
  name: "graphRelation",
  components: {Edge, VLabel},
  props: {
    relation: Object,
    objects: Array,
  },
}
</script>

<style scoped>
</style>