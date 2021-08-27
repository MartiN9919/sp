<template>
  <div class="d-flex flex-row justify-space-between flex-nowrap">
    <v-btn
      v-for="button in buttons"
      :key="button.action"
      :disabled="!button.disabled"
      @click="$emit(button.action)"
      color="teal"
      text
      right
      width="40%"
      height="3.5em"
    >{{button.title}}</v-btn>
  </div>
</template>

<script>
export default {
  name: "controlMenu",
  props: { buttons: Array},
}
</script>

<style scoped>

</style>