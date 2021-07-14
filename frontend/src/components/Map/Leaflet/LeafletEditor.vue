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
      v-model="fc_child"
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

import { mapGetters } from 'vuex';
import 'leaflet';
import { LMap, LTileLayer, LControlScale, } from 'vue2-leaflet';
import LControlPolylineMeasure from 'vue2-leaflet-polyline-measure';

import Edit       from '@/components/Map/Leaflet/Components/Edit';
import MixKey     from '@/components/Map/Leaflet/Mixins/Key';
import MixMeasure from '@/components/Map/Leaflet/Mixins/Measure';

export default {
  name: 'LeafletEditor',
  model: { prop:  ['fc_parent_prop'], event: 'fc_parent_change', },
  props: {
    fc_parent_prop: {
      type: Object,
      default() { return undefined; },
    },
    options: {
      type: Object,
      default() { return {
        // mode_enabled: {            // доступные для создания элементы
        //   marker:  true,
        //   line:    true,
        //   polygon: true,
        // },
        // mode_selected: 'Polygon',  // включенный по умолчанию режим
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

  computed: {
    ...mapGetters([
      'MAP_GET_TILES',
      'MAP_GET_TILE',
      'MAP_GET_SCALE',
      'MAP_GET_MEASURE',
    ]),

    // проброс fc
    fc_child: {
      get()    { return this.fc_parent_prop; },
      set(val) { this.$emit('fc_parent_change', val); },
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
