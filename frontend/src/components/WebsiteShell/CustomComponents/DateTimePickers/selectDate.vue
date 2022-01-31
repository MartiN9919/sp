<template>
  <v-date-picker
    v-model="value"
    @click:date="action()"
    show-adjacent-months
    first-day-of-week="1"
    full-width
    color="teal"
    locale="ru"
  />
</template>

<script>
export default {
  name: "selectDate",
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
        const isValid = this.validateDate(this.inputString)
        this.$emit('isValid', isValid)
        return isValid ? this.reverseDate(this.inputString, '.', '-') : ''
      },
      set: function (value) {
        this.$emit('changeInputString', this.reverseDate(value, '-', '.'))
      }
    },
  },
  methods: {
    reverseDate(value, old, fresh) {
      return value.split(old).reverse().join(fresh)
    },
    validateDate(date) {
      const validate = date => {
        const daysInMonth = days => 28 + (days + Math.floor(days/8)) % 2 + 2 % days + 2 * Math.floor(1/days)
        const dateArray = date.split('.').map(v => parseInt(v))
        const leap = ((dateArray[2] % 4 === 0) && (dateArray[2] % 100 !== 0)) || (dateArray[2] % 400 === 0)
        return !(
          dateArray[1] < 1 || dateArray[1] > 12 || dateArray[0] < 1  //base rules
          || (dateArray[1] === 2 && (dateArray[0] > 29 || (!leap && dateArray[0] === 29))) //february
          || (dateArray[1] !== 2 && dateArray[0] > daysInMonth(dateArray[1])) //other month (no february)
        )
      }
      return date && date.length === 10 ? validate(date) : false
    }
  }
}
</script>

<style scoped>

</style>