<template>
  <v-select
    v-model="selected"
    :items="baseObjects"
    :menu-props="{offsetY: true}"
    :prepend-inner-icon="objectIcon"
    class="v-input--dense selector-objects"
    label="Выбор типа создаваемого объекта"
    item-text="titleSingle"
    item-color="teal"
    item-value="id"
    color="teal"
    hide-details
    attach
    dense
    solo
  >
    <template v-slot:item="{ item }">
      <v-list-item-icon>
        <v-icon>{{ item.icon }}</v-icon>
      </v-list-item-icon>
      <v-list-item-title>
        {{ item.title }}
      </v-list-item-title>
    </template>
    <template v-slot:prepend-inner>
      <slot name="prepend-inner"></slot>
    </template>
  </v-select>
</template>

<script>
import {mapGetters} from "vuex"

export default {
  name: "SelectorObject",
  props: {
    selectedObject: Number,
    startObject: {
      type: Boolean,
      default: false,
    },
  },
  model: {
    prop: 'selectedObject',
    event: 'changeSelectedObject'
  },
  computed: {
    ...mapGetters(['baseObjects']),
    objectIcon: function () {
      return this.baseObjects.find(i => i.id === this.selected)?.icon
    },
    selected: {
      get: function () {
        if (this.selectedObject) {
          return this.selectedObject
        }
      },
      set: function (id) {
        this.$emit('changeSelectedObject', id)
      }
    }
  },
  mounted() {
    if(this.startObject) {
      this.selected = this.baseObjects[0].id
    }
  }
}
</script>

<style scoped>
.selector-objects >>> .v-input__slot {
  padding: 8px !important;
}
</style>