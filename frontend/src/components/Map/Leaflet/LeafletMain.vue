<template>
  <div
    style="height: 100%; width: 100%;"
    >

    <!-- SVG DEFS, STYLE -->
    <l-style-svg/>

    <l-map
      ref="map"
      style="height: 100%; z-index: 0;"
      :options="mapOptions"
      :crs="MAP_GET_TILE_VAL.crs"
      @ready="on_map_ready"
      @resize="on_map_resize"
      @zoomend="on_map_zoom"
      @click="on_map_click"
      @dblclick="on_map_dblclick"
      @contextmenu="on_menu_show"
    >

      <!-- ПОДЛОЖКА -->
      <l-tile-layer
        :url="MAP_GET_TILE_VAL.url"
        :attribution="MAP_GET_TILE_VAL.attr"
        :tms="MAP_GET_TILE_VAL.tms"
      />


      <!-- ФИГУРЫ -->
      <l-layer-group
        v-for="(map_item, map_ind) in SCRIPT_GET"
        :key="MAP_GET_KEY(map_ind)"
      >
        <l-marker-cluster
          :options="cluster_options(map_ind)"
        >
          <l-geo-json
            :geojson="data_normalize(map_ind, map_item)"
            :options="geojson_options(map_ind)"
          />
        </l-marker-cluster>

        <!-- ДЕКОРАТОР ФИГУР -->
        <l-style-decor
          :fc="data_normalize(map_ind, map_item)"
          :color="SCRIPT_GET_ITEM_COLOR(map_ind)"
        />
      </l-layer-group>

      <!-- РЕДАКТОР -->
      <EditorMap
        v-model="fc_edit"
        @ok="on_edit_ok"
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

      <!-- ВРЕМЕННОЙ ФИЛЬТР -->
      <ControlRange ref="range"/>

      <!-- ЛЕГЕНДА -->
      <ControlLegend :options="legend_options()"/>

      <!-- ЛОГОТИП -->
      <ControlLogo/>

    </l-map>

    <DialogMenuPos
      ref="key_dialog"
      @ok="menu_pos_save_ok"
    />

    <contextMenuNested
      ref="menu"
      :form="form"
      :items="menu_struct"
    />

  </div>
</template>



<script>

import { mapGetters, mapActions } from 'vuex';
import { Icon } from 'leaflet';

import {
  LMap,
  LTileLayer,
  LMarker,
  LPolyline,
  LPolygon,
  LPopup,
  LTooltip,
  LFeatureGroup,
  LLayerGroup,
  LGeoJson,
  LControlScale,
  LControl,
  LIcon,
} from 'vue2-leaflet';

import Vue2LeafletMarkerCluster from 'vue2-leaflet-markercluster';
import LControlPolylineMeasure  from 'vue2-leaflet-polyline-measure';

import { MAP_CONST, MAP_ITEM }  from '@/components/Map/Leaflet/Lib/Const';
import { get_feature_class, set_feature_hint } from '@/components/Map/Leaflet/Lib/LibFc';
import {
  icon_ini,
  marker_get,
  icon_group_get,
} from '@/components/Map/Leaflet/Components/Style/StyleIcon';

import StyleSvg         from '@/components/Map/Leaflet/Components/Style/StyleSvg';
import { correct_classes_name } from '@/components/Map/Leaflet/Components/Style/StyleData';
import StyleDecor       from '@/components/Map/Leaflet/Components/Style/StyleDecor';

import EditorMap        from '@/components/Map/Leaflet/Components/Editor/EditorMap';
import ControlRange     from '@/components/Map/Leaflet/Components/Control/ControlRange';
import ControlLegend    from '@/components/Map/Leaflet/Components/Control/ControlLegend';
import ControlLogo      from '@/components/Map/Leaflet/Components/Control/ControlLogo';
import MixResize        from '@/components/Map/Leaflet/Mixins/Resize';
import MixColor         from '@/components/Map/Leaflet/Mixins/Color';
import MixControl       from '@/components/Map/Leaflet/Mixins/Control';
import MixMeasure       from '@/components/Map/Leaflet/Mixins/Measure';
import MixMenu          from '@/components/Map/Leaflet/Mixins/Menu/Menu';


// устранение бага с путями
icon_ini();


