<template>
  <div v-intersect="onIntersect">
    <v-window v-model="bottomNavigation">
      <v-window-item key="dateStart" value="dateStart">
        <select-date v-model="dateStart" @isValid="isDateStartValid"/>
      </v-window-item>
      <v-window-item key="dateEnd" value="dateEnd" eager>
        <select-date v-model="dateEnd" @isValid="isDateEndValid"/>
      </v-window-item>
    </v-window>
    <v-bottom-navigation v-model="bottomNavigation" dark horizontal height="40" background-color="teal">
      <v-btn width="100%" value="dateStart">
        <span>Дата начала</span>
        <v-icon>mdi-calendar</v-icon>
      </v-btn>
      <v-btn :disabled="!isValidDateStart" width="100%" value="dateEnd">
        <span>Дата конца</span>
        <v-icon>mdi-calendar</v-icon>
      </v-btn>
    </v-bottom-navigation>
  </div>
</template>

<script>
import SelectDate from "@/components/WebsiteShell/CustomComponents/DateTimePickers/selectDate"

export default {
  name: "selectPeriod",
  components: {SelectDate},
  props: {
    inputString: String,
  },
  model: {prop: 'inputString', event: 'changeInputString'},
  data: () => ({
    isValidDateStart: false,
    isValidDateEnd: false,
    bottomNavigation: 'dateStart',
  }),
  computed: {
    value: {
      get: function () {
        this.$emit('isValid', this.isValidDateStart && this.isValidDateEnd)
        if(this.inputString) {
          let period = this.inputString.split('-')
          if(period.length === 1) {
            period.push('')
          }
          return period
        } else {
          return ['', '']
        }
      },
      set: function (value) {
        this.$emit('changeInputString', value)
      }
    },
    dateStart: {
      get: function () { return this.value[0] },
      set: function (date) {
        this.value = date + '-' + this.value[1]
      },
    },
    dateEnd: {
      get: function () { return this.value[1] },
      set: function (date) {
        this.value = this.value[0] + '-' + date
      },
    },
  },
  methods: {
    isDateStartValid(value) {
      this.isValidDateStart = value
      this.bottomNavigation = value ? 'dateEnd' : 'dateStart'
    },
    isDateEndValid(value) {
      this.isValidDateEnd = value
    },
    onIntersect(value) {
      if(!value[0].isIntersecting && this.isValidDateStart && !this.dateEnd.length) {
        this.dateEnd = new Date().toLocaleDateString('ru-RU')
      }
      this.bottomNavigation = 'dateStart'
    }
  }
}
</script>

<style scoped>

</style>