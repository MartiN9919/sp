<template>
  <component :is="selectComponent()" v-model="value" :type="type" v-bind="$attrs" @deletable="$emit('deletable')">
    <template v-slot:message>
      <slot name="message"></slot>
    </template>
  </component>
</template>

<script>
import geometryInput from "../InputForms/geometryInput"
import booleanInput from "../InputForms/booleanInput"
import dateInput from "../InputForms/dateInput"
import dateTimeInput from "../InputForms/dateTimeInput"
import numberInput from "../InputForms/numberInput"
import textInput from "../InputForms/textInput"
import selectorInput from "../InputForms/selectorInput"
import phoneInput from "../InputForms/phoneInput"
import fileInput from "../InputForms/fileInput"
import unknownInput from "../InputForms/unknownInput"

export default {
  name: 'responsiveInputForm',
  inheritAttrs: false,
  components: {phoneInput, geometryInput, booleanInput, dateInput, dateTimeInput, numberInput, textInput, selectorInput, fileInput, unknownInput},
  props: {
    inputString: [ String, Object, Boolean, Array, Number, Function],
    type: String,
  },
  model: { prop: 'inputString', event: 'changeInputString'},
  computed: {
    value: {
      get: function () { return this.inputString },
      set: function (value) { this.$emit('changeInputString', value) }
    }
  },
  methods: {
    selectComponent() {
      if (this.$attrs.items) return 'selectorInput'
      if (this.type === 'text') return 'textInput'
      if (this.type === 'geometry') return 'geometryInput'
      if (this.type === 'checkbox') return 'booleanInput'
      if (this.type === 'date') return 'dateInput'
      if (this.type === 'datetime') return 'dateTimeInput'
      if (this.type === 'number') return 'numberInput'
      if (this.type === 'phone_number') return 'phoneInput'
      if (this.type.startsWith('file')) return 'fileInput'
      return 'unknownInput'
    }
  }
}
</script>

<style scoped>

</style>
