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
      <v-btn text color="teal" @click="clickMinute" class="type-btn minute-btn">Мин.</v-btn>
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
  computed: {
    value: {
      get: function () {
        const isValid = this.validateTime(this.inputString)
        this.$emit('isValid', isValid)
        if(this.inputString.length < 3)
          this.clickHour()
        else this.clickMinute()
        return isValid ? this.inputString : ''
      },
      set: function (value) {
        this.$emit('changeInputString', value)
      }
    },
  },
  methods: {
    validateTime(time) {
      const timeArray = time.split(':').map(v => parseInt(v))
      return time.length === 5 && timeArray[0] < 24 && timeArray[1] < 60
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