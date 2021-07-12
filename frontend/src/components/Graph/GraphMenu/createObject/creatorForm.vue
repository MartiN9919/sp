<template>
  <div>
    <selector-input
      v-model="value" v-if="classifier.list_id" :rules="rules"
      :title="classifier.title" :list="classifier.list_id"
    ></selector-input>
    <geometry-input
      v-else-if="classifier.type === 'geometry'" v-model="value"
      :title="classifier.title" :rules="rules"
    ></geometry-input>
    <boolean-input
      v-else-if="classifier.type === 'checkbox'" v-model="value"
      :title="classifier.title" :rules="rules"
    ></boolean-input>
    <date-input
      v-else-if="classifier.type === 'date'" v-model="value"
      :title="classifier.title" :rules="rules"
    ></date-input>
    <date-time-input
      v-else-if="classifier.type === 'datetime'" v-model="value"
      :title="classifier.title" :rules="rules"
    ></date-time-input>
    <number-input
      v-else-if="classifier.type === 'number'" v-model="value"
      :title="classifier.title" :rules="rules"
    ></number-input>
    <text-input
      v-else-if="classifier.type === 'phone_number'" v-model="value"
      :title="classifier.title" :rules="rules"
    ></text-input>
    <text-input
      v-else-if="classifier.type === 'text'" v-model="value"
      :title="classifier.title" :rules="rules"
    ></text-input>
    <slot></slot>
  </div>
</template>

<script>
import geometryInput from "../../../WebsiteShell/InputForms/geometryInput"
import booleanInput from "../../../WebsiteShell/InputForms/booleanInput"
import dateInput from "../../../WebsiteShell/InputForms/dateInput"
import dateTimeInput from "../../../WebsiteShell/InputForms/dateTimeInput"
import numberInput from "../../../WebsiteShell/InputForms/numberInput"
import textInput from "../../../WebsiteShell/InputForms/textInput"
import selectorInput from "../../../WebsiteShell/InputForms/selectorInput"

export default {
  name: "creatorForm",
  components: {geometryInput, booleanInput, dateInput, dateTimeInput, numberInput, textInput, selectorInput, },
  model: { prop: 'inputString', event: 'changeInputString', },
  props: {
    classifier: Object,
    inputString: String,
    workAreaId: Number,
  },
  data: () => ({
    valid: true,
    rules: [ v => !!v || 'Поле должно быть заполнено', ],
  }),
  computed: {
    value: {
      get: function () { return this.inputString },
      set: function (val) { this.$emit('changeInputString', val) },
    },
  },
}
</script>

<style scoped>

</style>