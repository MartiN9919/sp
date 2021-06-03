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

      <!-- ЗАГОЛОВОК -->
      <v-card-title class="headline">Объект на карте</v-card-title>

      <!-- КАРТА -->
      <template>
        <l-map
          ref="map"
          style="height: 70vh; z-index: 0;"
          :options="mapOptions"
          :crs="MAP_GET_TILES[MAP_GET_TILE].crs"
          @ready="onMapReady"
          @contextmenu=""
          @click="onClick"
        >

          <!-- ПОДЛОЖКА -->
          <l-tile-layer
            :url="MAP_GET_TILES[MAP_GET_TILE].url"
            :attribution="MAP_GET_TILES[MAP_GET_TILE].attr"
            :tms="MAP_GET_TILES[MAP_GET_TILE].tms"
          />

          <!-- РЕДАКТОР -->
          <Edit/>

          <!-- МАСШТАБ -->
          <l-control-scale
            v-if="MAP_GET_SCALE"
            position="bottomright"
            :imperial="false"
            :metric="true"
          />

          <!-- ЛИНЕЙКА -->
          <l-control-polyline-measure
            v-if="MAP_GET_MEASURE"
            :options="measure_options()"
          />

        </l-map>
      </template>

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
import { mapGetters } from 'vuex';
import 'leaflet';
import { LMap, LTileLayer, LControlScale, } from 'vue2-leaflet';
import LControlPolylineMeasure from 'vue2-leaflet-polyline-measure';

import Edit from '@/components/Map/Leaflet/Edit';
import MixKey from '@/components/Map/Leaflet/L.Mix.Key';
import MixMeasure from '@/components/Map/Leaflet/L.Mix.Measure';


export default {
  name: 'geometry-input-dialog',

  props: { value: Array, },

  mixins: [ MixKey, MixMeasure, ],

  components: { LMap, LTileLayer, LControlScale, LControlPolylineMeasure, Edit, },

  data: () => ({
    dialog: false,

    mapOptions: {
      zoomControl: false,
      zoomSnap: 0.5,
    },
  }),

  mounted: function() {
  },

  computed: {
    ...mapGetters([
      'MAP_GET_TILES',
      'MAP_GET_TILE',
      'MAP_GET_SCALE',
      'MAP_GET_MEASURE',

      'SCRIPT_GET',
      'SCRIPT_GET_ITEM_COLOR',
      'SCRIPT_GET_ITEM_MARKER',
      'SCRIPT_GET_ITEM_LINE',
      'SCRIPT_GET_ITEM_POLYGON',
      'SCRIPT_GET_ITEM_ICON',
    ]),

    valueGeometry: {
      get: function() { return this.value },
      set: function(value) { this.$emit('changeValueGeometry', value) },
    },
  },
  methods: {
    acceptGeometry() {
      this.valueGeometry = [1, 2] // тут объекты fc с карты после нажатия кнопки подтверждения
      this.dialog = false
    },

    onMapReady() {
      this.map = this.$refs.map.mapObject;
      this.map.invalidateSize();
      this.key_mounted_after();
    },

    onClick(event) {
      console.log(event.latlng);
    },

  },

}
</script>

<style scoped lang="scss">
  @import "~leaflet/dist/leaflet.css";
  @import "~@/components/Map/Leaflet/L.css";
</style>