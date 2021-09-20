<template>
  <v-select
    v-model="selected"
    :items="baseObjects"
    :menu-props="{offsetY: true}"
    :prepend-inner-icon="objectIcon"
    item-color="teal"
    hide-details
    item-value="id"
    item-text="titleSingle"
    solo color="teal"
    class="v-input--dense selector-objects"
    label="Выбор типа создоваемого объекта"
    attach
  >
    <template v-slot:item="{ item }">
      <v-list-item-icon><v-icon>{{ item.icon }}</v-icon></v-list-item-icon>
      <v-list-item-title>{{ item.title }}</v-list-item-title>
    </template>
  </v-select>
</template>

<script>
import {mapActions, mapGetters} from "vuex"

export default {
  name: "selectorObject",
  props: {
    selectedObject: Number,
    isGetClassifiers: {
      type: Boolean,
      default: true,
    },
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
    objectIcon: function () { return this.baseObjects.find(i => i.id === this.selected)?.icon },
    selected: {
      get: function () { if (this.selectedObject) return this.selectedObject },
      set: function (id) {
        if(this.isGetClassifiers) this.getClassifiers(id)
        else this.$emit('changeSelectedObject', id)
      }
    }
  },
  methods: {
    ...mapActions(['getBaseClassifiers']),
    getClassifiers(id) {
      this.getBaseClassifiers({params: {object_id: id}})
        .then(() => { return this.$emit('changeSelectedObject', id) })
    }
  },
  mounted() {
    if(this.startObject) this.selected = this.baseObjects[0].id
  }
}
</script>

<style scoped>
.selector-objects >>> .v-input__slot {
  padding: 8px !important;
}
</style>