<template>
  <EditorSplit
    style="height: 70vh;"
    keySave="script_param"
  >

    <template v-slot:firstPane>
      <EditorNav
        @loadGeometry="load_geometry"
      />
    </template>

    <template v-slot:secondPane>
      <l-map
        ref="map"
        style="z-index: 0;"
        :options="map_options"
        :crs="MAP_GET_TILES[MAP_GET_TILE].crs"
        @ready="on_map_ready"
        @resize="on_map_resize"
        @contextmenu=""
        @dblclick="on_map_dblclick"
      >

        <!-- ПОДЛОЖКА -->
        <l-tile-layer
          :url="MAP_GET_TILES[MAP_GET_TILE].url"
          :attribution="MAP_GET_TILES[MAP_GET_TILE].attr"
          :tms="MAP_GET_TILES[MAP_GET_TILE].tms"
        />

        <!-- РЕДАКТОР -->
        <EditorMap
          v-model="fc_child"
          :modeEnabled="modeEnabled"
          :modeSelected="modeSelected"
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

  </EditorSplit>
</template>



<script>

import { mapGetters, mapActions, } from 'vuex';
import 'leaflet';
import { LMap, LTileLayer, LControlScale, } from 'vue2-leaflet';
import LControlPolylineMeasure from 'vue2-leaflet-polyline-measure';

import EditorSplit  from '@/components/Map/Leaflet/Components/EditorSplit';
import EditorNav    from '@/components/Map/Leaflet/Components/EditorNav';
import EditorMap    from '@/components/Map/Leaflet/Components/EditorMap';
import MixKey       from '@/components/Map/Leaflet/Mixins/Key';
import MixMeasure   from '@/components/Map/Leaflet/Mixins/Measure';

export default {
  name: 'LeafletEditor',
  model: { prop:  ['fc_parent_prop'], event: 'fc_parent_change', },
  props: {
    fc_parent_prop: {
      type: Object,
      default() { return undefined; },
    },
    modeEnabled: Object,      // доступные для создания элементы, например: { marker: true, line: true, polygon: true }
    modeSelected: String,     // включенный по умолчанию режим, например: 'Polygon'
  },


  mixins: [ MixKey, MixMeasure, ],

  components: { LMap, LTileLayer, LControlScale, LControlPolylineMeasure, EditorMap, EditorNav, EditorSplit, },

  data: () => ({
    fc_child: undefined,
    map_options: {
      zoomControl: false,
      zoomSnap: 0.5,
    },
  }),

  created() {
    this.fc_child = this.fc_parent;
  },

  watch: {
    fc_child: function(val) { this.fc_parent = val; },
  },

  computed: {
    ...mapGetters([
      'MAP_GET_TILES',
      'MAP_GET_TILE',
      'MAP_GET_SCALE',
      'MAP_GET_MEASURE',
    ]),

    fc_parent: {
      get()    { return this.fc_parent_prop; },
      set(val) { this.$emit('fc_parent_change', val); },
    },
  },

  methods: {
    ...mapActions([
      'appendErrorAlert',
    ]),

    on_map_ready() {
      this.map = this.$refs.map.mapObject;
      this.map.doubleClickZoom.disable();
      this.map.invalidateSize();
      this.key_mounted_after();
    },

    on_map_resize() {
      this.map.invalidateSize();
    },

    on_map_dblclick(e) {
      // this.appendErrorAlert({status: 501, content: e.latlng, show_time: 5, });
    },

    load_geometry(fc) {
      this.fc_child  = JSON.parse(JSON.stringify(fc))
      this.fc_parent = this.fc_child
    },

  },

}
</script>



<style scoped lang="scss">
  @import "~leaflet/dist/leaflet.css";
  @import "~@/components/Map/Leaflet/Lib/Lib.css";
</style>
