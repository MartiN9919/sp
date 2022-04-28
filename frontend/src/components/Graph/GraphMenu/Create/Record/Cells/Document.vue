<template>
  <td v-if="doc" class="text-center pl-3" @click="addToGraph" style="cursor: pointer">
    <span>{{ doc.title }}</span>
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