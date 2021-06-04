<template>
  <div
    v-if="if_active"
  >

    <!--
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
    -->

    <l-control
      position="topleft"
      class="leaflet-bar leaflet-control"
    >
      <a
        class="leaflet-buttons-control-button"
        role="button"
        title="Восстановить"
        @click="on_click_restore"
      >
        <v-icon>mdi-restore mdi-18px</v-icon>
      </a>
      <a
        class="leaflet-buttons-control-button"
        role="button"
        title="Очистить"
        @click="on_click_clear"
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
        :class="{ control_sel: mode_enabled.marker }"
        role="button"
        title="Добавить маркер"
        @click="mode_trigger_marker"
      >
        <v-icon>mdi-map-marker mdi-18px</v-icon>
      </a>
      <a
        v-if="mode_if_line()"
        class="leaflet-buttons-control-button"
        :class="{ control_sel: mode_enabled.line }"
        role="button"
        title="Добавить кривую"
        @click="mode_trigger_line"
      >
        <v-icon>mdi-vector-line mdi-18px</v-icon>
      </a>
      <a
        v-if="mode_if_polygon()"
        class="leaflet-buttons-control-button"
        :class="{ control_sel: mode_enabled.polygon }"
        role="button"
        title="Добавить полигон"
        @click="mode_trigger_polygon"
      >
        <v-icon>mdi-vector-triangle mdi-18px</v-icon>
      </a>
      <a
        v-if="mode_if_cut()"
        class="leaflet-buttons-control-button"
        :class="{ control_sel: mode_enabled.cut }"
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

const options = {
  type: Object,
  default() { return {}; },
};

