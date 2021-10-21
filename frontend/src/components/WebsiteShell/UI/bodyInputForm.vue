<template>
  <v-text-field
    v-model="value"
    v-bind="$attrs"
    class="customTextField"
    autocomplete="off"
    messages=" "
    :color="$CONST.APP.COLOR_OBJ"
  >
    <template v-slot:message="{}">
      <slot name="message"></slot>
    </template>
    <template v-slot:append>
      <v-hover v-slot="{ hover }">
        <v-icon
          v-if="$attrs.hasOwnProperty('deletable') && hover"
          @click.stop="$emit('deletable')"
          size="24"
          class="action-icon"
        >mdi-delete</v-icon>
        <v-icon size="24" v-else>{{$attrs.icon}}</v-icon>
      </v-hover>
    </template>
  </v-text-field>
</template>

<script>
export default {
  name: "bodyInputForm",
  inheritAttrs: false,
  props: ['inputString'],
  model: {
    prop: 'inputString',
    event: 'changeInputString'
  },
  computed: {
    value: {
      get: function () {
        return this.inputString
      },
      set: function (value) {
        this.$emit('changeInputString', value)
      }
    }
  }
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