<template>
  <div class="pt-2">
    <slot name="message"></slot>
    <v-text-field
      v-model="newValue" @mouseover.native="newHover = true" @mouseleave.native="newHover = false"
      dense outlined hide-details color="teal" autocomplete="off" messages=" " class="treeItemInput"
    >
      <template v-slot:append-outer="">
        <slot name="append-outer"></slot>
      </template>
      <template v-slot:append="">
        <slot name="append"></slot>
      </template>
    </v-text-field>
  </div>
</template>

<script>
export default {
  name: "bodyInputTreeItem",
  props: {
    hover: Boolean,
    value: String,
  },
  model: {
    prop: 'value',
    event: 'changeValue',
  },
  computed: {
    newHover: {
      get: function () { return this.hover },
      set: function (value) { this.$emit('changeHover', value) },
    },
    newValue: {
      get: function () { return this.value },
      set: function (value) { this.$emit('changeValue', value) },
    }
  },
}
</script>

<style scoped>
.treeItemInput >>> .v-input__append-inner {
  margin-top: 2 !important;
}
.treeItemInput >>> .v-input__append-outer {
  margin-top: 2 !important;
}
</style>