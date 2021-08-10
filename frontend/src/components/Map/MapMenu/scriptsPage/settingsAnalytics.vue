<template>
  <component :is="selectComponent()" v-model="value" v-bind="$attrs"></component>
</template>

<script>
import geometryInput from "../../../WebsiteShell/InputForms/geometryInput"
import booleanInput from "../../../WebsiteShell/InputForms/booleanInput"
import dateInput from "../../../WebsiteShell/InputForms/dateInput"
import dateTimeInput from "../../../WebsiteShell/InputForms/dateTimeInput"
import numberInput from "../../../WebsiteShell/InputForms/numberInput"
import textInput from "../../../WebsiteShell/InputForms/textInput"
import selectorInput from "../../../WebsiteShell/InputForms/selectorInput"
import phoneInput from "../../../WebsiteShell/InputForms/phoneInput"

export default {
  name: 'settingsAnalytics',
  inheritAttrs: false,
  components: {phoneInput, geometryInput, booleanInput, dateInput, dateTimeInput, numberInput, textInput, selectorInput, },
  props: {
    inputString: [ String, Object, Boolean, Array, Number, ],
    type: String,
  },
  model: { prop: 'inputString', event: 'changeInputString', },
  computed: {
    value: {
      get: function () { return this.inputString },
      set: function (value) { this.$emit('changeInputString', value) }
    }
  },
  methods: {
    selectComponent() {
      if (this.$attrs.list) return 'selectorInput'
      if (this.type === 'text') return 'textInput'
      if (this.type === 'geometry') return 'geometryInput'
      if (this.type === 'checkbox') return 'booleanInput'
      if (this.type === 'date') return 'dateInput'
      if (this.type === 'datetime') return 'dateTimeInput'
      if (this.type === 'number') return 'numberInput'
      if (this.type === 'phone_number') return 'phoneInput'
    }
  }
}
</script>

<style scoped>

</style>
