<template>
  <item-settings v-if="isBoolean" v-model="state" :title="title" :sub-title="subTitle">
    <v-switch disabled v-model="state" color="teal"/>
  </item-settings>
  <item-settings v-else-if="isString" :title="title" :sub-title="subTitle">
    <v-text-field v-model="state" v-facade="mask" reverse color="teal" class="number-input"/>
  </item-settings>
</template>

<script>
import ItemSettings from "@/components/Graph/GraphMenu/Settings/Modules/ItemSettings"
import { facade } from 'vue-input-facade'

export default {
  name: "ItemSearchSettings",
  directives: { facade },
  components: {ItemSettings},
  model: {
    prop: 'value',
    event: 'changeValue'
  },
  props: {
    title: String,
    subTitle: String,
    value: [String, Boolean],
    props: Object
  },
  computed: {
    isBoolean: function () {
      return typeof this.state === 'boolean'
    },
    isString: function () {
      return typeof this.state === 'string'
    },
    mask: function () {
      return this.props ? this.props.mask : null
    },
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
.number-input {
  width: 3em
}
</style>