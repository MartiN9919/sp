<template>
  <v-row no-gutters class="align-center noselect pb-4">
    <geometry-input
      v-if="type === 'geometry'"
      :title="title"
      v-model="value"
    ></geometry-input>
    <boolean-input
      v-else-if="type === 'checkbox'"
      :title="title"
      v-model="value"
    ></boolean-input>
    <date-input
      v-else-if="type === 'date'"
      :title="title"
      v-model="value"
    ></date-input>
    <date-time-input
      v-else-if="type === 'datetime'"
      :title="title"
      v-model="value"
    ></date-time-input>
    <v-text-field
      autocomplete="off"
      v-else color="teal"
      :type="type"
      v-model="value"
      :label="title"
      placeholder="Введите значение"
      hide-details class="pt-0 mt-0"
    ></v-text-field>
  </v-row>
</template>

<script>
import '@/assets/css/noselect.css'
import geometryInput from "./BlocksForEnteringValues/geometryInput";
import booleanInput from "./BlocksForEnteringValues/booleanInput";
import dateInput from "./BlocksForEnteringValues/dateInput";
import dateTimeInput from "./BlocksForEnteringValues/dateTimeInput";

export default {
  name: 'settingsAnalytics',
  components: {geometryInput, booleanInput, dateInput, dateTimeInput, },
  props: {
    type: String,
    title: String,
    inputString: [String, Object, Boolean, Array, ],
  },
  model: { prop: 'inputString', event: 'changeInputString', },
  computed: {
    value: {
      get: function () { return this.inputString },
      set: function (value) { this.$emit('changeInputString', value) }
    }
  }
}
</script>

<style scoped>

</style>
