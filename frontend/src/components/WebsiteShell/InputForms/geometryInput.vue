<template>
  <v-dialog
    v-model="dialog"
    @input="show_dialog"
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
      <v-card-title class="text-h5">{{ title }}</v-card-title>
      <LeafletEditor
        v-if="dialog"
        v-model="edit_fc"
        :options="edit_options()"
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
  },
  model: { prop: 'inputString', event: 'changeInputString', },
  data: () => ({
    dd: "ddda",
    dialog: false,
    fc_temp: undefined,    // не принятые изменения edit_fc
  }),
  computed: {
    value: {
      get()    { return this.inputString; },
      set(val) { this.$emit('changeInputString', val); }
    },
    edit_fc: {
      get()    { return this.value; },
      set(val) { this.fc_temp = val; },
    },
  },

  methods: {
    show_dialog (e) {
       if (this.value == undefined) this.value = { "type": "FeatureCollection", "features": [], }
       this.edit_fc = JSON.parse(JSON.stringify(this.value));
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

    // задавать не обязательно
    edit_options() {
      return {
        mode_enabled: {             // доступные для создания элементы
          marker:  true,
          line:    true,
          polygon: true,
        },
        // mode_selected: 'Polygon',   // включенный по умолчанию режим
      }
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