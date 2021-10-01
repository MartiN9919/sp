<template>
  <div class="phone-number-form">
    <body-input-form
      v-model="value"
      v-bind="$attrs"
      :class="bodyInputClasses"
      :placeholder="$attrs.placeholder || 'Введите номер телефона'"
      @keypress.native="isNumber"
      @deletable="$emit('deletable')"
      icon="mdi-cellphone"
      prefix="+"
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
  name: "phoneInput",
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
    },
  },
  methods: {
    isNumber(event) {
      if (event.key === ' ' || event.key === '.')
        return event.preventDefault()
      if(!this.value) {
        if (!Number(event.key))
          return event.preventDefault()
      } else
      if (!Number(this.value + event.key))
        return event.preventDefault()
    }
  }
}
</script>

<style scoped>
.phone-number-form {
  width: 100%;
}
</style>