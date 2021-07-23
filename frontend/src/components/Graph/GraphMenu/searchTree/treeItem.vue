<template>
  <v-text-field v-model="inputString" hide-details outlined dense class="mt-2" color="teal" autocomplete="off">
    <template v-slot:label="">
      <slot name="label"></slot>
    </template>
    <template v-slot:append="">
      <slot name="append"></slot>
    </template>
    <template v-slot:append-outer="">
      <slot name="append-outer"></slot>
    </template>
  </v-text-field>
</template>

<script>
export default {
  name: "treeItem",
  model: { prop: 'request', event: 'changeRequest'},
  props: {
    request: String ,
  },
  computed: {
    inputString: {
      get: function () { return this.request },
      set: function (value) { this.$emit('changeRequest', value) }
    }
  }
}
</script>

<style>
.v-treeview-node__root {
  padding: 0 !important;
}
</style>