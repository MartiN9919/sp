<template>
  <g>
    <edge :data="relation" :nodes="objects"/>
  </g>
</template>

<script>
import Edge from "@/components/Graph/lib/components/Edge"

export default {
  name: "graphRelation",
  components: {Edge},
  props: {
    relation: Object,
    objects: Array,
  }
}
</script>

<style scoped>

</style>