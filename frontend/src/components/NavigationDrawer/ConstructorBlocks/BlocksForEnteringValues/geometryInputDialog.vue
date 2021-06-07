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
          :options="map_options"
          :crs="MAP_GET_TILES[MAP_GET_TILE].crs"
          @ready="on_map_ready"
          @contextmenu=""
          @click="on_map_click"
        >

          <!-- ПОДЛОЖКА -->
          <l-tile-layer
            :url="MAP_GET_TILES[MAP_GET_TILE].url"
            :attribution="MAP_GET_TILES[MAP_GET_TILE].attr"
            :tms="MAP_GET_TILES[MAP_GET_TILE].tms"
          />

          <!-- РЕДАКТОР -->
          <Edit
            v-model="fc_edit"
            :options="edit_options()"
          />

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
import { mapGetters, mapActions } from 'vuex';
import 'leaflet';
import { LMap, LTileLayer, LControlScale, } from 'vue2-leaflet';
import LControlPolylineMeasure from 'vue2-leaflet-polyline-measure';

import Edit from '@/components/Map/Leaflet/Edit';
import MixKey from '@/components/Map/Leaflet/L.Mix.Key';
import MixMeasure from '@/components/Map/Leaflet/L.Mix.Measure';

import {
  MAP_TEST_EDIT_1,
  MAP_TEST_EDIT_2,
  MAP_TEST_EDIT_3,
  MAP_TEST_EDIT_4,
  MAP_TEST_EDIT_5,
} from '@/components/Map/Leaflet/Menu.test';


export default {
  name: 'geometry-input-dialog',

  props: { value: Array, },

  mixins: [ MixKey, MixMeasure, ],

  components: { LMap, LTileLayer, LControlScale, LControlPolylineMeasure, Edit, },

  data: () => ({
    dialog: false,
    fc_edit:     // { "type": "FeatureCollection", "features": [], }, //L.featureGroup().toGeoJSON(),
    {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {
            "hint": "Edit 1",
          },
          "geometry": {
            "type": "Polygon",
            "coordinates": [
              [
                [30.212402343750004,55.19141243527065],
                [30.443115234375004,54.50832650029076],
                [31.014404296875004,54.718275018302315],
                [30.212402343750004,55.19141243527065],
              ]
            ]
          }
        },
        {
          "type": "Feature",
          "properties": {
            "hint": "Edit 2",
          },
          "geometry": {
            "type":        "Point",
            "coordinates": [24.071044921875004,55.86914706303444]
          },
        },
      ],
    },

    map_options: {
      zoomControl: false,
      zoomSnap: 0.5,
    },
  }),



  watch: {
    fc_edit: {
      handler() {
        console.log('watch changed fc_edit 2', this.fc_edit);
      },
      deep: true,
    },
  },

  mounted: function() {
    this.MAP_ACT_EDIT_ON(MAP_TEST_EDIT_1);
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
    ...mapActions([
      'MAP_ACT_EDIT_ON',
      'MAP_ACT_EDIT_OFF',
    ]),

    edit_options() {
      return {
        mode_enabled: {
          marker:  true,
          polygon: true,
        },
        mode_selected: 'Polygon',
      }
    },

    acceptGeometry() {
      this.valueGeometry = [1, 2]; // тут объекты fc с карты после нажатия кнопки подтверждения
      this.dialog = false;
    },

    on_map_ready() {
      this.map = this.$refs.map.mapObject;
      this.map.invalidateSize();
      this.key_mounted_after();
    },

    on_map_click(event) {
      console.log(event.latlng);
    },

  },

}
</script>

<style scoped lang="scss">
  @import "~leaflet/dist/leaflet.css";
  @import "~@/components/Map/Leaflet/L.css";
</style>