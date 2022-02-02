<template>
  <div v-intersect="onIntersect">
    <v-window v-model="bottomNavigation">
      <v-window-item key="date" value="date">
        <select-date v-model="date" @isValid="isDateValid"/>
      </v-window-item>
      <v-window-item key="time" value="time" eager>
        <select-time v-model="time" @isValid="isTimeValid"/>
      </v-window-item>
    </v-window>
    <v-bottom-navigation v-model="bottomNavigation" dark horizontal height="40" background-color="teal">
      <v-btn width="100%" value="date">
        <span>Дата</span>
        <v-icon>mdi-calendar</v-icon>
      </v-btn>
      <v-btn :disabled="!isValidDate" width="100%" value="time">
        <span>Время</span>
        <v-icon>mdi-clock-outline</v-icon>
      </v-btn>
    </v-bottom-navigation>
  </div>
</template>

<script>
import SelectDate from "@/components/WebsiteShell/CustomComponents/DateTimePickers/selectDate"
import SelectTime from "@/components/WebsiteShell/CustomComponents/DateTimePickers/selectTime"

export default {
  name: "selectDateTime",
  components: {SelectTime, SelectDate},
  props: {
    inputString: String,
  },
  model: {prop: 'inputString', event: 'changeInputString'},
  data: () => ({
    isValidDate: false,
    isValidTime: false,
    bottomNavigation: 'date',
  }),
  computed: {
    value: {
      get: function () {
        this.$emit('isValid', this.isValidDate && this.isValidTime)
        if(this.inputString) {
          let datetime = this.inputString.split(' ')
          if(datetime.length === 1) {
            datetime.push('')
          }
          return datetime
        } else {
          return ['', '']
        }
      },
      set: function (value) {
        this.$emit('changeInputString', value)
      }
    },
    date: {
      get: function () { return this.value[0] },
      set: function (date) {
        this.value = date + ' ' + this.value[1]
      },
    },
    time: {
      get: function () { return this.value[1] },
      set: function (time) {
        this.value = this.value[0] + ' ' + time
      },
    },
  },
  methods: {
    isDateValid(value) {
      this.isValidDate = value
      this.bottomNavigation = value ? 'time' : 'date'
    },
    isTimeValid(value) {
      this.isValidTime = value
    },
    onIntersect() {
      this.bottomNavigation = 'date'
    }
  }
}
</script>

<style scoped>

</style>