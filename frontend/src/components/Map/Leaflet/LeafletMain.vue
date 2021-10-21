<template>
  <div
    style="height: 100%; width: 100%;"
    >

    <!-- ДЕКОРАТОР ФИГУР: SVG -->
    <l-decorator-svg/>

    <l-map
      ref="map"
      style="height: 100%; z-index: 0;"
      :options="mapOptions"
      :crs="MAP_GET_TILES[MAP_GET_TILE].crs"
      @ready="on_map_ready"
      @resize="on_map_resize"
      @click="on_map_click"
      @dblclick="on_map_dblclick"
      @contextmenu="on_menu_show"
    >

      <!-- ПОДЛОЖКА -->
      <l-tile-layer
        :url="MAP_GET_TILES[MAP_GET_TILE].url"
        :attribution="MAP_GET_TILES[MAP_GET_TILE].attr"
        :tms="MAP_GET_TILES[MAP_GET_TILE].tms"
      />


      <!-- ФИГУРЫ ИЗ state.map -->
      <l-layer-group
        v-for="(map_item, map_ind) in SCRIPT_GET"
        :key="MAP_GET_KEY(map_ind)"
      >
        <l-marker-cluster
          :options="cluster_options(map_ind)"
        >
          <l-geo-json
            ref="geoJson"
            :geojson="data_normalize(map_ind, map_item)"
            :options="geojson_options(map_ind)"
          />
        </l-marker-cluster>

        <!-- ДЕКОРАТОР ФИГУР: PATTERN -->
        <l-decorator-pattern
          :fc="data_normalize(map_ind, map_item)"
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
      <Range :options="range_options()"/>

      <!-- ЛЕГЕНДА -->
      <Legend :options="legend_options()"/>

      <!-- ЛОГОТИП -->
      <Logo/>

    </l-map>

    <KeyDialog
      ref="key_dialog"
      @ok="key_save_ok"
    />

    <contextMenuNested
      ref="menu"
      :form="form"
      :items="menu_struct"
    />

  </div>
</template>



<script>

import { mapGetters, mapActions, } from 'vuex';
import { Icon, } from 'leaflet';

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

import { MAP_ITEM }             from '@/components/Map/Leaflet/Lib/Const';
import {
  icon_ini,
  marker_get,
  icon_get_group,
} from '@/components/Map/Leaflet/Markers/Fun';

import DecoratorSvg     from '@/components/Map/Leaflet/Components/DecoratorSvg';
import DecoratorPattern from '@/components/Map/Leaflet/Components/DecoratorPattern';
import                       '@/components/Map/Leaflet/Markers/Pulse';
import EditorMap        from '@/components/Map/Leaflet/Components/EditorMap';
import Range            from '@/components/Map/Leaflet/Components/Range';
import Legend           from '@/components/Map/Leaflet/Components/Legend';
import Logo             from '@/components/Map/Leaflet/Components/Logo';
import MixResize        from '@/components/Map/Leaflet/Mixins/Resize';
import MixKey           from '@/components/Map/Leaflet/Mixins/Key';
import MixColor         from '@/components/Map/Leaflet/Mixins/Color';
import MixControl       from '@/components/Map/Leaflet/Mixins/Control';
import MixMeasure       from '@/components/Map/Leaflet/Mixins/Measure';
import MixMenu          from '@/components/Map/Leaflet/Mixins/Menu';


import { datesql_to_ts, } from '@/plugins/sys';


// устранение бага с путями
icon_ini();


