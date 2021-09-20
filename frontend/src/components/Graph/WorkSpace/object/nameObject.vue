<template>
  <foreignObject
      v-show="visible"
      height="1"
      :width="sizeNode"
      overflow="visible"
      :x="position.x"
      :y="position.y"
      class="pt-8"
  >
    <div style="text-align: center; color: #444444" :style="{fontSize: sizeNode/40}">{{title}}</div>
  </foreignObject>
</template>

<script>
export default {
  name: "nameObject",
  props: {
    visible: Boolean,
    position: Object,
    title: String,
    sizeNode: Number,
  }
}
</script>

<style scoped>

</style>