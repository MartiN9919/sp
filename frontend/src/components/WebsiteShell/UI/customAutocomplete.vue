<template>
  <v-autocomplete
    :items="items" :item-text="itemText" v-model="selected" :disabled="disabled"
    return-object hide-details color="teal" hide-no-data item-color="teal"
    :menu-props="{ maxWidth: '23em', minWidth: '23em' }"
  ></v-autocomplete>
</template>

<script>
export default {
  name: "customAutocomplete",
  props: {
    items: Array,
    input: Object,
    itemText: String,
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  model: {
    prop: 'input',
    event: 'changeInput',
  },
  computed: {
    selected: {
      get: function () { return this.input },
      set: function (value) { this.$emit('changeInput', value) },
    },
  },
}
</script>

<style scoped>

</style>