<template>
  <div class="geometry-input-form">
    <v-dialog
        width="60%"
        height="80%"
        v-model="dialog"
        @input="show_dialog"
        @keydown.esc="dialog = false"
        persistent
        style="z-index: 10000001"
        transition="dialog-bottom-transition"
    >
      <template
          v-slot:activator="{ on, attrs }"
      >
        <div v-on="on">
          <body-input-form
              :input-string="show_text()"
              :rules="rules"
              :clearable="clearable"
              :hide-details="hideDetails"
              :class="bodyInputClasses"
              :placeholder="placeholder"
              readonly
          >
            <template v-slot:label>
              {{title}}
            </template>
            <template v-slot:append="props" class="action-icon">
              <v-icon
                v-if="deletable && props.hover"
                @click.stop="$emit('deletable')"
                size="24"
              >mdi-delete</v-icon>
              <v-icon v-else size="24">mdi-map-marker-outline</v-icon>
            </template>
            <template v-slot:message>
              <slot name="message"></slot>
            </template>
          </body-input-form>
        </div>
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
          <v-btn :color="$CONST.APP.COLOR_OBJ" text @click="click_cancel">Отмена</v-btn>
          <v-btn :color="$CONST.APP.COLOR_OBJ" text @click="click_ok">Ок</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import LeafletEditor from '@/components/Map/Leaflet/LeafletEditor'
import BodyInputForm from "../UI/bodyInputForm"

export default {
  name: "geometryInput",
  components: {BodyInputForm, LeafletEditor, },
  model: { prop: 'inputString', event: 'changeInputString', },
  props: {
    inputString:  Object,
    modeEnabled:  { type: Object, default: () => ({ marker: true , line: true, polygon: true, }) }, // доступные элементы
    modeSelected: { type: String, default: () => undefined},                        // режим ввода по умолчанию

    rules: {
      type: Array,
      default: function () {
        return []
      }
    },
    deletable: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: '',
    },
    hideDetails: {
      type: Boolean,
      default: false,
    },
    placeholder: {
      type: String,
      default: 'Выберете объект на карте',
    },
    clearable: {
      type: Boolean,
      default: false,
    }
  },
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
    bodyInputClasses: function () { return this.title.length ? '' : 'pt-0' },
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

<style scoped>
.geometry-input-form >>> input {
  cursor: pointer;
}
.geometry-input-form >>> .v-input__slot {
  cursor: pointer;
}
.action-icon {
  cursor: pointer;
}
.geometry-input-form {
  width: 100%;
}
</style>