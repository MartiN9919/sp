<template>
  <v-text-field
    v-model="variable.value"
    :label="variable.title"
    placeholder="Выберете необходимую дату"
    hide-details readonly class="pt-0 mt-0" color="teal" type="text"
  >
    <template v-slot:append>
      <v-menu offset-x z-index="10001" left :close-on-content-click="false" transition="slide-x-reverse-transition">
        <template v-slot:activator="{ on, attrs }">
          <v-icon v-bind="attrs" v-on="on"
            :color="attrs['aria-expanded'] === 'true' ? 'teal' : ''"
          >mdi-calendar</v-icon>
        </template>
        <v-date-picker
          v-model="variable.value"
          show-adjacent-months
          first-day-of-week="1"
          color="teal" locale="ru"
        ></v-date-picker>
      </v-menu>
    </template>
  </v-text-field>
</template>

<script>
export default {
  name: "dateInput",
  props: {
    variable: Object,
  }
}
</script>

<style scoped>

</style>