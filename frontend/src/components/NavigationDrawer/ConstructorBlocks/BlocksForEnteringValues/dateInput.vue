<template>
  <v-menu
    :close-on-content-click="false"
    offset-x offset-y z-index="10001" bottom right
    nudge-left="290"
    transition="slide-x-reverse-transition"
    min-width="auto" fixed>
    <template v-slot:activator="{ on }">
      <v-text-field
        autocomplete="off"
        append-icon="mdi-calendar"
        v-model="variable.value"
        :label="variable.title"
        placeholder="Выберете необходимую дату"
        hide-details readonly class="pt-0 mt-0" color="teal" type="text"
        v-on="on"
      ></v-text-field>
    </template>
    <v-card oncontextmenu="return false">
      <v-date-picker
        v-model="variable.value"
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
    variable: Object,
  },
}
</script>

<style scoped>

</style>