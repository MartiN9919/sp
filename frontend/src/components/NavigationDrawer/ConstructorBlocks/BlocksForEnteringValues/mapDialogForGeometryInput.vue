<template>
  <v-dialog v-model="dialog" persistent>
    <template v-slot:activator="{ on, attrs }">
      <v-icon
          v-bind="attrs" v-on="on"
          :color="attrs['aria-expanded'] === 'true' ? 'teal' : ''"
      >mdi-map-marker-outline</v-icon>
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
  name: "mapDialogForGeometryInput",
  props: { value: Array, },
  data: () => ({ dialog: false, }),
  computed: {
    valueGeometry: {
      get: function() { return this.value },
      set: function(value) { this.$emit('changeValueGeometry', value) },
    },
  },
  methods: {
    acceptGeometry() {
      this.valueGeometry = [1, 2] // тут объекты future collection с карты после нажатия кнопки подтверждения
      this.dialog = false
    },
  },
}
</script>

<style scoped>

</style>