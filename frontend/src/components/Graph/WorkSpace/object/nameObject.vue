<template>
  <foreignObject :x="position.x" :y="position.y" :width="sizeNode" height="1" overflow="visible" class="pt-8">
    <div class="name-text" :style="{fontSize: sizeNode/40}">{{title}}</div>
  </foreignObject>
</template>

<script>
export default {
  name: "nameObject",
  props: {
    position: Object,
    title: String,
    sizeNode: Number,
  }
}
</script>

<style scoped>
  .name-text {
    color: #444444;
    position: relative;
    background-color: white;
    width: fit-content;
    margin: auto;
  }
</style>