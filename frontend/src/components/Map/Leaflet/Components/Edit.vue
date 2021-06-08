<template>
  <div>

    <l-control
      v-if="show_if"
      position="topleft"
      class="leaflet-bar leaflet-control"
    >
      <a
        v-if="mode_ok"
        class="leaflet-buttons-control-button select_off"
        role="button"
        @click="mode_ok_click"
      >OK</a>

      <a
        v-if="mode_enabled.marker"
        class="leaflet-buttons-control-button"
        :class="{ control_sel: mode_selected_if_marker() }"
        role="button"
        title="Добавить маркер"
        @click="mode_selected_trigger_marker"
      >
        <v-icon>mdi-map-marker mdi-18px</v-icon>
      </a>
      <a
        v-if="mode_enabled.line"
        class="leaflet-buttons-control-button"
        :class="{ control_sel: mode_selected_if_line() }"
        role="button"
        title="Добавить кривую"
        @click="mode_selected_trigger_line"
      >
        <v-icon>mdi-vector-line mdi-18px</v-icon>
      </a>
      <a
        v-if="mode_enabled.polygon"
        class="leaflet-buttons-control-button"
        :class="{ control_sel: mode_selected_if_polygon() }"
        role="button"
        title="Добавить полигон"
        @click="mode_selected_trigger_polygon"
      >
        <v-icon>mdi-vector-triangle mdi-18px</v-icon>
      </a>
      <a
        v-if="mode_enabled.cut"
        class="leaflet-buttons-control-button"
        :class="{ control_sel: mode_selected_if_cut() }"
        role="button"
        title="Обрезать"
        @click="mode_selected_trigger_cut"
      >
        <v-icon>mdi-scissors-cutting mdi-18px</v-icon>
      </a>
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

  </div>
</template>



<script>

/*
 * КОМПОНЕНТ: РЕДАКТОР ФИГУР
 *  <Edit
 *    v-model="fc"
 *    :options="options()"
 *    @ok="on_edit_stop_ok"
 *  />
 *
 *  options = {
 *    mode_enabled: {
 *      marker:  true,
 *      polygon: true,
 *    },
 *    mode_selected: 'Polygon',
 *  }
 *
 * v-model       - fc с двунаправленной связью, куда складываются данные
 *                 пустая область - { "type": "FeatureCollection", "features": [], } или L.featureGroup().toGeoJSON()
 *                 undedined      - режим редактирования выключается
 * mode_enabled  - доступные режимы редактирования (marker, line, polygon)
 * mode_selected - активизированный по умолчанию режим ('Marker', 'Line', 'Polygon')
 * @ok           - если задан - активна кнопка ОК
 *                 если задан - при обновлении fc включается режим редактирования
 *                 при нажатии на кнопку вызывается событие (возвращается копия fc) и редактирование завершается
 */

import { LControl, } from "vue2-leaflet";
import { MAP_ITEM, } from '@/components/Map/Leaflet/Lib/Const';
import { icon_get, icon_2_marker, } from '@/components/Map/Leaflet/Markers/Fun';
import '@geoman-io/leaflet-geoman-free';

const COLOR_ORIGIN = 'black';             // цвет маркеров и фигур ДО    ИЗМЕНЕНИЯ
const COLOR_MODIFY = '#f00';              // цвет маркеров и фигур ПОСЛЕ ИЗМЕНЕНИЯ
const TYPES = class {
  static MARKER  = 'Marker';
  static LINE    = 'Line';
  static POLYGON = 'Polygon';
  static CUT     = 'Cut';
};

