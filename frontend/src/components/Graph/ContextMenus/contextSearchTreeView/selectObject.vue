<template>
  <v-card flat>
    <v-card-subtitle class="text-uppercase py-2 text-center text-break block-card-subtitle">
      {{header}}
    </v-card-subtitle>
    <v-divider></v-divider>
    <v-card-actions class="pa-1">
      <v-btn
       :disabled="!stepBack"
        @click="sendMessageParentComponent('changeWindow', stepBack)"
        icon color="teal"
      >
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <v-autocomplete
        :items="listItems" item-text="title"
        v-model="selectedObject" hide-details
        return-object color="teal" hide-no-data
        class="pa-0 ma-0 pb-2" item-color="teal"
      ></v-autocomplete>
      <v-btn
        @click="sendMessageParentComponent('getSelectedObject', stepNext)"
        icon color="teal" :disabled="importance && !selectedObject"
      >
        <v-icon>{{stepNext ? 'mdi-arrow-right' : 'mdi-check'}}</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "selectObject",
  props: {
    listItems: { type: Array, default: function () { return [] } },
    stepBack: { type: String, default: null },
    stepNext: { type: String, default: null },
    header: { type: String, default: null },
    selected: { type: Object, default: null },
    importance: { type: Boolean, default: false },
  },
  model: {prop: 'selected', event: 'changeSelected'},
  computed: {
    selectedObject: {
      get: function () { return this.selected },
      set: function (value) { this.$emit('changeSelected', value) }
    },
  },
  methods: {
    sendMessageParentComponent(method, fill) {
      this.$emit(method, fill)
    }
  }
}
</script>

<style scoped>
.block-card-subtitle {
  background-color: #009688;
  color: white !important;
}
</style>