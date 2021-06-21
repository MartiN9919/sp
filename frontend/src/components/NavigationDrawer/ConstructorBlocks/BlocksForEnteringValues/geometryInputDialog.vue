<template>
  <v-dialog
    v-model="dialog"
    persistent
  >
    <template v-slot:activator="{ on, attrs }">
      <v-icon
        v-bind="attrs" v-on="on"
        :color="attrs['aria-expanded'] === 'true' ? 'teal' : ''"
      >mdi-map-marker-outline</v-icon>
    </template>
    <v-card
      class="select_off"
    >
      <v-card-title class="headline">Объект на карте</v-card-title>
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
  name: 'geometry-input-dialog',
  props: { value: Array, },
  components: { LeafletEditor, },
  data: () => ({
    dialog: false,
    // fc_edit: L.featureGroup().toGeoJSON(),    // { "type": "FeatureCollection", "features": [], }, //L.featureGroup().toGeoJSON(),
    // // {
    // //   "type": "FeatureCollection",
    // //   "features": [
    // //     {
    // //       "type": "Feature",
    // //       "properties": {
    // //         "hint": "Edit 1",
    // //       },
    // //       "geometry": {
    // //         "type": "Polygon",
    // //         "coordinates": [
    // //           [
    // //             [30.212402343750004,55.19141243527065],
    // //             [30.443115234375004,54.50832650029076],
    // //             [31.014404296875004,54.718275018302315],
    // //             [30.212402343750004,55.19141243527065],
    // //           ]
    // //         ]
    // //       }
    // //     },
    // //     {
    // //       "type": "Feature",
    // //       "properties": {
    // //         "hint": "Edit 2",
    // //       },
    // //       "geometry": {
    // //         "type":        "Point",
    // //         "coordinates": [24.071044921875004,55.86914706303444]
    // //       },
    // //     },
    // //   ],
    // // },

    // map_options: {
    //   zoomControl: false,
    //   zoomSnap: 0.5,
    // },
  }),



  // watch: {
  //   fc_edit: {
  //     handler() {
  //       console.log('watch changed fc_edit 2', this.fc_edit);
  //     },
  //     deep: true,
  //   },
  // },

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

<style scoped lang="scss">
</style>