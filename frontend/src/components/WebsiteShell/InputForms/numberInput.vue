<template>
  <div class="number-input-form">
    <body-input-form
      v-model="value"
      v-bind="$attrs"
      :rules="rules"
      :placeholder="$attrs.placeholder || 'Введите необходимое значение'"
      :class="bodyInputClasses"
      :clearable="false"
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
import BodyInputForm from "@/components/WebsiteShell/CustomComponents/bodyInputForm"

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
    },
    rules : function () {
      if (this.value) {
        let rule = [() => !isNaN(Number(this.value)) || 'Введите корректное число']
        return this.$attrs.hasOwnProperty('rules') ? rule.concat(this.$attrs.rules) : rule
      }
      else return this.$attrs.rules
    },
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