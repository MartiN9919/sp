<template>
  <v-list link>
    <v-list-item v-for="item in booleanMenu" :key="item.value" @click="selectItem(item.value)">
      <v-list-item-title >{{ item.text }}</v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<script>
export default {
  name: "menuBoolean",
  props: {
    inputString: String,
    closeMenu: Function,
    booleanMenu: Array,
  },
  model: { prop: 'inputString', event: 'changeInputString', },
  computed: {
    value: {
      get: function () { return this.inputString },
      set: function (val) { this.$emit('changeInputString', val) }
    },
  },
  methods: {
    selectItem (selectedValue) {
      this.value = selectedValue
      this.closeMenu()
    }
  }
}
</script>

<style scoped>

</style>