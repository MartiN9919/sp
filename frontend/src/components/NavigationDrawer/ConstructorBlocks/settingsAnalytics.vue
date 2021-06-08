<template>
  <v-tooltip bottom color="teal" z-index="10001" open-delay="1000">
    <template v-slot:activator="{ on }">
      <v-row no-gutters class="align-center noselect pb-4" v-on="on">
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
        ></date-time-input>
        <number-input
          v-else-if="variable.type === 'number'"
          :variable="variable"
        ></number-input>
        <text-input
          v-else-if="variable.type === 'text'"
          :variable="variable"
        ></text-input>
      </v-row>
    </template>
    <span>Описание: {{variable.hint}}</span>
  </v-tooltip>
</template>

<script>
import '@/assets/css/noselect.css'
import geometryInput from "./BlocksForEnteringValues/geometryInput";
import booleanInput from "./BlocksForEnteringValues/booleanInput";
import dateInput from "./BlocksForEnteringValues/dateInput";
import dateTimeInput from "./BlocksForEnteringValues/dateTimeInput";
import numberInput from "./BlocksForEnteringValues/numberInput";
import textInput from "./BlocksForEnteringValues/textInput";

export default {
  name: 'settingsAnalytics',
  components: { geometryInput, booleanInput, dateInput, dateTimeInput, numberInput, textInput, },
  props: {
    variable: Object
  },
}
</script>

<style scoped>

</style>
