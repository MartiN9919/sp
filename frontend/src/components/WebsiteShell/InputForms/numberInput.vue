<template>
  <div class="number-input-form">
    <body-input-form
      v-model="value"
      v-bind="$attrs"
      :placeholder="$attrs.placeholder || 'Введите необходимое значение'"
      :class="bodyInputClasses"
      icon="mdi-numeric"
      @keypress.native="isNumber"
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
  name: "numberInput",
  components: {BodyInputForm},
  model: { prop: 'inputString', event: 'changeInputString'},
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
  methods: {
    isNumber(event) {
      if(!this.value) {
        if (!Number(event.key) && !(event.key === '-'))
          return event.preventDefault()
      } else
      if (!Number(this.value + event.key))
        return event.preventDefault()
    }
  }
}
</script>

<style scoped>
.number-input-form {
  width: 100%;
}
</style>