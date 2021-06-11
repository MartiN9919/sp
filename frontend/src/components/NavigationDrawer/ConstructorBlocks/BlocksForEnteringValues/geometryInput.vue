<template>
  <v-dialog v-model="dialog" persistent>
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        autocomplete="off"
        append-icon="mdi-map-marker-outline"
        :label="variable.title"
        v-model="variable.value"
        placeholder="Выберете объект на карте"
        hide-details color="teal" readonly class="pt-0 mt-0" type="text"
        v-on="on"
      ></v-text-field>
    </template>
    <v-card>

      <!--   Тут ставится карта   -->

      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="teal" text @click="dialog = false">Отменить</v-btn>
        <v-btn color="teal" text @click="acceptGeometry">Подтвердить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "geometryInput",
  data: () => ({
    dialog: false,
  }),
  props: {
    variable: Object,
  },
  methods: {
    acceptGeometry() {
      this.variable.value = [1, 2] // тут объекты future collection с карты после нажатия кнопки подтверждения
      this.dialog = false
    },
  },

}
</script>

<style scoped>

</style>