export default {
  name:       'Edit',
  model:      { prop:  ['fc_prop'], event: 'fc_change', },
  props:      {
    fc_prop: {
      type: Object,
      default() { return undefined; },
    },
    options: {
      type: Object,
      default() {
        return {
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
  components: { LControl, },
  data() {
    return {
      show_if:       false,               // показать компонент
      mode_ok:       false,               // показывать кнопку ОК, позволяющую скрыть компонент (show_if)
      mode_enabled:  {                    // доступные фигуры, если не выбрано - доступно всё
        marker:        false,
        line:          false,
        polygon:       false,
        cut:           false,             // устанавливается автоматически при наличии line или polygon
      },
      mode_selected: undefined,           // выбранный по умолчанию режим
      fc_copy:       undefined,           // копия исходных данных fc
      fc_proxy:      undefined,           // fc_proxy в основе свойства fc
    };
  },

  computed: {
    fc: {                                 // FeatureCollection РЕДАКТИРУЕМЫХ объектов
      get()    {
        return this.fc_proxy;
      },
      set(val) {
        if (this.fc_proxy !== val) {
          this.fc_proxy = val;
          this.$emit('fc_change', val);
        }
      },
    },
  },

  watch: {
    // при изменении v-model
    fc_prop: {
      handler(val) {
        if (this.fc !== val) {
          this.fc_copy = val?JSON.parse(JSON.stringify(val)):undefined;
          this.map_load(val);
          this.mode_set(false);
        }
      },
      deep: true,
    },
  },


  mounted() {
    this.map = this.$parent.mapObject;    // в основном модуле: this.$refs.map.mapObject;
    this.map.pm.setLang('ru');

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

    // обработчик события: создание фигур
    this.map.on('pm:create', this.on_pm_create);

    // обработчик события: разрешить режим редактирования для создаваемых пользователем фигур
    this.map.on('pm:drawend', this.on_pm_drawend);

     // обработчик события: нажатие клавиши
    this.map.addEventListener('keydown', this.on_key_down);

    // установка данных
    this.fc = this.fc_prop;
    this.map_load(this.fc);

    // установка режима
    this.mode_set(true);
  },

  beforeDestroy: function() {
    this.mode_selected_off();
    this.mode_enabled_off();
    this.map.removeEventListener('keydown',    this.on_key_down);
    this.map.off                ('pm:create',  this.on_pm_create);
    this.map.off                ('pm:drawend', this.on_pm_drawend);
  },


  methods: {
    // ======================================
    // ДАННЫЕ НА КАРТЕ
    // ======================================

    // записать в fc
    map_save() {
      this.mode_selected_off();
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
    map_load(fc_new) {
      // очистить карту
      this.map_clear();

      // новые данные
      if (this.fc != fc_new) { this.fc = fc_new; }

      // при отсутствии данных отбой
      if (fc_new == undefined) return;

      // стили исходные
      let self  = this;
      let style = {
        onEachFeature: function(feature, layer)  { layer.options.editor = true;       },
        pointToLayer:  function(feature, latlng) { return self.marker_origin(latlng); },
        style:         function(feature)         { return self.path_origin();         },
      };
      let layer = (this.fc.type=='FeatureCollection')?L.geoJSON(this.fc, style):L.GeoJSON.geometryToLayer(this.fc, style);

      // события: установить
      this.events_layer_on(layer);

      // добавить слой на карту
      layer.addTo(this.map);

      // разрешить режим редактирования
      this.mode_pm_on();
    },


    // очистить на карте
    map_clear() {
      let self = this;
      this.mode_selected_off();
      this.map.pm.getGeomanLayers().forEach(function(layer) {
        if (layer.options.editor) {
          self.events_layer_off(layer);
          self.map.removeLayer(layer);
        }
      });
    },



    // ======================================
    // РЕЖИМЫ
    // ======================================

    // установить режим редактирования
    mode_set(first) {
      if (this.fc == undefined) {
        this.show_if = false;
      } else {
        this.mode_ok_set();
        this.mode_enabled_set();
        if (first) { this.mode_selected_set(); }
        this.show_if = true;
      }
    },

    // разрешить режим редактирования для каждой редактируемой фигуры
    mode_pm_on() {
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



    // ======================================
    // РЕЖИМ: КНОПКА ОК
    // ======================================
    mode_ok_set() {
      this.mode_ok = (this._events.ok !== undefined);
    },

    mode_ok_click() {
      this.$emit('ok', JSON.parse(JSON.stringify(this.fc)));
      this.fc_copy = undefined;
      this.fc = undefined;
      this.map_clear();
      this.mode_enabled_off();
      this.$nextTick(() => { this.show_if = false; });
    },




    // ======================================
    // РЕЖИМ: КНОПКИ РЕДАКТИРОВАНИЯ - ДОСТУПНОСТЬ
    // ======================================
    mode_enabled_set() {
      let mode_enabled_         =  this.options.mode_enabled || { marker: true, line: true, polygon: true, };
      this.mode_enabled.marker  =  mode_enabled_.marker      || false;
      this.mode_enabled.line    =  mode_enabled_.line        || false;
      this.mode_enabled.polygon =  mode_enabled_.polygon     || false;
      this.mode_enabled.cut     = (this.mode_enabled.line    || this.mode_enabled.polygon);
    },
    mode_enabled_off() {
      this.mode_enabled.marker  = false;
      this.mode_enabled.line    = false;
      this.mode_enabled.polygon = false;
      this.mode_enabled.cut     = false;
    },



    // ======================================
    // РЕЖИМ: КНОПКИ РЕДАКТИРОВАНИЯ - ВКЛЮЧЕНО
    // ======================================
    // режим по умолчанию
    mode_selected_set() {
      switch(this.options.mode_selected) {
        case TYPES.MARKER:  this.mode_selected_on_marker();  break;
        case TYPES.LINE:    this.mode_selected_on_line();    break;
        case TYPES.POLYGON: this.mode_selected_on_polygon(); break;
        case TYPES.CUT:     this.mode_selected_on_cut();     break;
      }
    },

    // выбрать режим
    mode_selected_on_marker()  { if (this.mode_enabled.marker)  { this.map.pm.enableDraw(TYPES.MARKER,  {}); this.mode_selected = TYPES.MARKER;  }},
    mode_selected_on_line()    { if (this.mode_enabled.line)    { this.map.pm.enableDraw(TYPES.LINE,    {}); this.mode_selected = TYPES.LINE;    }},
    mode_selected_on_polygon() { if (this.mode_enabled.polygon) { this.map.pm.enableDraw(TYPES.POLYGON, {}); this.mode_selected = TYPES.POLYGON; }},
    mode_selected_on_cut()     { if (this.mode_enabled.cut)     { this.map.pm.enableDraw(TYPES.CUT,     {}); this.mode_selected = TYPES.CUT;     }},

    // переключить режим
    mode_selected_trigger_marker() {
      if (!this.mode_enabled.marker) return;
      if (this.mode_selected == TYPES.MARKER) { this.mode_selected_off(); } else { this.mode_selected_on_marker(); }
    },
    mode_selected_trigger_line() {
      if (!this.mode_enabled.line) return;
      if (this.mode_selected == TYPES.LINE) { this.mode_selected_off(); } else { this.mode_selected_on_line(); }
    },
    mode_selected_trigger_polygon() {
      if (!this.mode_enabled.polygon) return;
      if (this.mode_selected == TYPES.POLYGON) { this.mode_selected_off(); } else { this.mode_selected_on_polygon(); }
    },
    mode_selected_trigger_cut() {
      if (!this.mode_enabled.cut) return;
      if (this.mode_selected == TYPES.CUT) { this.mode_selected_off(); } else { this.mode_selected_on_cut(); }
    },

    // проверить режим
    mode_selected_if_marker()  { return this.mode_selected == TYPES.MARKER;  },
    mode_selected_if_line()    { return this.mode_selected == TYPES.LINE;    },
    mode_selected_if_polygon() { return this.mode_selected == TYPES.POLYGON; },
    mode_selected_if_cut()     { return this.mode_selected == TYPES.CUT;     },

    // отключить режим
    mode_selected_off() {
      this.map.pm.disableDraw();
      this.mode_selected = undefined;
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
    events_layer_on(layer) {
      layer.on('pm:edit',           this.on_modify, this);
      layer.on('pm:cut',            this.on_modify, this);
      layer.on('pm:remove',         this.on_modify, this);
      layer.on('pm:vertexremoved',  this.on_modify, this);
    },

    events_layer_off(layer) {
      layer.off('pm:edit',          this.on_modify, this);
      layer.off('pm:cut',           this.on_modify, this);
      layer.off('pm:remove',        this.on_modify, this);
      layer.off('pm:vertexremoved', this.on_modify, this);
    },

    // очистить
    on_click_clear() {
      this.map_load(L.featureGroup().toGeoJSON());
    },

    // восстановить
    on_click_restore() {
      this.map_load(this.fc_copy)
    },

    // изменение на карте
    on_modify(e) {
      // сохранить данные из карты в fc
      this.map_save();

      // изменить стили после редактирования
      if (e.layer.setIcon)  e.layer.setIcon (this.icon_modify());
      if (e.layer.setStyle) e.layer.setStyle(this.path_modify());

      // установить события на новый слой при резке
      if (e.shape == 'Cut') this.events_layer_on(e.layer);
    },

    // операции с фигурами
    on_pm_create (e) { this.events_layer_on(e.layer); this.mode_selected_off(); this.map_save(); },
    on_pm_drawend(e) {                                this.mode_selected_off(); this.map_save(); this.mode_pm_on(); },

    // нажатие клавиши
    on_key_down(e)  {
      switch (e.originalEvent.key) {
      case 'Escape':
        this.mode_selected_off();
        break;

      case 'M': case 'm': // латиница
      case 'Ь': case 'ь': // русский
        if (e.originalEvent.shiftKey) { this.mode_selected_on_marker(); }
        break;

      case 'L': case 'l': // латиница
      case 'Д': case 'д': // русский
        if (e.originalEvent.shiftKey) { this.mode_selected_on_line(); }
        break;

      case 'P': case 'p': // латиница
      case 'З': case 'з': // русский
        if (e.originalEvent.shiftKey) { this.mode_selected_on_polygon(); }
        break;

      case 'C': case 'c': // латиница
      case 'С': case 'с': // русский
        if (e.originalEvent.shiftKey) { this.mode_selected_on_cut(); }
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
