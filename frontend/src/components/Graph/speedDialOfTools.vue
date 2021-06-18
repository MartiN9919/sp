<template>
  <v-speed-dial absolute right bottom direction="top" open-on-hover transition="slide-y-reverse-transition">
    <template v-slot:activator>
      <v-btn icon color="teal" large><v-icon>mdi-pencil</v-icon></v-btn>
    </template>
    <v-tooltip z-index="100001" right color="blue">
      <template v-slot:activator="{ on }">
        <v-btn fab small color="blue" dark v-on="on"><v-icon>mdi-format-list-text</v-icon></v-btn>
      </template>
      <span>Список найденных объектов</span>
    </v-tooltip>
    <v-tooltip z-index="100001" right color="green">
      <template v-slot:activator="{ on }">
        <v-btn fab small color="green" dark v-on="on"><v-icon>mdi-plus</v-icon></v-btn>
      </template>
      <span>Добавить новый объект</span>
    </v-tooltip>
    <v-tooltip z-index="100001" right color="red">
      <template v-slot:activator="{ on }">
        <v-btn fab small color="red" dark v-on="on"><v-icon>mdi-magnify</v-icon></v-btn>
      </template>
      <span>Найти объект в системе</span>
    </v-tooltip>
  </v-speed-dial>
</template>

<script>
export default {
  name: "speedDialOfTools"
}
</script>

<style scoped>

</style>