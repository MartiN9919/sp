<template>
  <v-time-picker
    v-model="value"
    no-title
    full-width
    color="teal"
    format="24hr"
    ref="time"
  >
    <template v-slot:default>
      <v-btn text color="teal" @click="clickHour" class="type-btn hour-btn">Час.</v-btn>
      <v-btn :disabled="!isValidHour" text color="teal" @click="clickMinute" class="type-btn minute-btn">Мин.</v-btn>
    </template>
  </v-time-picker>
</template>

<script>
export default {
  name: "selectTime",
  props: {
    inputString: String,
  },
  model: {prop: 'inputString', event: 'changeInputString'},
  data: () => ({
    isValidHour: false,
    isValidMinute: false
  }),
  computed: {
    value: {
      get: function () {
        this.isValidHour = this.validateHour(this.inputString)
        this.isValidMinute = this.validateMinute(this.inputString)
        this.$emit('isValid', this.isValidHour && this.isValidMinute)
        if(this.isValidHour)
          this.clickMinute()
        else this.clickHour()
        return this.isValidMinute ? this.inputString : this.inputString + '00'
      },
      set: function (value) {
        this.$emit('changeInputString', value)
      }
    },
  },
  methods: {
    validateHour(time) {
      let timeArray = time.split(':')
      if(timeArray.length < 1 || timeArray[0].length < 2)
        return false
      let hour = parseInt(timeArray[0])
      return hour < 24;
    },
    validateMinute(time) {
      let timeArray = time.split(':')
      if(timeArray.length < 2 || timeArray[1].length < 2)
        return false
      let minute = parseInt(timeArray[1])
      return timeArray[1] < 60;
    },
    clickHour() {
      this.selecting = 1
      this.$nextTick(() => this.$refs.time.selecting = 1)
    },
    clickMinute() {
      this.selecting = 2
      this.$nextTick(() => this.$refs.time.selecting = 2)
    },
  }
}
</script>

<style scoped>
.type-btn {
  position: absolute;
  bottom: 0;
}

.hour-btn {
  left: 0;
}

.minute-btn {
  right: 0;
}

>>> .v-picker__actions {
  padding: 0;
}
</style>