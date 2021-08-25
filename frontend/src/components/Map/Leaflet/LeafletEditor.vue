<template>
  <EditorSplit
    style="height: 70vh;"
    localStorageKey="script_param"
  >

    <template v-slot:firstPane>
      <EditorNav
        localStorageKey="script_param"
        @selectedFc="on_nav_selected_fc"
      />
    </template>

    <template v-slot:secondPane>
      <l-map
        ref="map"
        style="z-index: 0;"
        :options="map_options"
        :crs="MAP_GET_TILES[MAP_GET_TILE].crs"
        @ready="on_map_ready"
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
          @resetSelect="on_map_reset_select"
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

        <!-- ЗАМЕТКИ -->
        <Notify ref="notify"/>

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
import Notify       from '@/components/Map/Leaflet/Components/Notify';
import MixKey       from '@/components/Map/Leaflet/Mixins/Key';
import MixMeasure   from '@/components/Map/Leaflet/Mixins/Measure';
import MixResize    from '@/components/Map/Leaflet/Mixins/Resize';
import MixControl   from '@/components/Map/Leaflet/Mixins/Control';


import { fc_merge } from '@/components/Map/Leaflet/Lib/Lib';

export default {
  name: 'LeafletEditor',
  model: { prop:  ['fc_parent_prop'], event: 'fc_parent_change', },
  props: {
    fc_parent_prop: { type: Object, default: () => undefined, },
    modeEnabled: Object,      // доступные для создания элементы, например: { marker: true, line: true, polygon: true }
    modeSelected: String,     // включенный по умолчанию режим, например: 'Polygon'
  },

  components: { LMap, LTileLayer, LControlScale, LControlPolylineMeasure, EditorMap, EditorNav, EditorSplit, Notify, },
  mixins: [ MixKey, MixMeasure, MixResize, MixControl, ],

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

  mounted() {
    // установить слушатель map.on_resize
    this.resize_add(this.$refs.map.$el, this.on_map_resize);
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

    on_map_resize () {                   // fire from MixResize
      if (this.map) this.map.invalidateSize();
    },

    on_map_dblclick(e) {
      // this.appendErrorAlert({status: 501, content: e.latlng, show_time: 5, });
    },

    // сбросить выделение (obj, osm): из child.map в свойство child.nav
    on_map_reset_select() {
      this.$refs.notify.notify_del();
    },

    // обновить на карте fc
    on_nav_selected_fc(fc, name) {
      console.log(11);
      this.fc_child  = JSON.parse(JSON.stringify(fc));
      this.fc_parent = this.fc_child;
      let dd = fc_merge([this.fc_child,]);
      this.$refs.notify.notify_set(name);
    },

  },

}
</script>



<style scoped lang="scss">
  @import "~leaflet/dist/leaflet.css";
  @import "~@/components/Map/Leaflet/Lib/Lib.css";
</style>
