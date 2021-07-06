<template>
  <v-row no-gutters>
    <v-col>
      <v-menu
        v-model=menuDate :close-on-content-click="false"
        offset-x offset-y z-index="10001" bottom right
        nudge-left="290" ref="menuDate"
        transition="slide-x-reverse-transition"
        min-width="auto" fixed>
        <template v-slot:activator="{ on }">
          <v-textarea
            row-height="1" auto-grow
            autocomplete="off"
            append-icon="mdi-calendar"
            v-model="value.date"
            :label="'Дата - ' + title"
            placeholder="Выберете дату"
            hide-details readonly class="pt-0 mt-0" color="teal" type="text"
            v-on="on"
          ></v-textarea>
        </template>
        <v-date-picker
          v-if="menuDate"
          v-model="value.date"
          show-adjacent-months
          first-day-of-week="1"
          color="teal" locale="ru"
          @click:date="$refs.menuDate.save()"
        ></v-date-picker>
      </v-menu>
    </v-col>
    <v-col class="pl-4">
      <v-menu
        :close-on-content-click="false"
        v-model="menuTime"
        offset-x offset-y z-index="10001" bottom right
        nudge-left="290" ref="menuTime"
        transition="slide-x-reverse-transition"
        min-width="auto" fixed>
        <template v-slot:activator="{ on }">
          <v-textarea
            row-height="1" auto-grow
            autocomplete="off"
            append-icon="mdi-clock-outline"
            v-model="value.time"
            :label="'Время - ' + title"
            placeholder="Выберете время"
            hide-details readonly class="pt-0 mt-0" color="teal" type="text"
            v-on="on"
          ></v-textarea>
        </template>
        <v-time-picker
          v-if="menuTime"
          v-model="value.time"
          scrollable
          @click:minute="$refs.menuTime.save()"
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
  data: () => ({
    menuDate: false,
    menuTime: false,
  }),
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