export default {
  name: 'Edit',
  model: {
    prop:  ['fc_prop'],
    event: 'fc_change',
  },
  props: ['fc_prop', 'options'],
  components: {
    LControl,
  },
  data() {
    return {
      if_active: true,          // активация режима - не изменять в MAP_ACT_EDIT_ON
      mode_enabled: {           // доступные фигуры, если не выбрано - доступно всё
        marker:    false,
        line:      false,
        polygon:   false,
        cut:       false,       // устанавливается автоматически при наличии line или polygon
      },
      select:    '',            // выбранный по умолчанию режим
      fc_copy:   undefined,     // копия исходных данных fc
    };
  },

  computed: {
    // FeatureCollection РЕДАКТИРУЕМЫХ объектов
    fc: {
      get()    { return this.fc_prop; },
      set(val) { this.$emit('fc_change', val); },
    },
  },

  created() {
  },

  mounted() {
    // скопировать исходные данные
    this.fc_copy = this.fc?JSON.parse(JSON.stringify(this.fc)):undefined;

    let mode_enabled2 = this.options.mode_enabled     || {};
    this.mode_enabled.marker  = mode_enabled2.marker  || false;
    this.mode_enabled.line    = mode_enabled2.line    || false;
    this.mode_enabled.polygon = mode_enabled2.polygon || false;

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

    // загрузить данные на карту
    this.map_load();

     // обработчики событий
    this.map.addEventListener('keydown', this.on_key_down);
  },

  beforeDestroy: function() {
    this.map.removeEventListener('keydown', this.on_key_down);
    this.map.off('pm:create',  this.on_pm_create);
    this.map.off('pm:drawend', this.on_pm_drawend);
  },


  methods: {
    // ======================================
    // РЕЖИМЫ
    // ======================================

    // разрешить режим редактирования для каждой редактируемой фигуры
    mode_on() {
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
    mode_if_marker()  {
      console.log(this.mode_enabled.marker); return  true;
      }, //this.mode_enabled.marker;  },
    mode_if_line()    { return  this.mode_enabled.line;    },
    mode_if_polygon() { return  this.mode_enabled.polygon; },
    mode_if_cut()     { return (this.mode_enabled.line || this.mode_enabled.polygon); },

    // включение режимов редактирования
    mode_on_marker()  { if (this.mode_if_marker())  { this.map.pm.enableDraw('Marker',  {}); this.mode_enabled.marker  = true; }},
    mode_on_line()    { if (this.mode_if_line())    { this.map.pm.enableDraw('Line',    {}); this.mode_enabled.line    = true; }},
    mode_on_polygon() { if (this.mode_if_polygon()) { this.map.pm.enableDraw('Polygon', {}); this.mode_enabled.polygon = true; }},
    mode_on_cut()     { if (this.mode_if_cut())     { this.map.pm.enableDraw('Cut',     {}); this.mode_enabled.cut     = true; }},

    // перелючение режимов редактирования
    mode_trigger_marker()  { if (!this.mode_enabled.marker ) { this.mode_on_marker();  } else { this.mode_off(); }},
    mode_trigger_line()    { if (!this.mode_enabled.line   ) { this.mode_on_line();    } else { this.mode_off(); }},
    mode_trigger_polygon() { if (!this.mode_enabled.polygon) { this.mode_on_polygon(); } else { this.mode_off(); }},
    mode_trigger_cut()     { if (!this.mode_enabled.cut    ) { this.mode_on_cut();     } else { this.mode_off(); }},

    // отключить режим редактирования и скрыть кнопки
    mode_off() {
      this.map.pm.disableDraw();
      this.mode_enabled.marker  = false;
      this.mode_enabled.line    = false;
      this.mode_enabled.polygon = false;
      this.mode_enabled.cut     = false;
    },


    // ======================================
    // ДАННЫЕ НА КАРТЕ
    // ======================================

    // записать в fc
    map_save() {
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
      this.fc = fg.toGeoJSON();
    },


    // загрузить из fc
    map_load() {
      // на неактивном компоненте загрузка отключена
      if (!this.if_active) return;

      // очистить карту
      this.map_clear();

      // стили исходные
      let self  = this;
      let style = {
        onEachFeature: function(feature, layer)  { layer.options.editor =true;               },
        pointToLayer:  function(feature, latlng) { return self.marker_origin(latlng); },
        style:         function(feature)         { return self.path_origin();         },
      };
      let layer = (this.fc.type=='FeatureCollection')?L.geoJSON(this.fc, style):L.GeoJSON.geometryToLayer(this.fc, style);

      // стили после редактирования
      layer.on('pm:edit',          this.on_modify, this);
      layer.on('pm:cut',           this.on_modify, this);
      layer.on('pm:vertexremoved', this.on_modify, this);

      // добавить слой на карту
      layer.addTo(this.map);

      // разрешить режим редактирования
      this.mode_on();
    },


    // очистить на карте
    map_clear() {
      let self = this;
      this.mode_off();
      this.map.pm.getGeomanLayers().forEach(function(layer) {
        if (layer.options.editor) {
          layer.off('pm:edit',          self.on_modify);
          layer.off('pm:cut',           self.on_modify);
          layer.off('pm:vertexremoved', self.on_modify);
          self.map.removeLayer(layer);
        }
      });
    },





    // ======================================
    // СТИЛИ
    // ======================================
    // признак редактирования
    edit_property() {
      return { editor: true, }
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

    // очистить
    on_click_clear() {
      this.fc = L.featureGroup().toGeoJSON();
      this.$nextTick(() => { this.map_load(); })
    },

    // восстановить
    on_click_restore() {
      this.fc = this.fc_copy?JSON.parse(JSON.stringify(this.fc_copy)):undefined;
      this.$nextTick(() => { this.map_load(); })
    },

    // изменение на карте
    on_modify(e) {
      // сохранить данные из карты в fc
      this.map_save();

      // изменить стили после редактирования
      if (e.layer.setIcon)  e.layer.setIcon (this.icon_modify());
      if (e.layer.setStyle) e.layer.setStyle(this.path_modify());
    },

    // операции с фигурами
    on_pm_create () { this.mode_off(); },
    on_pm_drawend() { this.mode_off(); this.mode_on(); },

    // нажатие клавиши
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
