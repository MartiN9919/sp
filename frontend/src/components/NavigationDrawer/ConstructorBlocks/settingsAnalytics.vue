<template>
  <v-row no-gutters class="align-center noselect pb-4">
    <geometry-input
      v-if="variable.type === 'geometry'"
      :variable="variable">
    </geometry-input>
    <boolean-input
      v-else-if="variable.type === 'checkbox'"
      :variable="variable"
    ></boolean-input>
    <date-input
      v-else-if="variable.type === 'date'"
      :variable="variable"
    ></date-input>
    <date-time-input
      v-else-if="variable.type === 'datetime'"
      :variable="variable"
    >
    </date-time-input>
    <v-text-field
      v-else color="teal"
      :type="variable.type"
      v-model="variable.value"
      :label="variable.title"
      placeholder="Введите значение"
      hide-details class="pt-0 mt-0"
    ></v-text-field>
  </v-row>
</template>

<script>
import '@/assets/css/noselect.css'
import './BlocksForEnteringValues/mapDialogForGeometryInput'
import geometryInput from "./BlocksForEnteringValues/geometryInput";
import booleanInput from "./BlocksForEnteringValues/booleanInput";
import dateInput from "./BlocksForEnteringValues/dateInput";
import dateTimeInput from "./BlocksForEnteringValues/dateTimeInput";

export default {
  name: 'settingsAnalytics',
  components: {geometryInput, booleanInput, dateInput, dateTimeInput, },
  props: {
    variable: Object
  },
}
</script>

<style scoped>

</style>
