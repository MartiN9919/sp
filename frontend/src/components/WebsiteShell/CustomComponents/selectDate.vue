<template>
  <div>
    <v-date-picker
        v-model="value" @click:date="closeMenu()"
        show-adjacent-months first-day-of-week="1" color="teal" locale="ru"
    ></v-date-picker>
  </div>
</template>

<script>
export default {
  name: "selectDate",
  props: {
    inputString: String,
    closeMenu: Function,
  },
  model: { prop: 'inputString', event: 'changeInputString', },
  data: () => ({
    bottomNavigation: 'date',
  }),
  computed: {
    value: {
      get: function () {
        return this.inputString
      },
      set: function (val) {
        this.$emit('changeInputString', val)
      }
    },
  }
}
</script>

<style scoped>

</style>