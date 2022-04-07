<template>
  <item-settings v-model="state" :title="title"/>
</template>

<script>
import ItemSettings from "@/components/Graph/GraphMenu/Settings/Modules/ItemSettings"
import {mapActions} from "vuex"

export default {
  name: "ItemClassifierSettings",
  components: {ItemSettings},
  props: {
    title: String,
    status: Boolean,
    id: Number
  },
  computed: {
    state: {
      get: function () {
        return this.status
      },
      set: function () {
        this.setClassifiersSettings(this.id)
      }
    }
  },
  methods: mapActions(['setClassifiersSettings'])
}
</script>

<style scoped>
.v-list-item {
  height: 30px;
  min-height: 30px;
}
</style>