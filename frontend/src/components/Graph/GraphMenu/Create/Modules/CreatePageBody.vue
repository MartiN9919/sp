<template>
  <div class="h-100">
    <div class="work-place">
      <slot name="header"/>

      <slot v-if="!editable" name="body"/>
    </div>
    <slot v-if="!editable" name="control"/>
  </div>
</template>

<script>
export default {
  name: "CreatePageBody",
  props: {
    editable: {
      type: Boolean,
      default: false
    },
    info: String,
  }
}
</script>

<style scoped>
.work-place {
  height: calc(100% - 44px);
  overflow-y: auto;
  overflow-x: hidden;
}
</style>