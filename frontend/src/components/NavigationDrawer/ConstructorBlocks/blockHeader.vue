<template>
  <div class="title font-weight-light text text-center select_off" style="color: #80CBC4">
    {{ textHeader }}
  </div>
</template>

<script>
export default {
  name: 'blockHeader',
  props: {
    textHeader: String
  }
}
</script>

<style scoped>

</style>