export default {
  name: 'LeafletMain',

  mixins: [
    MixResize,
    MixColor,
    MixControl,
    MixMeasure,
    MixMenu,
  ],


  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    LTooltip,
    LFeatureGroup,
    LLayerGroup,
    LGeoJson,
    LPolyline,
    LPolygon,
    LControlScale,
    LControl,
    LIcon,
    'l-marker-cluster': Vue2LeafletMarkerCluster,
    'l-style-svg':      StyleSvg,
    'l-style-decor':    StyleDecor,
    LControlPolylineMeasure,

    EditorMap,
    ControlRange,
    ControlLegend,
    ControlLogo,
  },


  data() {
    return {
      hover_map_ind:     -1,      // MAP_ITEM[hover_map_ind]                   - блок, над которым находится курсор
      hover_feature_ind: -1,      // MAP_ITEM[].FC.features[hover_feature_ind] - фигура, над которой находится курсор
      mapOptions: {
        zoomControl: false,
        zoomSnap:    0.5,
      },
    };
  },


  mounted: function() {
    this.map = this.$refs.map.mapObject;
    this.map.doubleClickZoom.disable();

    // установить слушатель map.on_resize
    this.resize_add(this.$refs.map.$el, this.on_map_resize);

    // добавить обработчики горячих клавиш меню
    this.mounted_menu();
  },


  computed: {
    ...mapGetters([
      'MAP_GET_KEY',
      'MAP_GET_TILE_VAL',
      'MAP_GET_SCALE',
      'MAP_GET_MEASURE',
      'MAP_GET_CLUSTER',
      'MAP_GET_HINT',

      'MAP_GET_ZOOM',
      'MAP_GET_EDIT',

      'SCRIPT_GET',
      'SCRIPT_GET_ITEM',
      'SCRIPT_GET_ITEM_COLOR',
      'SCRIPT_GET_ITEM_FC_STYLE_LINE',
      'SCRIPT_GET_ITEM_FC_STYLE_POLYGON',
      'SCRIPT_GET_ITEM_SEL',
      'SCRIPT_GET_ITEM_FIND_ACTIVE',
    ]),

    // FeatureCollection РЕДАКТИРУЕМЫХ объектов
    fc_edit: {
      get()    { return this.MAP_GET_EDIT; },
      set(val) { /* this.MAP_ACT_EDIT({data: val}); */ },
    },
  },


  methods: {
    ...mapActions([
      'MAP_ACT_ZOOM',
      'MAP_ACT_EDIT',
      'SCRIPT_ACT_SEL_SET',
      'SCRIPT_ACT_SEL_CLEAR',
      'addNotification',
      'setNavigationDrawerStatus',
      'setActiveTool',
      'changeSelectedTreeViewItem',
    ]),


    // ===============
    // LEGEND
    // ===============
    legend_options() {
      return {
        hover_map_ind     : this.hover_map_ind,
        hover_feature_ind : this.hover_feature_ind,
      }
    },

    legend_hide() {
      this.hover_map_ind     = -1;
      this.hover_feature_ind = -1;
    },


    // ===============
    // MAP
    // ===============
    // корректировать данные
    data_normalize(map_ind, map_item) {
      // рассчитать цвета (легенда, цвет от значения в группе)
      this.data_normalize_color(map_item);

      // deep copy
      let fc = map_item.fc;
      fc = JSON.parse(JSON.stringify(fc));

      // установить fc.features[ind].ind - порядковый номер фигуры в fc
      for(let ind=0; ind<fc.features.length; ind++) { fc.features[ind][MAP_ITEM.FC.FEATURES.IND] = ind; }

      // отфильтровать с допустимыми датами
      fc = this.$refs.range.filter(fc);

      return fc;
    },

    cluster_options(map_ind) {
      let color = this.SCRIPT_GET_ITEM_COLOR(map_ind);
      return {
        // область при наведении курсора на кластер
        showCoverageOnHover: true,
        polygonOptions: { color: color, },

        // для последующей коррекции цвета маркеров
        cluster_color: color,

        // увеличение, при котором создавать кластеры
        disableClusteringAtZoom: this.MAP_GET_CLUSTER?17:0,

        // подмена иконки кластера
        iconCreateFunction: function (cluster) {
          // select фактически не имеет смысла, т.к. могут группироваться маркеры с разными id
          return icon_group_get(color, cluster.getChildCount()); //, feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES._SEL_]
        },

        // цвет региона сгруппированного кластера
        spiderLegPolylineOptions: { weight: 1.5, color: color, opacity: 0.5 },

        // несгрупированные и сгруппированные маркеры одинаковы
        // singleMarkerMode: true,
      };
    },


    geojson_options(map_ind) {
      let self = this;
      return {
        // для каждого маркера / фигуры
        onEachFeature: function(feature, layer) {
          // control-легенда: установка onHover
          // события повторно вызывают this.data_normalize_color
          let self = this;
          layer.on('mouseover', function(e) { self.hover_map_ind = map_ind;  self.hover_feature_ind = feature[MAP_ITEM.FC.FEATURES.IND]; });
          layer.on('mouseout',  function(e) {
            if (!e.originalEvent.ctrlKey) self.hover_map_ind = -1;
            self.hover_feature_ind = -1;
          });
          layer.on('click', function(e) {
            // реакция выделения только на объекты из БД
            if ((!e.target.feature.obj_id) || (!e.target.feature.rec_id)) return;
            L.DomEvent.stopPropagation(e);
            // выделить элемент на карте
            let dat = {
              active_script_id: self.SCRIPT_GET_ITEM(map_ind).refresh,  // в качестве id экзеспляра скрипта используем TS
              obj_id:           e.target.feature.obj_id,
              rec_id:           e.target.feature.rec_id,
              ctrl:             e.originalEvent.ctrlKey,
            };
            self.SCRIPT_ACT_SEL_SET(dat);
            // выделить скрипт
            let sel_script = self.SCRIPT_GET_ITEM_FIND_ACTIVE(dat.active_script_id)
            self.changeSelectedTreeViewItem(sel_script);
          });

          // подсказка
          if (self.MAP_GET_HINT) { set_feature_hint(layer, feature.properties); }

          // класс для стилей линий и полигонов
          let classes_str = get_feature_class(feature);
          // коррекция названий классов для избежания повторов из разных скриптов
          classes_str = correct_classes_name(classes_str, map_ind, feature[MAP_ITEM.FC.FEATURES.IND]);
          if ((classes_str != '') && (layer.setStyle)) { layer.setStyle({'className': classes_str, }); }

          // редактирование запрещено - удалить pm - для уменьшения объема вычислений
          if (layer.pm) { delete layer.pm; }
        }.bind(this),


        // стиль маркеров
        pointToLayer: function(feature, latlng) {
          // приоритет цвета в feature над цветом скрипта
          let color = feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.COLOR];
          if (color == undefined) color = self.SCRIPT_GET_ITEM_COLOR(map_ind);

          let class_main = feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS]??'';
          let class_sel  = feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES._SEL_]?MAP_CONST.CLASS.SEL:'';
          let class_dop  = 'upper-markers';                                                // поднять маркеры над фигурами-декораторами
          const classes  = {...feature.properties, 'class': class_main+' '+class_sel+' '+class_dop, };

          return marker_get(latlng, color, classes, self.MAP_GET_ZOOM);
        },


        // стиль фигур
        style: function(feature) {
          // приоритет цвета в feature над цветом скрипта
          let color = feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.COLOR];
          if (color == undefined) color = self.SCRIPT_GET_ITEM_COLOR(map_ind);

          let classSel = feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES._SEL_]?MAP_CONST.CLASS.SEL:'';
          return {
            weight:      2,
            opacity:     .5,
            color:       color,
            fillOpacity: .3,
            fillColor:   feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES._FILL_COLOR_],    // set in mixin: Color
            fillRule:    'evenodd',
            className:   classSel,
            // smoothFactor: 50,
            // noClip:       true,
          };
        },
      };
    },



    // ===============
    // СОБЫТИЯ
    // ===============
    on_map_ready() {
      this.map.invalidateSize();
      this.$refs.map.$el.focus(); // нужно ли при открытой панели?
    },

    on_map_resize() {
      this.map.invalidateSize();
    },

    on_map_zoom(val) {
      this.MAP_ACT_ZOOM(this.map.getZoom());
    },

    on_map_click(e) {
      this.SCRIPT_ACT_SEL_CLEAR();
      this.changeSelectedTreeViewItem();
    },

    on_map_dblclick(e) {
      this.addNotification({content: e.latlng, });
      // this.setNavigationDrawerStatus();
      // this.setActiveTool('dossierPage');
    },

    on_edit_ok(e, dat) {
      this.MAP_ACT_EDIT({data: dat});
    },

    // GET BUTTON
    btn_get_click(e) {
      console.log(this.getDataAsGeoJSON());
    },

    getDataAsGeoJSON () {
      // create FeatureCollection
      const geoJSON = {
        type:     'FeatureCollection',
        features: [],
      };

      // export each layer
      this.map.eachLayer(function (layer) {
        if (layer._leaflet_id && (layer instanceof L.Path || layer instanceof L.Marker)) {
          const geoJSONShape      = layer.toGeoJSON(16); // для точности
          geoJSONShape.properties = layer.properties;
          geoJSONShape.id         = layer._leaflet_id;
          geoJSON.features.push(geoJSONShape);
        }
      });

      return geoJSON;
    },


  }
};
</script>

<style scoped lang="scss">
  @import "~leaflet/dist/leaflet.css";
  @import "~leaflet.markercluster/dist/MarkerCluster.css";
  @import "~leaflet.markercluster/dist/MarkerCluster.Default.css";
  @import "~@/components/Map/Leaflet/Lib/Lib.css";
  @import "~@/components/Map/Leaflet/Components/Style/StyleIcon.css";
  @import "~@/components/Map/Leaflet/Mixins/Control.css";

  /* выделенный объект */
  div::v-deep .sel { animation: 1s ease 0s infinite normal none running pulse; }
  @keyframes pulse {
    0%   { opacity: 1;  }
    50%  { opacity: .4; }
    100% { opacity: 1;  }
  }

  /* маркеры выше */
  div::v-deep .upper-markers { z-index: 5000 !important; }
  div::v-deep div.upper-markers > svg { position: absolute; }  /* else bug on production */
</style>
