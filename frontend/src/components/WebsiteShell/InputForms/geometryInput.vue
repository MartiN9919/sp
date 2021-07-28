<template>
  <v-dialog
    v-model="dialog"
    width="60%"
    height="80%"
    @input="show_dialog"
    @keydown.esc="dialog = false"
    persistent
  >
    <template
      v-slot:activator="{ on, attrs }"
    >
      <v-textarea
        v-on="on"
        class="pt-0 mt-0 geometry-input-cursor"
        type="text"
        append-icon="mdi-map-marker-outline"
        autocomplete="off"
        row-height="1" auto-grow
        color="teal"
        placeholder="Выберете объект на карте"
        hide-details
        readonly
        :label="title"
        :rules="rules"
        :value="show_text()"
      ></v-textarea>
    </template>

    <v-card>
      <v-card-title class="text-h7">{{ title }}</v-card-title>
      <v-divider></v-divider>
      <LeafletEditor
        v-if="dialog"
        v-model="fc"
        :modeEnabled="modeEnabled"
        :modeSelected="modeSelected"
      />
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="teal" text @click="click_cancel">Отмена</v-btn>
        <v-btn color="teal" text @click="click_ok">Ок</v-btn>
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
    rules: Array,
    title: String,
    inputString: Object,
    modeEnabled: Object,      // доступные для создания элементы, например: { marker: true, line: true, polygon: true }
    modeSelected: String,     // включенный по умолчанию режим, например: 'Polygon'
  },
  model: { prop: 'inputString', event: 'changeInputString', },
  data: () => ({
    dialog: false,
    fc_temp: undefined,       // не принятые изменения fc
  }),
  computed: {
    value: {
      get()    { return this.inputString; },
      set(val) { this.$emit('changeInputString', val); }
    },
    fc: {
      get()    { return this.value; },
      set(val) { this.fc_temp = val; },
    },
  },

  methods: {
    show_dialog (e) {
       if (this.value == undefined) this.value = { "type": "FeatureCollection", "features": [], }
       this.fc = JSON.parse(JSON.stringify(this.value));
    },

    click_ok() {
      this.dialog = false;
      this.value  = JSON.parse(JSON.stringify(this.fc_temp));
    },

    click_cancel() {
      this.dialog = false;
    },

    show_text() {
      if (this.value == undefined) return ''
      if (this.value.features.length == 0) return ''
      return '[объект]'
    },

  },

}

// ТЕСТОВЫЕ ДАННЫЕ
// { "type": "FeatureCollection", "features": [], },
// L.featureGroup().toGeoJSON(),
// this.value = {
//   "type": "FeatureCollection",
//   "features": [
//     {
//       "type": "Feature",
//       "properties": {
//         "hint": "Edit 1",
//       },
//       "geometry": {
//         "type": "Polygon",
//         "coordinates": [
//           [
//             [30.212402343750004,55.19141243527065],
//             [30.443115234375004,54.50832650029076],
//             [31.014404296875004,54.718275018302315],
//             [30.212402343750004,55.19141243527065],
//           ]
//         ]
//       }
//     },
//     {
//       "type": "Feature",
//       "properties": {
//         "hint": "Edit 2",
//       },
//       "geometry": {
//         "type":        "Point",
//         "coordinates": [24.071044921875004,55.86914706303444]
//       },
//     },
//   ],
// },

</script>

<style>
  .geometry-input-cursor * { cursor: pointer!important; }
</style>