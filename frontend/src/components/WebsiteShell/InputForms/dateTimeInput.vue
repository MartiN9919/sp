<template>
  <v-menu
    :close-on-content-click="false" ref="menuDateTime" transition="slide-x-reverse-transition"
    offset-x offset-y bottom right fixed z-index="10001" min-width="auto" nudge-left="290"
  >
    <template v-slot:activator="{ on }">
      <v-textarea
        v-model="value"
        v-on="on" :rules="rulesDateTime" :label="'Дата и время - ' + title"
        autocomplete="off" append-icon="mdi-calendar-clock" row-height="1" auto-grow
        hide-details readonly class="pt-0 mt-0" color="teal" type="text" placeholder="Выберете дату"
      ></v-textarea>
    </template>
      <v-window v-model="bottomNavigation">
      <v-window-item key="date" value="date">
        <v-date-picker
          v-model="date" @click:date="bottomNavigation = 'time'"
          show-adjacent-months first-day-of-week="1" color="teal" locale="ru"
        ></v-date-picker>
      </v-window-item>
      <v-window-item key="time" value="time">
        <v-time-picker
          v-model="time" @click:minute="$refs.menuDateTime.save(); bottomNavigation = 'date'"
          scrollable color="teal" format="24hr"
        ></v-time-picker>
      </v-window-item>
    </v-window>
    <v-bottom-navigation v-model="bottomNavigation" dark horizontal height="40" background-color="teal">
      <v-btn value="date"><span>Дата</span><v-icon>mdi-calendar</v-icon></v-btn>
      <v-btn value="time"><span>Время</span><v-icon>mdi-clock-outline</v-icon></v-btn>
    </v-bottom-navigation>
  </v-menu>
</template>

<script>
export default {
  name: "dateTimeInput",
  props: {
    rules: { type: Array, default: () => { return [] }},
    title: String,
    inputString: String,
  },
  model: { prop: 'inputString', event: 'changeInputString', },
  data: () => ({
    bottomNavigation: 'date',
  }),
  computed: {
    rulesDateTime : function () {
      if (this.value) return [v => (v || '').split(' ').length > 1 || 'Введите все значения'].concat(this.rules)
      else return this.rules
    },
    value: {
      get: function () { return this.inputString },
      set: function (val) { this.$emit('changeInputString', val) }
    },
    date: {
      get: function () { return this.calculateValue('-') },
      set: function (date) { this.changeValue('-', date) },
    },
    time: {
      get: function () { return this.calculateValue(':') },
      set: function (time) { this.changeValue(':', time) },
    },
  },
  methods: {
    calculateValue (typeForSplit) {
      if (this.value) {
        let dateTime = this.value.split(' ')
        if (dateTime.length === 1) {
          if (this.value.split(typeForSplit).length > 1)
            return this.value
        } else {
          if (typeForSplit === '-') return dateTime[0]
          if (typeForSplit === ':') return dateTime[1]
        }
      } else return ''
    },
    changeValue (typeForSplit, value) {
      if (this.value) {
        let dateTime = this.value.split(' ')
        if (dateTime.length === 1)
          if (this.value.split(typeForSplit).length > 1)
            this.value = value
          else {
            if (typeForSplit === '-')
              this.value = value + ' ' + this.value
            if (typeForSplit === ':')
              this.value = this.value + ' ' + value
          }
        else {
          if (typeForSplit === '-')
            dateTime[0] = value
          if (typeForSplit === ':')
            dateTime[1] = value
          this.value = dateTime.join(' ')
        }
      } else this.value = value
    },
  },
}
</script>

<style scoped>

</style>