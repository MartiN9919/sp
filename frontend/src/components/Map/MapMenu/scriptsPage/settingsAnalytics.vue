<template>
  <selector-input v-if="list" :title="title" v-model="value" :rules="rules" :list="list"></selector-input>
  <geometry-input v-else-if="type === 'geometry'" :title="title" :rules="rules" v-model="value"></geometry-input>
  <boolean-input v-else-if="type === 'checkbox'" :title="title" :rules="rules" v-model="value"></boolean-input>
  <date-input v-else-if="type === 'date'" :title="title" :rules="rules" v-model="value"></date-input>
  <date-time-input v-else-if="type === 'datetime'" :title="title" :rules="rules" v-model="value"></date-time-input>
  <number-input v-else-if="type === 'number'" :title="title" :rules="rules" v-model="value"></number-input>
  <text-input v-else-if="type === 'phone_number'" :title="title" :rules="rules" v-model="value"></text-input>
  <text-input v-else-if="type === 'text'" :title="title" :rules="rules" v-model="value"></text-input>
</template>

<script>
import '@/assets/css/noselect.css'
import geometryInput from "../../../WebsiteShell/InputForms/geometryInput";
import booleanInput from "../../../WebsiteShell/InputForms/booleanInput";
import dateInput from "../../../WebsiteShell/InputForms/dateInput";
import dateTimeInput from "../../../WebsiteShell/InputForms/dateTimeInput";
import numberInput from "../../../WebsiteShell/InputForms/numberInput";
import textInput from "../../../WebsiteShell/InputForms/textInput";
import selectorInput from "../../../WebsiteShell/InputForms/selectorInput";

export default {
  name: 'settingsAnalytics',
  components: {geometryInput, booleanInput, dateInput, dateTimeInput, numberInput, textInput, selectorInput, },
  props: {
    type: String,
    title: String,
    list: Array,
    inputString: [String, Object, Boolean, Array, ],
  },
  data: () => ({
    rules: [ v => !!v || 'Поле должно быть заполнено', ],
  }),
  model: { prop: 'inputString', event: 'changeInputString', },
  computed: {
    value: {
      get: function () { return this.inputString },
      set: function (value) { this.$emit('changeInputString', value) }
    }
  },
}
</script>

<style scoped>

</style>
