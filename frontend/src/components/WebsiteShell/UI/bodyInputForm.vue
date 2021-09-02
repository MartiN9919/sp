<template>
  <v-text-field
    v-model="value"
    v-bind="$attrs"
    class="customTextField"
    autocomplete="off"
    messages=" "
    color="teal"
    @keypress="$emit('keypress', $event)"
  >
    <template v-slot:label>
      <slot name="label"></slot>
    </template>
    <template v-slot:message="{}">
      <slot name="message"></slot>
    </template>
    <template v-slot:append>
      <v-hover v-slot="{ hover }">
        <slot name="append" :hover="hover"></slot>
      </v-hover>
    </template>
  </v-text-field>
</template>

<script>
export default {
  name: "bodyInputForm",
  inheritAttrs: false,
  props: [ 'inputString', ],
  model: { prop: 'inputString', event: 'changeInputString', },
  computed: {
    value: {
      get: function () { return this.inputString },
      set: function (value) { this.$emit('changeInputString', value) }
    },
  },
}
</script>

<style scoped>
.v-text-field {
  margin-top: 0;
  padding-top: 12px;
}
.customTextField >>> .v-text-field__slot {
  position: initial !important;
}
.customTextField >>> input {
  padding: 0;
}
.customTextField >>> .v-input__slot {
  align-items: flex-end;
  margin-bottom: 0;
}
.customTextField >>> .v-input__append-inner {
  margin-top: 0 !important;
}
.customTextField >>> .v-messages {
  min-height: 0;
}
.customTextField >>> .v-text-field__details {
  min-height: 0;
}
</style>