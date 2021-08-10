<template>
  <div class="text-input-form">
    <body-input-form
      v-model="value"
      :rules="rules"
      :clearable="clearable"
      :hide-details="hideDetails"
      :class="bodyInputClasses"
      :placeholder="placeholder"
    >
      <template v-slot:label>
        {{title}}
      </template>
      <template v-slot:append="props">
        <v-icon v-if="deletable && props.hover" @click.stop="$emit('deletable')" size="24" class="action-icon">mdi-delete</v-icon>
        <v-icon v-else size="24">mdi-format-color-text</v-icon>
      </template>
      <template v-slot:message>
        <slot name="message"></slot>
      </template>
    </body-input-form>
  </div>
</template>

<script>

import BodyInputForm from "./BodyToForm/bodyInputForm"

export default {
  name: "textInput",
  components: {BodyInputForm},
  model: { prop: 'inputString', event: 'changeInputString', },
  props: {
    inputString: String,
    rules: {
      type: Array,
      default: function () {
        return []
      }
    },
    deletable: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: '',
    },
    hideDetails: {
      type: Boolean,
      default: false,
    },
    clearable: {
      type: Boolean,
      default: false,
    },
    placeholder: {
      type: String,
      default: 'Введите необходимое значение',
    },
  },
  computed: {
    bodyInputClasses: function () { return this.title.length ? '' : 'pt-0' },
    value: {
      get: function () { return this.inputString },
      set: function (value) { this.$emit('changeInputString', value) }
    }
  },
}
</script>

<style scoped>
.text-input-form {
  width: 100%;
}
.action-icon {
  cursor: pointer;
}
</style>