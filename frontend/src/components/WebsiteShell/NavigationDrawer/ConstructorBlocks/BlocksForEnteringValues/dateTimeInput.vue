<template>
  <v-row>
    <v-col>
      <v-menu
        :close-on-content-click="false"
        offset-x offset-y z-index="10001" bottom right
        nudge-left="290"
        transition="slide-x-reverse-transition"
        min-width="auto" fixed>
        <template v-slot:activator="{ on }">
          <v-text-field
            autocomplete="off"
            append-icon="mdi-calendar"
            v-model="value.date"
            :label="'Дата - ' + title"
            placeholder="Выберете дату"
            hide-details readonly class="pt-0 mt-0" color="teal" type="text"
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker
          v-model="value.date"
          show-adjacent-months
          first-day-of-week="1"
          color="teal" locale="ru"
        ></v-date-picker>
      </v-menu>
    </v-col>
    <v-col>
      <v-menu
        :close-on-content-click="false"
        offset-x offset-y z-index="10001" bottom right
        nudge-left="290"
        transition="slide-x-reverse-transition"
        min-width="auto" fixed>
        <template v-slot:activator="{ on }">
          <v-text-field
            autocomplete="off"
            append-icon="mdi-clock-outline"
            v-model="value.time"
            :label="'Время - ' + title"
            placeholder="Выберете время"
            hide-details readonly class="pt-0 mt-0" color="teal" type="text"
            v-on="on"
          ></v-text-field>
        </template>
        <v-time-picker
          v-model="value.time"
          scrollable
          color="teal" format="24hr"
        ></v-time-picker>
      </v-menu>
    </v-col>
  </v-row>

</template>

<script>
export default {
  name: "dateTimeInput",
  props: {
    title: String,
    inputString: [String, Object, ],
  },
  model: { prop: 'inputString', event: 'changeInputString', },
  computed: {
    value: {
      get: function () { return this.inputString ? this.inputString : '' },
      set: function (value) { this.$emit('changeInputString', value) }
    }
  },
  created() {
    if (!this.value)
      this.value = { date: '', time: '', }
  },
}
</script>

<style scoped>
.v-picker__title {
  height: 50px;
}
</style>