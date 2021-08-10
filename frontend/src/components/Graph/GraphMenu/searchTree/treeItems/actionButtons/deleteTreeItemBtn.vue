<template>
  <v-btn icon @click="deleteChildObject">
    <v-icon>mdi-delete</v-icon>
  </v-btn>
</template>

<script>
export default {
  name: "deleteTreeItemBtn",
  methods: {
    deleteChildObject() {
      this.$emit('deleteChildObject')
    }
  }
}
</script>

<style scoped>

</style>