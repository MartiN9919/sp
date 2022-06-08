<template>
  <item-settings v-model="state" :title="title" :sub-title="subTitle">
    <v-switch disabled v-model="state" color="teal"/>
  </item-settings>
</template>

<script>
import ItemSettings from "@/components/Graph/GraphMenu/Settings/Modules/ItemSettings"

export default {
  name: "ItemGlobalSettings",
  components: {ItemSettings},
  model: {
    prop: 'value',
    event: 'changeValue'
  },
  props: {
    title: String,
    subTitle: String,
    value: Boolean
  },
  computed: {
    state: {
      get: function () {
        return this.value
      },
      set: function (value) {
        this.$emit('changeValue', value)
      }
    }
  }
}
</script>

<style scoped>

</style>