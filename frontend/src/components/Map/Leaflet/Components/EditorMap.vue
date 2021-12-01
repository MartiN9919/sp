<template>
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
        v-if="modeEdit"
        class="leaflet-buttons-control-button"
        role="button"
        title="Восстановить"
        @click="on_click_restore"
      >
        <v-icon>mdi-restore mdi-18px</v-icon>
      </a>
      <a
        v-if="modeEdit"
        class="leaflet-buttons-control-button"
        role="button"
        title="Очистить"
        @click="on_click_clear"
      >
        <v-icon>mdi-delete mdi-18px</v-icon>
      </a>
    </l-control>
</template>



<script>

/*
 * КОМПОНЕНТ: РЕДАКТОР ФИГУР
 *  <EditorMap
 *    v-model="fc"
 *    :modeEnabled="modeEnabled"
 *    :modeSelected="modeSelected"
 *    @ok="on_edit_stop_ok"
 *    @restore=""
 *    @clear=""
 *  />
 *
 *  modeEnabled = {
 *    marker:  true,
 *    polygon: true,
 *  },
 *  modeSelected: 'Polygon',
 *
 * v-model       - fc с двунаправленной связью, куда складываются данные
 *                 пустая область - { "type": "FeatureCollection", "features": [], } или L.featureGroup().toGeoJSON()
 *                 undedined      - режим редактирования выключается
 * mode_enabled  - доступные режимы редактирования (marker, line, polygon)
 * mode_selected - активизированный по умолчанию режим ('Marker', 'Line', 'Polygon')
 * modeEdit      - доступность редактирования, иначе только просмотр
 * @ok           - если задан - активна кнопка ОК
 *                 если задан - при обновлении fc включается режим редактирования
 *                 при нажатии на кнопку вызывается событие (возвращается копия fc) и редактирование завершается
 * @restore      - событие при нажатии на кнопку restore
 * @clear        - событие при нажатии на кнопку clear
 */

