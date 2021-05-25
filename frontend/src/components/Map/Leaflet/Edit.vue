<template>
  <div
    v-if="MAP_GET_EDIT_ACTIVE"
  >

    <l-control
      position="topleft"
      class="leaflet-bar leaflet-control"
    >
      <a
        class="leaflet-buttons-control-button select_off"
        role="button"
        @click="data_ok"
      >OK</a>
    </l-control>

    <l-control
      position="topleft"
      class="leaflet-bar leaflet-control"
    >
      <a
        class="leaflet-buttons-control-button"
        role="button"
        title="Сохранить"
        @click="data_save"
      >
        <v-icon>mdi-content-save mdi-18px</v-icon>
      </a>
      <a
        class="leaflet-buttons-control-button"
        role="button"
        title="Восстановить"
        @click="data_load"
      >
        <v-icon>mdi-restore mdi-18px</v-icon>
      </a>
      <a
        class="leaflet-buttons-control-button"
        role="button"
        title="Очистить"
        @click="data_clear"
      >
        <v-icon>mdi-delete mdi-18px</v-icon>
      </a>
    </l-control>

    <l-control
      position="topleft"
      class="leaflet-bar leaflet-control"
    >
      <a
        v-if="mode_if_marker()"
        class="leaflet-buttons-control-button"
        :class="{ control_sel: editor_mode.marker }"
        role="button"
        title="Добавить маркер"
        @click="mode_trigger_marker"
      >
        <v-icon>mdi-map-marker mdi-18px</v-icon>
      </a>
      <a
        v-if="mode_if_line()"
        class="leaflet-buttons-control-button"
        :class="{ control_sel: editor_mode.line }"
        role="button"
        title="Добавить кривую"
        @click="mode_trigger_line"
      >
        <v-icon>mdi-vector-line mdi-18px</v-icon>
      </a>
      <a
        v-if="mode_if_polygon()"
        class="leaflet-buttons-control-button"
        :class="{ control_sel: editor_mode.polygon }"
        role="button"
        title="Добавить полигон"
        @click="mode_trigger_polygon"
      >
        <v-icon>mdi-vector-triangle mdi-18px</v-icon>
      </a>
      <a
        v-if="mode_if_cut()"
        class="leaflet-buttons-control-button"
        :class="{ control_sel: editor_mode.cut }"
        role="button"
        title="Обрезать"
        @click="mode_trigger_cut"
      >
        <v-icon>mdi-scissors-cutting mdi-18px</v-icon>
      </a>
    </l-control>

  </div>
</template>



<script>
import {
  mapGetters,
  mapActions,
} from 'vuex';

import {
  LControl,
} from "vue2-leaflet";

import {
  MAP_ITEM,
} from '@/components/Map/Leaflet/L.Const';

import {
  icon_get,
  icon_2_marker,
} from '@/components/Map/Leaflet/L.Marker';

import '@geoman-io/leaflet-geoman-free';


const COLOR_ORIGIN = 'black';   // цвет маркеров и фигур ДО    ИЗМЕНЕНИЯ
const COLOR_MODIFY = '#f00';    // цвет маркеров и фигур ПОСЛЕ ИЗМЕНЕНИЯ


