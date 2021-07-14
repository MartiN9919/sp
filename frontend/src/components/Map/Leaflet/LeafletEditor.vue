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
      v-model="fc"
      :options="options"
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



<script>

import { mapGetters, mapActions } from 'vuex';
import 'leaflet';
import { LMap, LTileLayer, LControlScale, } from 'vue2-leaflet';
import LControlPolylineMeasure from 'vue2-leaflet-polyline-measure';

import Edit       from '@/components/Map/Leaflet/Components/Edit';
import MixKey     from '@/components/Map/Leaflet/Mixins/Key';
import MixMeasure from '@/components/Map/Leaflet/Mixins/Measure';

export default {
  name: 'LeafletEditor',

  props:      {
    // fc_prop: {
    //   type: Object,
    //   default() { return undefined; },
    // },
    options: {
      type: Object,
      default() { return {
        // mode_enabled: {
        //   marker:  true,
        //   line:    true,
        //   polygon: true,
        // },
        // mode_selected: 'Polygon',
      };
    },
    },
  },


  mixins: [ MixKey, MixMeasure, ],

  components: { LMap, LTileLayer, LControlScale, LControlPolylineMeasure, Edit, },

  data() {
    return {
      map_options: {
        zoomControl: false,
        zoomSnap: 0.5,
      },
    }
  },

  watch: {
    // fc: {
    //   handler() {
    //     console.log('watch changed fc 2', this.fc);
    //   },
    //   deep: true,
    // },

    fc: function(val) {
      console.log('update 2', this.fc, val);
    },
  },

  mounted() {
    console.log('mounted')
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

    // FeatureCollection РЕДАКТИРУЕМЫХ объектов
    fc: {
      get()    {     // { "type": "FeatureCollection", "features": [], }, //L.featureGroup().toGeoJSON(),
        console.log('get')
        return {
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
      }
      },
      set(val) { console.log('set', val) },
    },

  },

  methods: {
    on_map_ready() {
      this.map = this.$refs.map.mapObject;
      this.map.invalidateSize();
      this.key_mounted_after();
    },

    on_map_click(event) {
      // console.log(event.latlng);
    },

  },

}
</script>



<style scoped lang="scss">
  @import "~leaflet/dist/leaflet.css";
  @import "~@/components/Map/Leaflet/Lib/Lib.css";
</style>
