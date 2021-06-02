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


    <v-card>

      <!-- ЗАГОЛОВОК -->
      <v-card-title class="headline">Отметки на карте</v-card-title>

      <!-- КАРТА -->
      <template>
        <l-map
          ref="map_edit"
          style="height: 70vh; z-index: 0;"
          :options="mapOptions"
          :crs="MAP_GET_TILES[MAP_GET_TILE].crs"
          @ready="onMapReady"
        >

          <!--
          @click="onClick"
          @contextmenu="menu_show"
          -->

          <!-- ПОДЛОЖКА -->
          <l-tile-layer
            :url="MAP_GET_TILES[MAP_GET_TILE].url"
            :attribution="MAP_GET_TILES[MAP_GET_TILE].attr"
            :tms="MAP_GET_TILES[MAP_GET_TILE].tms"
          />


          <!-- РЕДАКТОР -->
          <!--
          <Edit/>
          -->

          <!-- МАСШТАБ -->
          <!--
          <l-control-scale
            v-if="MAP_GET_SCALE"
            position="bottomright"
            :imperial="false"
            :metric="true"
          />
          -->


          <!-- ТЕСТ -->
          <!--
          <l-control
            v-if="true"
            position="topleft"
          >
            <v-btn class="button-container leaflet-buttons-control-button" @click="editor_on">Test 1</v-btn>
            <v-btn class="button-container leaflet-buttons-control-button" @click="onTest2">Test 2</v-btn>
          </l-control>
          -->

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
import {
  LMap,
  LTileLayer,
  // LFeatureGroup,
  // LLayerGroup,
  // LGeoJson,
  // LMarker,
  // LPolyline,
  // LPolygon,
  // LIcon,
} from 'vue2-leaflet';

export default {
  name: 'geometry-input-dialog',

  props: { value: Array, },

  components: { LMap, LTileLayer, },

  data: () => ({
    dialog: false,

    mapOptions: {
      zoomControl: false,
      zoomSnap: 0.5,
      //crs: this.ttt(),
    },
  }),

  computed: {
    ...mapGetters([
      'MAP_GET_TILES',
      'MAP_GET_TILE',
      'MAP_GET_SCALE',

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
      this.valueGeometry = [1, 2] // тут объекты future collection с карты после нажатия кнопки подтверждения
      this.dialog = false
    },

    // ===============
    // СОБЫТИЯ
    // ===============
    onMapReady() {
      console.log(11)
      this.map = this.$refs.map_edit.mapObject;
      //this.onEditReady();
    },

  },

}
</script>

<style scoped lang="scss">
  @import "~leaflet/dist/leaflet.css";
  @import "~@/components/Map/Leaflet/L.css";
</style>