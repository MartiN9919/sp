<template>
  <ResSplitPane
    split-to="columns"
    :allow-resize="true"
    :min-size="15"
    :max-size="85"
    :size="sizeMenuColumn"
    :resizerBorderThickness="1"
    :resizerThickness="1"
    v-on:update:size="sizeMenuColumn = $event"
    units="percents"
    style="position: static"
  >
    <v-col slot="firstPane" class="column-settings pa-0">
      <MapGeometry/>
    </v-col>

    <v-col slot="secondPane" class="column-settings overflow-hidden pa-0">
      <l-map
        ref="map"
        style="height: 70vh; z-index: 0;"
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
        <MapEdit
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
    </v-col>
  </ResSplitPane>
</template>



<script>

import { mapGetters, mapActions, } from 'vuex';
import 'leaflet';
import { LMap, LTileLayer, LControlScale, } from 'vue2-leaflet';
import LControlPolylineMeasure from 'vue2-leaflet-polyline-measure';
import ResSplitPane from 'vue-resize-split-pane'

import MapEdit      from '@/components/Map/Leaflet/Components/MapEdit';
import MapGeometry  from '@/components/Map/Leaflet/Components/MapGeometry';
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

  components: { LMap, LTileLayer, LControlScale, LControlPolylineMeasure, ResSplitPane, MapEdit, MapGeometry, },

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

    on_map_dblclick(event) {
      // this.appendErrorAlert({status: 501, content: event.latlng, show_time: 5, });
    },

  },

}
</script>



<style scoped lang="scss">
  @import "~leaflet/dist/leaflet.css";
  @import "~@/components/Map/Leaflet/Lib/Lib.css";
</style>
