<template>
  <div class="title text-center select_off" style="color: #00796B">
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
