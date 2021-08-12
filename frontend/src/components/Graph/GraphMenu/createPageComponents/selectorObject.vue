<template>
  <v-select
    v-model="selected"
    :items="items"
    :menu-props="{offsetY: true}"
    item-color="teal"
    hide-details
    return-object
    item-text="title"
    solo color="teal"
    class="v-input--dense selector-objects"
    label="Выбор типа создоваемого объекта"
    attach
  ></v-select>
</template>

<script>
export default {
  name: "selectorObject",
  props: {
    items: Array,
    selectedObject: Object,
  },
  model: {
    prop: 'selectedObject',
    event: 'changeSelectedObject',
  },
  computed: {
    selected: {
      get: function () { return this.selectedObject },
      set: function (object) { this.$emit('changeSelectedObject', object) }
    }
  }
}
</script>

<style scoped>
.selector-objects >>> .v-input__slot {
  padding: 8 !important;
}
</style>