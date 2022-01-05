<template>
  <l-map
    ref="map"
    style="height: 100%; width: 100%; z-index: 0;"
    :options="map_options"
    :crs="MAP_GET_TILE_VAL.crs"
    @ready="on_map_ready"
    @contextmenu=""
    @dblclick="on_map_dblclick"
  >

    <!-- ПОДЛОЖКА -->
    <l-tile-layer
      :url="MAP_GET_TILE_VAL.url"
      :attribution="MAP_GET_TILE_VAL.attr"
      :tms="MAP_GET_TILE_VAL.tms"
    />

    <!-- ФИГУРЫ -->
    <l-geo-json
      :geojson="data_normalize(fc)"
      :options="geojson_options()"
    />

    <!-- МАСШТАБ -->
    <l-control-scale
      v-if="controls"
      position="bottomright"
      :imperial="false"
      :metric="true"
    />

    <!-- ЛИНЕЙКА -->
    <l-control-polyline-measure
      v-if="controls"
      :options="measure_options()"
    />

  </l-map>
</template>



<script>

import { mapGetters, mapActions, } from 'vuex';
import 'leaflet';
import { LMap, LTileLayer, LGeoJson, LControlScale, } from 'vue2-leaflet';
import LControlPolylineMeasure from 'vue2-leaflet-polyline-measure';

import MixResize    from '@/components/Map/Leaflet/Mixins/Resize';
import MixMeasure   from '@/components/Map/Leaflet/Mixins/Measure';
import {marker_get}   from '@/components/Map/Leaflet/Components/Style/StyleIcon';

export default {
  name: 'LeafletViewer',
  props: {
    fc:       { type: Object,  default: () => undefined, },
    controls: { type: Boolean, default: () => true, },       // дополнительные элементы (рулетка, масштаб)
  },

  components: { LMap, LTileLayer, LGeoJson, LControlScale, LControlPolylineMeasure, },
  mixins: [ MixMeasure, MixResize, ],

  data: () => ({
    map_options: {
      zoomControl: false,
      zoomSnap: 0.5,
    },
  }),

  mounted() {
    // установить слушатель map.on_resize
    this.resize_add(this.$refs.map.$el, this.on_map_resize);
  },

  computed: {
    ...mapGetters([
      'MAP_GET_TILE_VAL',
    ]),
  },

  methods: {
    ...mapActions([
      'addNotification',
    ]),

    on_map_ready() {
      this.map = this.$refs.map.mapObject;
      this.map.doubleClickZoom.disable();
      this.map.invalidateSize();

      let self = this;
      let fc   = JSON.parse(JSON.stringify(this.fc));
      let layer = L.geoJson(fc);
      setTimeout(function(){  // this.$nextTick не успевает
        self.map.fitBounds(layer.getBounds(), { padding: [30, 30], });
      }, 100);
    },

    on_map_resize () {                   // fire from MixResize
      if (this.map) this.map.invalidateSize();
    },

    on_map_dblclick(e) {
      // this.addNotification({content: e.latlng});
    },

    data_normalize(fc) {
      return JSON.parse(JSON.stringify(fc));
    },

    geojson_options() {
      return {
        // // для каждого маркера / фигуры
        // onEachFeature: function(feature, layer) {
        //   layer.setStyle({'className': '', });
        // }.bind(this),


        // стиль маркеров
        pointToLayer: function(feature, latlng) {
          return marker_get(latlng, 'red', '');
        },


        // стиль фигур
        style: function(feature) {
          return {
            weight:      2,
            opacity:     .5,
            color:       '#f00',
            fillOpacity: .3,
            fillColor:   '#a00',
            fillRule:    'evenodd',
            className:   '',
          };
        },
      };
    },

  },

}
</script>



<style scoped lang="scss">
  @import "~leaflet/dist/leaflet.css";
  @import "~@/components/Map/Leaflet/Lib/Lib.css";
  @import "~@/components/Map/Leaflet/Mixins/Control.css";
</style>
