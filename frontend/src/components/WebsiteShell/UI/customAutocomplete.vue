<template>
  <v-combobox
    :items="items" :item-text="itemText" v-model="selected" :disabled="disabled"
    return-object hide-details color="teal" hide-no-data item-color="teal"
    :menu-props="{ offsetY: true, maxWidth: '320', minWidth: '320' }"
  >
    <template v-slot:item="{ item }">
      <div class="py-1">{{item[itemText]}}</div>
    </template>
  </v-combobox>
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
      set: function (value) {
        if (this.items.find(item => item === value))
          this.$emit('changeInput', value)
        else this.$emit('changeInput', this.items[0])
      },
    },
  },

}
</script>

<style scoped>

</style>