<template>
  <v-file-input
    v-model="value"
    :rules="rules"
    :clearable="clearable"
    :hide-details="hideDetails"
    :class="bodyInputClasses"
    :placeholder="placeholder"
    :disabled="disabled"
    accept="image/png, image/jpeg, image/bmp"
    prepend-icon=""
    truncate-length="200"
    show-size
    class="customInputFile"
    autocomplete="off"
    messages=" "
    color="teal"
    item-color="teal"
  >
    <template v-slot:label>
      {{title}}
    </template>
    <template v-slot:append>
      <v-hover v-slot="{ hover }" class="action-icon">
        <v-icon
            v-if="deletable && hover"
            @click.stop="$emit('deletable')"
            size="24"
        >mdi-delete</v-icon>
        <v-icon v-else size="24">mdi-camera</v-icon>
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
    clearable: {
      type: Boolean,
      default: false,
    },
    deletable: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    hideDetails: {
      type: Boolean,
      default: false,
    },
    placeholder: {
      type: String,
      default: 'Введите необходимое значение',
    },
    rules: {
      type: Array,
      default: function () {
        return []
      }
    },
    title: {
      type: String,
      default: '',
    },
  },
  computed: {
    bodyInputClasses: function () { return this.title.length ? 'pt-5' : '' },
    value: {
      get: function () { return this.inputString?.file },
      set: function (value) { this.$emit('changeInputString', {'file': value}) }
    },
  },
}
</script>

<style scoped>
.v-text-field {
  margin-top: 0;
  padding-top: 12px;
}
/*.customInputFile >>> input {*/
/*  padding: 0;*/
/*  cursor: pointer;*/
/*}*/
.customInputFile >>> .v-input__slot {
  align-items: flex-end;
  margin-bottom: 0;
}
.customInputFile >>> .v-input__append-inner {
  margin-top: 0 !important;
  cursor: pointer;
}
.customInputFile >>> .v-messages {
  min-height: 0;
}
.customInputFile >>> .v-text-field__details {
  min-height: 0;
}
.customInputFile >>> .v-text-field__slot {
  min-height: 0;
  cursor: pointer;
}
.action-icon {
  cursor: pointer;
}
.customInputFile {
  width: 100%;
}
</style>