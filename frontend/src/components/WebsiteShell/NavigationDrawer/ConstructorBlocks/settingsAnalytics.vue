<template>
  <v-tooltip
    open-delay="1000" bottom nudge-bottom="-20" z-index="10001"
    transition="false" color="#00796B" max-width="20%"
  >
    <template v-slot:activator="{ on }">
      <v-row v-if="!list" no-gutters class="align-center noselect pb-3" v-on="on">
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
        <number-input
          v-else-if="type === 'number'"
          :title="title"
          v-model="value"
        ></number-input>
        <text-input
          v-else-if="type === 'phone_number'"
          :title="title"
          v-model="value"
        ></text-input>
        <text-input
          v-else-if="type === 'text'"
          :title="title"
          v-model="value"
        ></text-input>
      </v-row>
      <v-row v-else no-gutters class="align-center noselect pb-3" v-on="on">
<!--        <selector-input-->
<!--          :title="title"-->
<!--          v-model="value"-->
<!--          :list="list"-->
<!--        ></selector-input>-->
        <v-select
          :items="list" autocomplete="off" :label="title" attach v-model="value"
          :menu-props="{offsetY: true, maxWidth: '100%', minWidth: '100%'}"
          append-icon="mdi-format-list-bulleted" placeholder="Выберете необходимое значение"
          hide-details class="pt-0 mt-0 leaflet-grab" color="teal" type="text" item-color="teal"
        >
          <template v-slot:item="{ item }">
            <div class="py-1">{{item}}</div>
          </template>
        </v-select>
      </v-row>
    </template>
    <p class="text-formatter-for-window-size additional-text text-justify ma-0">
      {{hint ? hint : 'Описание отсутствует'}}
    </p>
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
import selectorInput from "./BlocksForEnteringValues/selectorInput";

export default {
  name: 'settingsAnalytics',
  components: {geometryInput, booleanInput, dateInput, dateTimeInput, numberInput, textInput, selectorInput, },
  props: {
    type: String,
    title: String,
    list: Array,
    hint: {type: String, default: ''},
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