import { LControl, } from "vue2-leaflet";
import { MAP_CONST, MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { icon_get, icon_2_marker, } from '@/components/Map/Leaflet/Components/Style/StyleIcon';
import { fc_normalize, } from '@/components/Map/Leaflet/Lib/LibFc';
import '@geoman-io/leaflet-geoman-free';

const TYPES = class {
  static MARKER   = 'Marker';
  static LINE     = 'Line';
  static POLYGON  = 'Polygon';
  static CUT      = 'Cut';
};
const FC_KEY_VAL    = 'val';              // fc
const FC_KEY_ORIGIN = 'origin';           // признак данных как не измененных (в черном, а не красном)
const FC_KEY_NEW    = 'new';              // признак новых данных на замену старых
const FC_KEY_COPY   = 'copy';             // признак необходимости копирования данных в fc_copy
const FC_KEY_MODE   = 'mode';             // признак необходимости установки режима редактирования (линия, точка, ...)

export default {
  name: 'EditorMap',
  model: { prop:  ['fc_prop'], event: 'fc_change', },

  props: {
    fc_prop:      { type: Object,  default: () => undefined, },
    modeSelected: { type: String,  default: () => undefined, }, // включенный по умолчанию режим: 'polygon', 'line', 'marker', 'cut'
    modeEnabled:  { type: Object,  default: () => ({ marker: true, line: true, polygon: true, }), }, // доступные для создания элементы
    modeEdit:     { type: Boolean, default: () => true, } // доступность редактирования, иначе только просмотр
  },
  emits: [
    'fc_change',                          // изменение fc пользователем
    'resetSelect',                        // для сброса выбора в nav
    'ok',                                 // нажатие кнопки ок
  ],

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
      fc_copy:       L.featureGroup().toGeoJSON(), // копия исходных данных fc
      fc_wait:       undefined,           // ожидаемое значение fc в watch после set
    };
  },

  computed: {
    fc: {
      get() { return this.fc_prop },
      set(obj) {
        let val       = (obj) ? ((FC_KEY_VAL    in obj) ? obj[FC_KEY_VAL]    : obj  ) : obj;
        let is_origin = (obj) ? ((FC_KEY_ORIGIN in obj) ? obj[FC_KEY_ORIGIN] : true)  : true;
        let is_new    = (obj) ? ((FC_KEY_NEW    in obj) ? obj[FC_KEY_NEW]    : false) : false;
        let is_copy   = (obj) ? ((FC_KEY_COPY   in obj) ? obj[FC_KEY_COPY]   : false) : false;
        let is_mode   = (obj) ? ((FC_KEY_MODE   in obj) ? obj[FC_KEY_MODE]   : false) : false;

        if (is_copy) {
          this.fc_copy = val?JSON.parse(JSON.stringify(val)):undefined; // глубокая копия для возможного восстановления
        }

        this.fc_wait = val;
        this.$emit('fc_change', val);       // вызывает отложенный watch.fc

        if (is_new) {
          this.map_load(val, is_origin);
          this.editor_set(is_mode);
        }
      },
    },
  },

  watch: {
    // при внешнем и внутреннем изменении fc (после fc.set)
    fc_prop: {
      handler(val) {
        // блокировать следствие внутреннего изменения fc
        let is_in = (val == this.fc_wait);
        this.fc_wait = undefined;
        if (is_in) { return }

        // вызвать fc.set
        this.fc = {
          [FC_KEY_VAL]:    val?JSON.parse(JSON.stringify(val)):undefined,
          [FC_KEY_ORIGIN]: false,
          [FC_KEY_NEW]:    true,
          [FC_KEY_COPY]:   false,
        };
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
        ...this.layer_editor_prop(),      // признак редактирования слоя
        riseOnHover:         true,        // слой с маркером под курсором наверх
      },
      pathOptions: {
        //...this.layer_editor_prop(),    // признак редактирования слоя
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
    // L.PM.setOptIn(true);

    // обработчик события: создание фигур
    this.map.on('pm:create', this.on_pm_create);

    // обработчик события: разрешить режим редактирования для создаваемых пользователем фигур
    this.map.on('pm:drawend', this.on_pm_drawend);

     // обработчик события: нажатие клавиши
    this.map.addEventListener('keydown', this.on_key_down);

    // установка данных
    this.fc = {
      [FC_KEY_VAL]:    this.fc,
      [FC_KEY_ORIGIN]: true,
      [FC_KEY_NEW]:    true,
      [FC_KEY_COPY]:   true,
      [FC_KEY_MODE]:   true,
    };
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

    // записать из карты в fc
    map_save() {
      this.mode_selected_off();
      let fg = L.featureGroup();
      this.map.pm.getGeomanLayers(true).eachLayer(function(layer) {
        if (this.layer_editor_is(layer)) {
          if ((layer instanceof L.Path) || (layer instanceof L.Marker)) {
            // bug fix: удалить удаленные части фигур
            if (layer instanceof L.Path) {
              layer._latlngs = layer._latlngs.filter( x => (!(x instanceof Array) || (x.length > 0)));
            }
            fg.addLayer(layer);
          }
        }
      }.bind(this));

      this.fc = {
        [FC_KEY_VAL ]:   fc_normalize(fg.toGeoJSON()), // fc_normalize: fix bug missing properties when cut features
        [FC_KEY_ORIGIN]: true,
        [FC_KEY_NEW ]:   false,
        [FC_KEY_COPY]:   false,
      };
    },


    // загрузить на карту из fc
    // fc указывается как аргумент, т.к. функция вызывается из fc.set, когда значение this.fc еще старое
    // mode_origin - загрузить как уже неизмененное (черное, а не красное)
    map_load(fc, mode_origin=true) {
      // отключить возможный режим редактирования
      this.mode_selected_off();

      // очистить карту
      this.map_clear();

      // при отсутствии данных отбой
      if (fc == undefined) return;

      // стили исходные
      let self  = this;
      let style = (mode_origin) ?
        {
          pointToLayer:  function(feature, latlng) { return self.marker_origin(latlng); },
          style:         function(feature)         { return self.path_origin(); },
          // onEachFeature: function(feature, layer)  { },
        } :
        {
          pointToLayer:  function(feature, latlng) { return self.marker_modify(latlng); },
          style:         function(feature)         { return self.path_modify(); },
        };
      let layer = (fc.type.toLowerCase()==='featurecollection')?L.geoJSON(fc, style):L.GeoJSON.geometryToLayer(fc, style);
      // слой: настроить
      this.layer_set(layer);
      // if (!mode_origin) { this.layer_style_modify(layer) } - маркеры не реагируют

      // слой: добавить на карту
      layer.addTo(this.map);

      // разрешить редактирование каждой редактируемой фигуры
      this.editor_on();

      // позиционирование карты на layer (отложено, так как сначала позиционируется по key[1])
      this.$nextTick(function() {
        if (layer.hasOwnProperty('_layers') && Object.keys(layer._layers).length > 0) {
          this.map.fitBounds(layer.getBounds(), { padding: [30, 30], });
        }
        else {
          this.map.setView(layer._latlng)
        }
      });
    },


    // карта: очистить
    map_clear() {
      this.mode_selected_off();
      this.map.pm.getGeomanLayers(true).eachLayer(function(layer) {
        if (this.layer_editor_is(layer)) {
          this.layer_del(layer)
        }
      }.bind(this));
    },



    // ======================================
    // СЛОИ
    // ======================================
    layer_set(layer) {
      // layer.pmIgnore = false;
      // L.PM.reInitLayer(layer);

      layer.on('pm:edit',           this.on_modify, this);
      layer.on('pm:cut',            this.on_modify, this);
      layer.on('pm:remove',         this.on_modify, this);
      layer.on('pm:vertexremoved',  this.on_modify, this);
    },

    layer_free(layer) {
      layer.off('pm:edit',          this.on_modify, this);
      layer.off('pm:cut',           this.on_modify, this);
      layer.off('pm:remove',        this.on_modify, this);
      layer.off('pm:vertexremoved', this.on_modify, this);
    },

    layer_del(layer) {
      this.layer_free(layer);
      this.map.removeLayer(layer);
    },


    layer_editor_prop()    { return { editor: this._uid, } },
    layer_editor_is(layer) { return (layer.options.editor === this._uid) },


    // ======================================
    // РЕЖИМЫ
    // ======================================

    // установить режим редактирования
    editor_set(first) {
      if (this.fc == undefined) {
        this.show_if = false;
      } else {
        this.mode_ok_set();
        this.mode_enabled_set();
        if (first) { this.mode_selected_set(); }
        this.show_if = true;
      }
    },

    // разрешить редактирование каждой редактируемой фигуры
    editor_on() {
      this.map.pm.getGeomanLayers(true).eachLayer(function(layer) {
        if (this.layer_editor_is(layer)) {
          layer.pm.enable({
            allowSelfIntersection: false,     // запретить самопересечения линий
            limitMarkersToCount:   5,         // количество редактируемых точек на линии
          });
        }
      }.bind(this));
    },



    // ======================================
    // РЕЖИМ: КНОПКА ОК
    // ======================================
    mode_ok_set() {
      this.mode_ok = (this._events.ok !== undefined);
    },

    mode_ok_click() {
      // this.mode_selected_off();
      this.$emit('ok', JSON.parse(JSON.stringify(this.fc)));
      this.fc_copy = undefined;
      this.$emit('fc_change', undefined);
      this.map_clear();
      this.mode_enabled_off();
      this.$nextTick(() => { this.show_if = false; });
    },




    // ======================================
    // РЕЖИМ: КНОПКИ РЕДАКТИРОВАНИЯ - ДОСТУПНОСТЬ
    // ======================================
    mode_enabled_set() {
      let mode_enabled_         =  this.modeEnabled       || { marker: true, line: true, polygon: true, };
      this.mode_enabled.marker  =  mode_enabled_.marker   || false;
      this.mode_enabled.line    =  mode_enabled_.line     || false;
      this.mode_enabled.polygon =  mode_enabled_.polygon  || false;
      this.mode_enabled.cut     = (this.mode_enabled.line || this.mode_enabled.polygon);
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
      if (!this.modeSelected) return;

      let mode = this.modeSelected.trim().toLowerCase();
      switch(mode) {
        case 'marker':  this.mode_selected_on_marker();  break;
        case 'line':    this.mode_selected_on_line();    break;
        case 'polygon': this.mode_selected_on_polygon(); break;
        case 'cut':     this.mode_selected_on_cut();     break;
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
    mode_selected_if() { return (
      this.mode_selected_if_marker()  ||
      this.mode_selected_if_line()    ||
      this.mode_selected_if_polygon() ||
      this.mode_selected_if_cut()
    )},
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

    // установить слою измененное состояние
    layer_style_modify(layer) {
      if (layer.setIcon)  layer.setIcon (this.icon_modify());
      if (layer.setStyle) layer.setStyle(this.path_modify());
    },


    // иконки
    icon_origin() { return icon_get(MAP_CONST.COLOR.EDITOR_ORIGIN); },
    icon_modify() { return icon_get(MAP_CONST.COLOR.EDITOR_MODIFY); },

    // маркеры
    marker_origin(latlng) {
      return icon_2_marker(latlng, this.icon_origin(), this.layer_editor_prop());
    },
    marker_modify(latlng) {
      return icon_2_marker(latlng, this.icon_modify(), this.layer_editor_prop());
    },

    // фигуры
    path_common() {
      return {
        weight:      5,
        opacity:     .5,
        fillOpacity: .3,
        dashArray:   '4, 8',
      }
    },
    path_origin() {
      return {
        ...this.layer_editor_prop(),
        ...this.path_common(),
        color:       MAP_CONST.COLOR.EDITOR_ORIGIN,
        fillColor:   MAP_CONST.COLOR.EDITOR_ORIGIN,
      }
    },
    path_modify() {
      return {
        ...this.layer_editor_prop(),
        ...this.path_common(),
        color:       MAP_CONST.COLOR.EDITOR_MODIFY,
        fillColor:   MAP_CONST.COLOR.EDITOR_MODIFY,
      }
    },



    // ======================================
    // СОБЫТИЯ
    // ======================================

    // очистить
    on_click_clear() {
      this.fc = {
        [FC_KEY_VAL]:    L.featureGroup().toGeoJSON(),
        [FC_KEY_ORIGIN]: true,
        [FC_KEY_NEW]:    true,
        [FC_KEY_COPY]:   false,
      }
      // сбросить map.notify
      this.$emit('resetSelect');
    },

    // восстановить
    on_click_restore() {
      this.fc = {
        [FC_KEY_VAL]:    this.fc_copy?JSON.parse(JSON.stringify(this.fc_copy)):undefined,
        [FC_KEY_ORIGIN]: true,
        [FC_KEY_NEW]:    true,
        [FC_KEY_COPY]:   false,
      };
      // сбросить map.notify
      this.$emit('resetSelect');
    },

    // изменение на карте
    on_modify(e) {
      // изменить стили после редактирования
      this.layer_style_modify(e.layer);

      // настроить новый слой при резке
      if (e.shape == 'Cut') {
        this.layer_set(e.layer);
        this.editor_on();
      }

      // сохранить данные из карты в fc
      this.map_save();

      // сбросить map.notify
      this.$emit('resetSelect');
    },

    // операции с фигурами
    // при create срабатывает on_pm_create, потом on_pm_drawend
    // при разрезании фигуры - только on_pm_drawend
    on_pm_create (e) {
      this.layer_set(e.layer);
    },
    on_pm_drawend(e) {
      this.mode_selected_off();
      this.map_save();
      this.editor_on();

      // сбросить map.notify
      // this.$emit('resetSelect');
    },

    // нажатие клавиши
    on_key_down(e)  {
      switch (e.originalEvent.key) {
      case 'Escape':
        if (this.mode_selected_if()) {
          this.mode_selected_off();
          e.originalEvent.stopPropagation();  // чтобы по ESC не закрылось окно
          this.$emit('setFocus');
        }
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
