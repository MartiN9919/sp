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

    <!-- РЕДАКТОР -->
    <EditorMap
      v-model="fc_child"
      :modeEnabled="{}"
      modeSelected=""
      :modeEdit="false"
      @resetSelect="on_map_reset_select"
      @setFocus="on_map_set_focus"
    />

    <!-- МАСШТАБ -->
    <l-control-scale
      v-if="dop_controls"
      position="bottomright"
      :imperial="false"
      :metric="true"
    />

    <!-- ЛИНЕЙКА -->
    <l-control-polyline-measure
      v-if="dop_controls"
      :options="measure_options()"
    />

  </l-map>
</template>



<script>

import { mapGetters, mapActions, } from 'vuex';
import 'leaflet';
import { LMap, LTileLayer, LControlScale, } from 'vue2-leaflet';
import LControlPolylineMeasure from 'vue2-leaflet-polyline-measure';

import EditorMap    from '@/components/Map/Leaflet/Components/Editor/EditorMap';
import MixResize    from '@/components/Map/Leaflet/Mixins/Resize';
import MixMeasure   from '@/components/Map/Leaflet/Mixins/Measure';

import { fc_merge } from '@/components/Map/Leaflet/Lib/LibFc';

export default {
  name: 'LeafletViewer',
  model: { prop:  ['fc_parent_prop'], event: 'fc_parent_change', },
  props: {
    fc_parent_prop: { type: Object,  default: () => undefined, },
    dop_controls:   { type: Boolean, default: () => true, },  // дополнительные элементы (рулетка, масштаб)
  },

  components: { LMap, LTileLayer, LControlScale, LControlPolylineMeasure, EditorMap, },
  mixins: [ MixMeasure, MixResize, ],

  data: () => ({
    LOCAL_STORAGE_KEY_POSTFIX: 'geometry',
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
      'MAP_GET_TILE_VAL',
    ]),

    fc_parent: {
      get()    { return this.fc_parent_prop; },
      set(val) { this.$emit('fc_parent_change', val); },
    },
  },

  methods: {
    ...mapActions([
      'addNotification',
    ]),

    on_map_ready() {
      this.map = this.$refs.map.mapObject;
      this.map.doubleClickZoom.disable();
      this.map.invalidateSize();
    },

    on_map_resize () {                   // fire from MixResize
      if (this.map) this.map.invalidateSize();
    },

    on_map_dblclick(e) {
      // this.addNotification({content: e.latlng, timeout: 5, });
    },

    // сбросить выделение (obj, osm): из child.map в свойство child.nav
    on_map_reset_select() {
      this.$refs.notify.notify_del();
    },

    on_map_set_focus() {
      this.$refs.map.$el.focus()
    },

  },

}
</script>



<style scoped lang="scss">
  @import "~leaflet/dist/leaflet.css";
  @import "~@/components/Map/Leaflet/Lib/Lib.css";
</style>
