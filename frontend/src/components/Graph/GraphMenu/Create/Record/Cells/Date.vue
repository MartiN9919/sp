<template>
  <td class="text-end text-no-wrap pl-3">
    <span>{{ date }}</span>
  </td>
</template>

<script>
export default {
  name: "Date",
  props: {
    date: String
  }
}
</script>

<style scoped>

</style>