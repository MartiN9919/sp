<template>
  <div class="title font-weight-light text text-center noselect" style="color: #80CBC4">
    {{ textHeader }}
  </div>
</template>

<script>
import '@/assets/css/noselect.css'

export default {
  name: 'blockHeader',
  props: {
    textHeader: String
  }
}
</script>

<style scoped>

</style>
