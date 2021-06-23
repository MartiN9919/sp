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

      <LeafletEditor
          :options="edit_options()"
      />

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
import LeafletEditor from '@/components/Map/Leaflet/LeafletEditor';

export default {
  name: "geometryInput",
  components: { LeafletEditor, },
  props: {
    variable: Object,
  },
  data: () => ({
    dialog: false,
  }),
  computed: {
    valueGeometry: {
      get: function() { return this.value },
      set: function(value) { this.$emit('changeValueGeometry', value) },
    },
  },

  methods: {
    acceptGeometry() {
      this.valueGeometry = [1, 2]; // тут объекты fc с карты после нажатия кнопки подтверждения
      this.dialog = false;
    },

    // задавать не обязательно
    edit_options() {
      return {
        mode_enabled: {
          marker:  true,
          line:    true,
          polygon: true,
        },
        mode_selected: 'Polygon',
      }
    },

  },

}
</script>

<style scoped>

</style>