<template>
  <v-menu
    :close-on-content-click="false" ref="menuDate" transition="slide-x-reverse-transition"
    offset-x offset-y bottom right fixed z-index="10001" min-width="auto" nudge-left="290"
  >
    <template v-slot:activator="{ on }">
      <v-textarea
        v-model="value" v-on="on" :rules="rules" :label="title"
        autocomplete="off" append-icon="mdi-calendar" row-height="1" auto-grow
        hide-details readonly class="pt-0 mt-0" color="teal" type="text" placeholder="Выберете необходимую дату"
      ></v-textarea>
    </template>
    <v-date-picker
      v-model="value" @click:date="$refs.menuDate.save()"
      show-adjacent-months first-day-of-week="1" color="teal" locale="ru"
    ></v-date-picker>
  </v-menu>
</template>

<script>
export default {
  name: "dateInput",
  props: {
    rules: Array,
    title: String,
    inputString: String,
  },
  model: { prop: 'inputString', event: 'changeInputString', },
  computed: {
    value: {
      get: function () { return this.inputString },
      set: function (value) { this.$emit('changeInputString', value) },
    },
  },
}
</script>

<style scoped>

</style>