<template>
  <v-file-input
    v-model="value"
    v-bind="$attrs"
    :class="bodyInputClasses"
    :placeholder="$attrs.placeholder || 'Выбирете файл'"
    :accept="accept"
    prepend-icon=""
    truncate-length="200"
    show-size
    class="customInputFile"
    autocomplete="off"
    messages=" "
    color="teal"
    item-color="teal"
  >
    <template v-slot:append>
      <v-hover v-slot="{ hover }">
        <v-icon
          v-if="$attrs.hasOwnProperty('deletable') && hover"
          @click.stop="$emit('deletable')"
          size="24"
          class="action-icon"
        >mdi-delete</v-icon>
        <v-icon v-else size="24">{{icon}}</v-icon>
      </v-hover>
    </template>
    <template v-slot:message>
      <slot name="message"></slot>
    </template>
  </v-file-input>
</template>

<script>
export default {
  name: "fileInput",
  model: { prop: 'inputString', event: 'changeInputString', },
  props: {
    inputString: Object,
    type: String,
  },
  computed: {
    bodyInputClasses: function () { return this.$attrs.hasOwnProperty('label') ? 'pt-2' : '' },
    accept: function () { return this.$attrs['type-load'] === 'photo' ? 'image/*' : '' },
    icon: function () { return this.$attrs['type-load'] === 'photo' ? 'mdi-file-image-outline' : 'mdi-file-outline' },
    value: {
      get: function () { return this.inputString?.file },
      set: function (value) {
        value
          ? this.$emit('changeInputString', {'file': value})
          : this.$emit('changeInputString', value)
      }
    },
  },
}
</script>

<style scoped>
.v-text-field {
  margin-top: 0;
  padding-top: 12px;
}
.customInputFile >>> .v-input__slot {
  align-items: flex-end;
  margin-bottom: 0;
  cursor: pointer;
}
.customInputFile >>> .v-messages {
  min-height: 0;
}
.customInputFile >>> .v-text-field__details {
  min-height: 0;
}
.customInputFile >>> .v-text-field__slot {
  min-height: 25px;
}
.action-icon {
  cursor: pointer;
}
.customInputFile {
  width: 100%;
}
</style>