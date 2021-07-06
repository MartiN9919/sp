<template>
  <v-card flat>
    <v-card-subtitle class="text-uppercase py-2 text-center text-break block-card-subtitle">
      {{header}}
    </v-card-subtitle>
    <v-divider></v-divider>
    <v-card-text class="px-4 py-2">
      <v-autocomplete
        :items="listItems" item-text="title" v-model="selected" :disabled="disableSelectedObject"
        return-object hide-details color="teal" hide-no-data item-color="teal" class="pt-0"
      ></v-autocomplete>
      <v-switch
        v-model="isActualStatus" outlined hide-details color="teal"
        label="Поиск только по актуальным значениям"
      ></v-switch>
    </v-card-text>
      <v-card-actions>
        <v-btn outlined color="teal" width="40%" @click="$emit('stepBack')">Назад</v-btn>
        <v-spacer></v-spacer>
        <v-btn outlined color="teal" width="40%" @click="$emit('stepNext')">Продолжить</v-btn>
      </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "selectObject",
  props: {
    listItems: { type: Array, default: function () { return [] } },
    header: { type: String, default: null },
    selectedObject: { type: Object, default: null },
    isActual: { type: Boolean, default: false },
    disableSelectedObject: { type: Boolean, default: false },
  },
  computed: {
    selected: {
      get: function () { return this.selectedObject },
      set: function (value) { this.$emit('selectedObject', value) }
    },
    isActualStatus: {
      get: function () { return this.isActual },
      set: function (value) { this.$emit('isActual', value) },
    },
  },
}
</script>

<style scoped>
.block-card-subtitle {
  background-color: #009688;
  color: white !important;
}
</style>