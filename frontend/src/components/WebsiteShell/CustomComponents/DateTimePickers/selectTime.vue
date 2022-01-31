<template>
  <v-time-picker
    v-model="value"
    @click:minute=""
    full-width
    color="teal"
    format="24hr"
  />
</template>

<script>
export default {
  name: "selectTime",
  props: {
    inputString: String,
    action: {
      type: Function,
      default: () => {},
    },
  },
  model: {prop: 'inputString', event: 'changeInputString'},
  computed: {
    value: {
      get: function () {
        const isValid = this.validateTime(this.inputString)
        this.$emit('isValid', isValid)
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
    }
  }
}
</script>

<style scoped>

</style>