<template>
      <l-map
        ref="map"
        style="z-index: 0;"
        :options="map_options"
        :crs="MAP_GET_TILE_VAL.crs"
        @ready="on_map_ready"
        @contextmenu=""
        @dblclick="on_map_dblclick"
      >
      <!--
        @contextmenu="on_menu_show($event,'editor')"
      -->

        <!-- ПОДЛОЖКА -->
        <l-tile-layer
          :url="MAP_GET_TILE_VAL.url"
          :attribution="MAP_GET_TILE_VAL.attr"
          :tms="MAP_GET_TILE_VAL.tms"
        />

        <!-- РЕДАКТОР -->
        <EditorMap
          v-model="fc"
          :modeEnabled="modeEnabled"
          :modeSelected="modeSelected"
          :modeEdit="modeEdit"
          @resetSelect="on_map_reset_select"
          @setFocus="on_map_set_focus"
        />

        <!-- МАСШТАБ -->
        <!--
        <l-control-scale
          v-if="MAP_GET_SCALE"
          position="bottomright"
          :imperial="false"
          :metric="true"
        />
        -->

        <!-- ЛИНЕЙКА -->
        <!--
        <l-control-polyline-measure
          v-if="MAP_GET_MEASURE"
          :options="measure_options()"
        />
        -->

        <!-- ЛОГОТИП -->
        <!-- <ControlLogo/> -->

        <!-- ЗАМЕТКИ -->
        <!-- <ControlNotify ref="notify"/> -->

      </l-map>
</template>



<script>

import { mapGetters, mapActions, } from 'vuex';
import 'leaflet';
import { LMap, LTileLayer, LControlScale, } from 'vue2-leaflet';
//import LControlPolylineMeasure from 'vue2-leaflet-polyline-measure';

//import { MAP_CONST } from '@/components/Map/Leaflet/Lib/Const';
//import EditorSplit   from '@/components/Map/Leaflet/Components/Editor/EditorSplit';
//import EditorNav     from '@/components/Map/Leaflet/Components/Editor/EditorNav';
import EditorMap     from '@/../../frontend/src/components/Map/Leaflet/Components/Editor/EditorMap';
//import ControlLogo   from '@/components/Map/Leaflet/Components/Control/ControlLogo';
//import ControlNotify from '@/components/Map/Leaflet/Components/Control/ControlNotify';
//import MixResize     from '@/components/Map/Leaflet/Mixins/Resize';
//import MixControl    from '@/components/Map/Leaflet/Mixins/Control';
//import MixMeasure    from '@/components/Map/Leaflet/Mixins/Measure';
//import MixMenu       from '@/components/Map/Leaflet/Mixins/Menu/Menu';

//import { fc_merge }  from '@/components/Map/Leaflet/Lib/LibFc';

export default {
  name: 'Map',
  //model: { prop:  ['fc_parent_prop'], event: 'fc_parent_change', },
  props: {
    // fc_parent_prop: { type: Object, default: () => undefined, },
    // modeEnabled: Object,      // доступные для создания элементы, например: { marker: true, line: true, polygon: true }
    // modeSelected: String,     // включенный по умолчанию режим, например: 'Polygon'
  },

  components: { LMap, LTileLayer, LControlScale, ControlLogo, LControlPolylineMeasure, EditorMap, EditorNav, EditorSplit, ControlNotify, },
  // mixins: [ MixMeasure, MixMenu, MixResize, MixControl, ],

  data: () => ({
    modeEdit: true,           // доступность редактирования, иначе только просмотр
    modeEnabled: { marker: true, line: true, polygon: true },
    modeSelected: 'Polygon',
    fc: undefined,
    map_options: {
      zoomControl: false,
      zoomSnap: 0.5,
    },
  }),

  created() {
    //this.fc = this.fc_old;
  },

  mounted() {
    this.resize_add(this.$refs.map.$el, this.on_map_resize);                        // установить слушатель map.on_resize
  },

  watch: {
    // fc: function(val) {
    //   this.fc_old = val;
    //   this.modeEdit = (JSON.stringify(val)?.length < MAP_CONST.GEOMETRY.BIG);       // доступность редактирования
    // },
  },

  computed: {
    // ...mapGetters([
    //   'MAP_GET_TILE_VAL',
    //   'MAP_GET_SCALE',
    //   'MAP_GET_MEASURE',
    // ]),

    // fc_old: {
    //   get()    { return this.fc_parent_prop; },
    //   set(val) { this.$emit('fc_parent_change', val); },
    // },
  },

  methods: {
    // ...mapActions([
    //   'addNotification',
    // ]),

    on_map_ready() {
      this.map = this.$refs.map.mapObject;
      // this.map.doubleClickZoom.disable();
      this.map.invalidateSize();
      // this.mounted_menu();                    // добавить обработчики горячих клавиш меню
    },

    on_map_resize () {                        // fire from MixResize
      if (this.map) this.map.invalidateSize();
    },

    on_map_dblclick(e) {
      // this.addNotification({content: e.latlng, });
    },

    // сбросить выделение (obj, osm): из child.map в свойство child.nav
    on_map_reset_select() {
      // this.$refs.notify.notify_del();
    },

    on_map_set_focus() {
      // this.$refs.map.$el.focus()
    },

    // обновить на карте fc
    on_nav_new(id, name, fc_new) {
      this.fc  = JSON.parse(JSON.stringify(fc_new));
      this.fc_old = this.fc;
      this.$refs.notify.notify_set(name);
    },
    on_nav_add(id, name, fc_new) {
      let fc_temp  = JSON.parse(JSON.stringify(fc_new));
      this.fc = fc_merge([this.fc, fc_temp,]);
      this.fc_old = this.fc;
      this.$refs.notify.notify_add(name);
    },

  },

}

/*
<style scoped lang="scss">
  @import "~leaflet/dist/leaflet.css";
  @import "~@/components/Map/Leaflet/Lib/Lib.css";
  @import "~@/components/Map/Leaflet/Mixins/Control.css";
</style>
*/
</script>