export default {
  name: 'LeafletMain',

  mixins: [
    MixResize,
    MixKey,
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
    'l-marker-cluster':    Vue2LeafletMarkerCluster,
    'l-decorator-svg':     DecoratorSvg,
    'l-decorator-pattern': DecoratorPattern,
    LControlPolylineMeasure,

    EditorMap,
    Range,
    Legend,
    Logo,
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

    // добавить обработчики событий клавиатуры
    this.mounted_after_key();
  },


  computed: {
    ...mapGetters([
      'MAP_GET_KEY',
      'MAP_GET_RANGE_SEL',
      'MAP_GET_TILES',
      'MAP_GET_TILE',
      'MAP_GET_SCALE',
      'MAP_GET_MEASURE',
      'MAP_GET_CLUSTER',
      'MAP_GET_HINT',

      'MAP_GET_EDIT',

      'SCRIPT_GET',
      'SCRIPT_GET_ITEM_COLOR',
      'SCRIPT_GET_ITEM_FC_STYLE',
      'SCRIPT_GET_ITEM_FC_STYLE_LINE',
      'SCRIPT_GET_ITEM_FC_STYLE_POLYGON',
      'SCRIPT_GET_ITEM_SEL',
    ]),

    // FeatureCollection РЕДАКТИРУЕМЫХ объектов
    fc_edit: {
      get()    { return this.MAP_GET_EDIT; },
      set(val) { /* this.MAP_ACT_EDIT({data: val}); */ },
    },
  },


  methods: {
    ...mapActions([
      'MAP_ACT_EDIT',
      'SCRIPT_ACT_SEL_SET',
      'SCRIPT_ACT_SEL_CLEAR',
      'appendErrorAlert',
      'setNavigationDrawerStatus',
      'setActiveTool',
    ]),


    // ===============
    // RANGE
    // ===============
    range_options() {
      return { }
    },


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
      let fc = map_item[MAP_ITEM.FC.KEY];
      fc = JSON.parse(JSON.stringify(fc));

      // установить fc.features[ind].ind - порядковый номер фигуры в fc
      for(let ind=0; ind<fc.features.length; ind++) { fc.features[ind].ind = ind; }

      // отфильтровать с допустимыми датами
      let range_ts  = this.MAP_GET_RANGE_SEL;
      if ((range_ts[0]>0) && (range_ts[1]>0)) {
        let item_date;
        let features = fc.features.filter(function(map_item) {
          if (!map_item.properties.date) return true;
          item_date = datesql_to_ts(map_item.properties.date);
          return ((item_date >= range_ts[0]) && (item_date <= range_ts[1]));
        });
        fc.features = features;
      }

      // console.log(this.$refs.geoJson)
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
          return icon_get_group(color, cluster.getChildCount());
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
          layer.on('mouseover', function(e) { self.hover_map_ind = map_ind;  self.hover_feature_ind = feature.ind; });
          layer.on('mouseout',  function(e) {
            if (!e.originalEvent.ctrlKey) self.hover_map_ind = -1;
            self.hover_feature_ind = -1;
          });
          layer.on('click', function(e) {
            // реакция выделения только на объекты из БД
            if ((!e.target.feature.obj_id) || (!e.target.feature.rec_id)) return;
            L.DomEvent.stopPropagation(e);
            let dat = {
              obj_id: e.target.feature.obj_id,
              rec_id: e.target.feature.rec_id,
              ctrl:   e.originalEvent.ctrlKey,
            };
            self.SCRIPT_ACT_SEL_SET(dat);
          });

          // подсказка
          if (self.MAP_GET_HINT && feature.properties.hint && feature.properties.hint!='') layer.bindTooltip(
            "<div>"+feature.properties.hint+"</div>",
            { permanent: false, sticky: true, }
          );

          // класс для стилей линий и полигонов
          let style = {};
          if (feature.geometry.type == MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.LINE)    { style = self.SCRIPT_GET_ITEM_FC_STYLE_LINE   (map_ind); }
          if (feature.geometry.type == MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.POLYGON) { style = self.SCRIPT_GET_ITEM_FC_STYLE_POLYGON(map_ind); }
          let className = style[MAP_ITEM.FC.STYLE.LINE.CLASS.KEY] ?? '';
          if (className != '') { layer.setStyle({'className': className, }); }

          // редактирование запрещено - удалить pm - для уменьшения объема вычислений
          if (layer.pm) { delete layer.pm; }
        }.bind(this),


        // стиль маркеров
        pointToLayer: function(feature, latlng) {
          let className = (feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES._SEL_]?'sel':'');
          let layer = marker_get(latlng, self.SCRIPT_GET_ITEM_FC_STYLE (map_ind), className);
          return layer;
        },


        // стиль фигур
        style: function(feature) {
          return {
            weight:      2,
            opacity:     .5,
            color:       self.SCRIPT_GET_ITEM_COLOR(map_ind),
            fillOpacity: .3,
            fillColor:   feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES._COLOR_],    // set in mixin: Color
            fillRule:    'evenodd',
            className:   (feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES._SEL_  ]?'sel':''),
          };
        },
      };
    },



    // ===============
    // СОБЫТИЯ
    // ===============
    on_map_ready() {
      this.map.invalidateSize();
    },

    on_map_resize() {
      this.map.invalidateSize();
    },

    on_map_click(e) {
      this.SCRIPT_ACT_SEL_CLEAR();
    },

    on_map_dblclick(e) {
      this.appendErrorAlert({status: 501, content: e.latlng, show_time: 5, });
      this.setNavigationDrawerStatus();
      this.setActiveTool('dossierPage');
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
        type: 'FeatureCollection',
        features: []
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

<style>
  .leaflet-center {
    left: 50%;
    transform: translate(-50%, 0%);
  }
  .polyline-measure-tooltip-difference {
    color: #060;
    font-style: normal!important;
  }

  /*** кнопка ***/
  .polyline-measure-unicode-icon {
    color: rgba(0, 0, 0, 0.54)!important;
  }
  .polyline-measure-controlOnBgColor {
    color: red!important;
  }
</style>

<style scoped lang="scss">
  @import "~leaflet/dist/leaflet.css";
  @import "~leaflet.markercluster/dist/MarkerCluster.css";
  @import "~leaflet.markercluster/dist/MarkerCluster.Default.css";

  @import "~@/components/Map/Leaflet/Lib/Lib.css";

  @import "~@/components/Map/Leaflet/Markers/Cluster.css";
  @import "~@/components/Map/Leaflet/Markers/Pulse.css";
  @import "~@/components/Map/Leaflet/Markers/Font.css";

  @import "~@/components/Map/Leaflet/Mixins/Control.css";

  div::v-deep .sel { animation: 1s ease 0s infinite normal none running pulse; }
  @keyframes pulse {
    0%   { opacity: 1;  }
    50%  { opacity: .4; }
    100% { opacity: 1;  }
  }

</style>
