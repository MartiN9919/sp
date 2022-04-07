<template>
  <div class="geometry-input-form">
    <v-dialog
        width="60%"
        height="80%"
        v-model="dialog"
        @keydown.esc="dialog = false"
        @deletable="$emit('deletable')"
        persistent
        style="z-index: 10000001"
        transition="dialog-bottom-transition"
    >
      <template v-slot:activator="{ on, attrs }">
        <div v-on="on">
          <body-input-form
            v-bind="$attrs"
            :input-string="show_text()"
            @changeInputString="$emit('changeInputString', $event)"
            @deletable="$emit('deletable')"
            :class="bodyInputClasses"
            :icon="icon"
            :placeholder="$attrs.placeholder || 'Выберете объект на карте'"
            readonly
          >
            <template v-slot:message>
              <slot name="message"></slot>
            </template>
          </body-input-form>
        </div>
      </template>

      <v-card>
        <v-card-title class="text-h7">{{ $attrs.label }}</v-card-title>
        <v-divider></v-divider>
        <LeafletEditor
          v-if="dialog"
          style="height: 70vh;"
          v-model="featureCollection"
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
import BodyInputForm from "@/components/WebsiteShell/CustomComponents/bodyInputForm"

export default {
  name: "geometryInput",
  components: {BodyInputForm, LeafletEditor, },
  model: { prop: 'inputString', event: 'changeInputString', },
  props: {
    inputString:  Object,
  },
  data: () => ({
    dialog: false,
    copyInputString: null,
    modeEnabled: null, // { marker: true , line: true, polygon: true, }, доступные элементы
    modeSelected: null,
    icon: ''
  }),
  mounted() {
    this.icon = this.isPoint ? 'mdi-map-marker-outline' : 'mdi-map-outline'
    this.modeEnabled = this.isPoint ? {marker: true} : {line: true, polygon: true}
  },
  computed: {
    bodyInputClasses: function () { return this.$attrs.hasOwnProperty('label') ? '' : 'pt-0' },
    isPoint: function () { return this.$attrs['type-load'] === 'point' },
    featureCollection: {
      get: function () {
        if(this.inputString){
          if(this.inputString.type === 'FeatureCollection')
            return this.inputString
          else
            return { "type": "FeatureCollection", "features": [{'type': 'Feature', 'geometry': this.inputString, 'properties': {}}], }
        }
        else return { "type": "FeatureCollection", "features": []}
      },
      set: function (value) { this.copyInputString = value }
    }
  },
  methods: {
    click_ok() {
      this.$emit('changeInputString', this.copyInputString)
      this.copyInputString = null
      this.dialog = false;
    },
    click_cancel() {
      this.copyInputString = null
      this.dialog = false;
    },
    show_text() {
      if (!this.featureCollection || this.featureCollection.features.length === 0) return ''
      return this.isPoint ? 'Точка' : 'Геометрия'
    },
  },
}

</script>

<style scoped>
.geometry-input-form >>> input {
  cursor: pointer;
}
.geometry-input-form >>> .v-input__slot {
  cursor: pointer;
}
.geometry-input-form {
  width: 100%;
}
</style>