export default {
  name: 'Edit',

  components: {
    LControl,
  },

  data() {
    return {
      editor_mode: {
        marker:  false,
        line:    false,
        polygon: false,
        cut:     false,
      },
    };
  },


  computed: {
    ...mapGetters([
      'MAP_GET_EDIT_ACTIVE',
      'MAP_GET_EDIT_MODE_MARKER',
      'MAP_GET_EDIT_MODE_LINE',
      'MAP_GET_EDIT_MODE_POLYGON',
      'MAP_GET_EDIT_SELECT',
      'MAP_GET_EDIT_DATA',
    ]),
  },


  mounted() {
    this.map = this.$parent.mapObject;    // в основном модуле: this.$refs.map.mapObject;
    this.map.pm.setLang('ru');
    // this.map.pm.addControls({
    //   position:         'topleft',
    //   oneBlock:         true,             // кнопки в одном блоке

    //   drawCircle:       false,
    //   drawCircleMarker: false,
    //   drawRectangle:    false,

    //   editMode:         false,
    //   dragMode:         false,
    //   removalMode:      false,
    // });

    let options = {
      snappable:             true,        // примагничивание
      snapDistance:          5,           // расстояние примагничивания
      tooltips:              false,       // подсказки
      allowSelfIntersection: false,       // самопересечения
      finishOn:              'dblclick',  // завершение редактирования
      continueDrawing:       false,       // продолжать создание
      markerStyle: {
        ...this.edit_property(),
        riseOnHover:         true,        // слой с маркером под курсором наверх
      },
      pathOptions: {
        ...this.edit_property(),
        ...this.path_origin(),
        ...this.path_modify(),
      },
      templineStyle: {                    // стиль зафиксированных линий при создании фигуры
        ...this.path_origin(),
        ...this.path_modify(),
      },
      hintlineStyle: {                    // стиль НЕ зафиксированных линий при создании фигуры
        ...this.path_origin(),
        ...this.path_modify(),
      },
    };
    let icon = this.icon_modify();
    if (icon) { options.markerStyle.icon = icon; }
    this.map.pm.setGlobalOptions(options);

    // создание фигур
    this.map.on('pm:create', this.on_pm_create);

    // разрешить режим редактирования для создаваемых пользователем фигур
    this.map.on('pm:drawend', this.on_pm_drawend);

    // загрузить данные
    this.data_load();

     // обработчики событий
    this.map.addEventListener('keydown', this.on_key_down);
  },

  beforeDestroy: function() {
    this.map.removeEventListener('keydown', this.on_key_down);
    this.map.off('pm:create',  this.on_pm_create);
    this.map.off('pm:drawend', this.on_pm_drawend);
  },


  watch: {
    MAP_GET_EDIT_DATA: {
      handler() { this.data_load(); },
      deep: true,
    },
  },


  methods: {
    ...mapActions([
      'MAP_ACT_EDIT_OFF',
      'MAP_ACT_EDIT_DATA',
    ]),


    // ======================================
    // РЕЖИМЫ
    // ======================================

    // разрешить режим редактирования для каждой редактируемой фигуры
    mode_enable() {
      this.map.eachLayer( function(layer) {
        if (
        (layer instanceof L.Path || layer instanceof L.Marker) &&
        (layer.pm) &&
        (layer.options.editor)) {
          layer.pm.enable({
            allowSelfIntersection: false,
            limitMarkersToCount:   20,        // количество редактируемых точек на линии
          });
        }
      });
    },

    // доступность режимов редактирования
    mode_if_marker()  { return  this.MAP_GET_EDIT_MODE_MARKER;  },
    mode_if_line()    { return  this.MAP_GET_EDIT_MODE_LINE;    },
    mode_if_polygon() { return  this.MAP_GET_EDIT_MODE_POLYGON; },
    mode_if_cut()     { return (this.MAP_GET_EDIT_MODE_LINE || this.MAP_GET_EDIT_MODE_POLYGON); },

    // включение режимов редактирования
    mode_on_marker()  { if (this.mode_if_marker())  { this.map.pm.enableDraw('Marker',  {}); this.editor_mode.marker  = true; }},
    mode_on_line()    { if (this.mode_if_line())    { this.map.pm.enableDraw('Line',    {}); this.editor_mode.line    = true; }},
    mode_on_polygon() { if (this.mode_if_polygon()) { this.map.pm.enableDraw('Polygon', {}); this.editor_mode.polygon = true; }},
    mode_on_cut()     { if (this.mode_if_cut())     { this.map.pm.enableDraw('Cut',     {}); this.editor_mode.cut     = true; }},

    // перелючение режимов редактирования
    mode_trigger_marker()  { if (!this.editor_mode.marker ) { this.mode_on_marker();  } else { this.mode_off(); }},
    mode_trigger_line()    { if (!this.editor_mode.line   ) { this.mode_on_line();    } else { this.mode_off(); }},
    mode_trigger_polygon() { if (!this.editor_mode.polygon) { this.mode_on_polygon(); } else { this.mode_off(); }},
    mode_trigger_cut()     { if (!this.editor_mode.cut    ) { this.mode_on_cut();     } else { this.mode_off(); }},

    // отключить режим редактирования если он включен
    mode_off() {
      this.map.pm.disableDraw();
      this.editor_mode.marker  = false;
      this.editor_mode.line    = false;
      this.editor_mode.polygon = false;
      this.editor_mode.cut     = false;
    },


    // ======================================
    // ДАННЫЕ
    // ======================================

    // при нажатии на ОК
    data_ok() {
      this.data_save();      // 1 - сохранить данные в state.data
      this.data_clear();     // 2 - очистить карту, state.data не чистим
      this.MAP_ACT_EDIT_OFF();      // 3 - выключить режим редактирования, state.data не чистим
    },


    // записать данные на шину из карты
    data_save() {
      this.mode_off();
      let fg = L.featureGroup();
      this.map.pm.getGeomanLayers().forEach(function(layer) {
        if (
          (layer.options.editor) &&
          (layer instanceof L.Path || layer instanceof L.Marker)) {
          // bug fix: удалить удаленные части фигур
          if (layer instanceof L.Path) {
            layer._latlngs = layer._latlngs.filter( x => (!(x instanceof Array) || (x.length > 0)));
          }
          fg.addLayer(layer);
        }
      });
      fg = fg.toGeoJSON();
      this.MAP_ACT_EDIT_DATA({data: fg});
    },


    // загрузить данные из шины на карту
    data_load() {
      // на неактивном компоненте загрузка отключена
      if (!this.MAP_GET_EDIT_ACTIVE) return;

      this.data_clear();

      let self  = this;
      let data  = this.MAP_GET_EDIT_DATA;

      // стили исходные
      let style = {
        onEachFeature: function(feature, layer)  { layer.options.editor =true;               },
        pointToLayer:  function(feature, latlng) { return self.marker_origin(latlng); },
        style:         function(feature)         { return self.path_origin();         },
      };
      let layer = (data.type=='FeatureCollection')?L.geoJSON(data, style):L.GeoJSON.geometryToLayer(data, style);

      // стили после редактирования
      layer.on('pm:edit',          this.style_modify, this);
      layer.on('pm:cut',           this.style_modify, this);
      layer.on('pm:vertexremoved', this.style_modify, this);

      // добавить слой на карту
      layer.addTo(this.map);

      // разрешить режим редактирования
      this.mode_enable();

      // включить редактирование
      //ddddd
    },


    // очистить данные на карте (шину не трогаем)
    data_clear() {
      let self = this;
      this.mode_off();
      this.map.pm.getGeomanLayers().forEach(function(layer) {
        if (layer.options.editor) {
          layer.off('pm:edit',          self.style_modify);
          layer.off('pm:cut',           self.style_modify);
          layer.off('pm:vertexremoved', self.style_modify);
          self.map.removeLayer(layer);
        }
      });
    },




    // ======================================
    // СТИЛИ
    // ======================================
    // признак редактирования
    edit_property() {
      return {
        editor: true,
      }
    },

    // стили после редактирования
    style_modify(e) {
      if (e.layer.setIcon)  e.layer.setIcon (this.icon_modify());
      if (e.layer.setStyle) e.layer.setStyle(this.path_modify());
    },

    // иконки
    icon_origin() {
      return icon_get({
        //name:  MAP_ITEM.MARKER.FONT,
        //icon:  'mdi-exclamation-thick',
        name:  MAP_ITEM.MARKER.COLOR,
        color: COLOR_ORIGIN,
      });
    },
    icon_modify() {
      return icon_get({
        name:  MAP_ITEM.MARKER.COLOR,
        color: COLOR_MODIFY,
      });
    },

    // маркеры
    marker_origin(latlng) {
      return icon_2_marker(latlng, this.icon_origin());
    },
    marker_modify(latlng) {
      return icon_2_marker(latlng, this.icon_modify());
    },

    // фигуры
    path_origin() {
      return {
          weight:      5,
          opacity:     .5,
          fillOpacity: .3,
          color:       COLOR_ORIGIN,
          fillColor:   COLOR_ORIGIN,
          dashArray:   '4, 8',
          //className: 'ddd',
        }
    },
    path_modify() {
      return {
          color:       COLOR_MODIFY,
          fillColor:   COLOR_MODIFY,
        }
    },



    // ======================================
    // СОБЫТИЯ
    // ======================================
    on_pm_create () { this.mode_off(); },
    on_pm_drawend() { this.mode_off(); this.mode_enable(); },
    on_key_down(e)  {
      switch (e.originalEvent.key) {
      case 'Escape':
        this.mode_off();
        break;

      case 'M': case 'm': // латиница
      case 'Ь': case 'ь': // русский
        if (e.originalEvent.shiftKey) { this.mode_on_marker(); }
        break;

      case 'L': case 'l': // латиница
      case 'Д': case 'д': // русский
        if (e.originalEvent.shiftKey) { this.mode_on_line(); }
        break;

      case 'P': case 'p': // латиница
      case 'З': case 'з': // русский
        if (e.originalEvent.shiftKey) { this.mode_on_polygon(); }
        break;

      case 'C': case 'c': // латиница
      case 'С': case 'с': // русский
        if (e.originalEvent.shiftKey) { this.mode_on_cut(); }
        break;
      }
    },

  },
}


</script>

<style scoped lang="scss">
  @import "~@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css";

  .control_sel {
    background-color: #dfd!important;
  }
  .control_sel > i {
    color: red!important;
  }
  .leaflet-bar.leaflet-control .v-icon {
    line-height: inherit;
  }

</style>
