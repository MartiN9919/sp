<template>
  <v-dialog v-model="dialog" persistent>
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="teal" v-bind="attrs" v-on="on" plain
        class="pb-2 text-decoration-underline"
      >Выбрать объект на карте</v-btn>
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
  name: "mapDialog",
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
      this.valueGeometry = [] // тут объекты future collection с карты после нажатия кнопки подтверждения
      this.dialog = false
    },
  },
}
</script>

<style scoped>

</style>