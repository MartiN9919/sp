<template>
  <v-menu
    :close-on-content-click="false"
    offset-x offset-y z-index="10001" bottom right
    nudge-left="290"
    transition="slide-x-reverse-transition"
    min-width="auto" fixed>
    <template v-slot:activator="{ on }">
      <v-textarea
        row-height="1" auto-grow
        autocomplete="off"
        append-icon="mdi-calendar"
        v-model="value"
        :rules="rules"
        :label="title"
        placeholder="Выберете необходимую дату"
        hide-details readonly class="pt-0 mt-0" color="teal" type="text"
        v-on="on"
      ></v-textarea>
    </template>
    <v-card>
      <v-date-picker
        v-model="value"
        show-adjacent-months
        first-day-of-week="1"
        color="teal" locale="ru"
      ></v-date-picker>
    </v-card>
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
      set: function (value) { this.$emit('changeInputString', value) }
    }
  },
}
</script>

<style scoped>

</style>