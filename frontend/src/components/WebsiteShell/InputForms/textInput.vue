<template>
  <div class="text-input-form">
    <body-input-form
      v-model="value"
      v-bind="$attrs"
      :class="bodyInputClasses"
      :placeholder="$attrs.placeholder || 'Введите необходимое значение'"
      icon="mdi-format-color-text"
      @deletable="$emit('deletable')"
    >
      <template v-slot:message>
        <slot name="message"></slot>
      </template>
    </body-input-form>
  </div>
</template>

<script>
import BodyInputForm from "../UI/bodyInputForm"

export default {
  name: "textInput",
  components: {BodyInputForm},
  model: { prop: 'inputString', event: 'changeInputString', },
  props: {
    inputString: String,
  },
  computed: {
    bodyInputClasses: function () { return this.$attrs.hasOwnProperty('label') ? '' : 'pt-0' },
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
</style>