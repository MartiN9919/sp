<template>
  <td class="text-center pl-3" @click="addToGraph" style="cursor: pointer">
    <span class="teal--text">{{ doc ? doc.title : '' }}</span>
  </td>
</template>

<script>
export default {
  name: "Document",
  props: {
    doc: Object
  },
  methods: {
    addToGraph() {
      this.$emit('addToGraph', this.doc)
    },
  }
}
</script>

<style scoped>

</style>