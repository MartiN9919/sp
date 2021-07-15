<template>
  <div style="height: 100%; width: 100%;">
    <l-map
      ref="map"
      style="height: 100%; z-index: 0;"
      :options="mapOptions"
      :crs="MAP_GET_TILES[MAP_GET_TILE].crs"
      @ready="on_map_ready"
      @resize="on_map_resize"
      @dblclick="on_map_dblclick"
      @contextmenu="menu_show"
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
            :geojson="data_normalize(map_ind)"
            :options="geojson_options(map_ind)"
          />
        </l-marker-cluster>
      </l-layer-group>


      <!-- РЕДАКТОР -->
      <Edit
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

    <Menu
      :options="menu_options()"
      @event_get="btn_get_click"
      @legend_hide="legend_hide"
    />
  </div>
</template>



<script>

import { mapGetters, mapActions, } from 'vuex';
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

import Vue2LeafletMarkerCluster     from 'vue2-leaflet-markercluster';
import LControlPolylineMeasure      from 'vue2-leaflet-polyline-measure';

import { MAP_ITEM }                 from '@/components/Map/Leaflet/Lib/Const';
import { marker_get }               from '@/components/Map/Leaflet/Markers/Fun';

import                      '@/components/Map/Leaflet/Markers/Pulse';
import Edit            from '@/components/Map/Leaflet/Components/Edit';
import Menu            from '@/components/Map/Leaflet/Components/Menu';
import Range           from '@/components/Map/Leaflet/Components/Range';
import Legend          from '@/components/Map/Leaflet/Components/Legend';
import Logo            from '@/components/Map/Leaflet/Components/Logo';
import MixKey          from '@/components/Map/Leaflet/Mixins/Key';
import MixFeatureColor from '@/components/Map/Leaflet/Mixins/FeatureColor';
import MixControl      from '@/components/Map/Leaflet/Mixins/Control';
import MixMeasure      from '@/components/Map/Leaflet/Mixins/Measure';

import { datesql_to_ts, } from '@/plugins/sys';

// устранение бага с путями
delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl:       require('leaflet/dist/images/marker-icon.png'),
  shadowUrl:     require('leaflet/dist/images/marker-shadow.png'),
});


export default {
  name: 'LeafletMain',


  mixins: [
    MixKey,
    MixFeatureColor,
    MixControl,
    MixMeasure,
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
    LControlPolylineMeasure,

    Edit,
    Menu,
    Range,
    Legend,
    Logo,
  },


  data() {
    return {
      menu: {
        visible: false,
        x:       0,
        y:       0,
      },

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
    this.key_mounted_after();
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
      'SCRIPT_GET_ITEM_MARKER',
      'SCRIPT_GET_ITEM_LINE',
      'SCRIPT_GET_ITEM_POLYGON',
      'SCRIPT_GET_ITEM_ICON',
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
      'appendErrorAlert',
    ]),

    // ===============
    // MENU
    // ===============
    menu_show(e) {
      e.originalEvent.preventDefault();
      e.originalEvent.stopPropagation();
      this.menu.visible = false;
      this.menu.x = e.originalEvent.clientX;
      this.menu.y = e.originalEvent.clientY;
      this.$nextTick(() => { this.menu.visible = true })
    },

    menu_options() {
      return {
        visible : this.menu.visible,
        x       : this.menu.x,
        y       : this.menu.y,
      }
    },


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
    data_normalize(map_ind) {
      // рассчитать цвета (легенда, цвет от значения в группе)
      this.data_normalize_color(map_ind);

      // deep copy
      let item = this.SCRIPT_GET_ITEM(map_ind);
      let fc   = item[MAP_ITEM.FC];
      fc = JSON.parse(JSON.stringify(fc));

      // установить fc.features[ind].ind - порядковый номер фигуры в fc
      for(let ind=0; ind<fc.features.length; ind++) { fc.features[ind].ind = ind; }

      // отфильтровать с допустимыми датами
      let range_ts  = this.MAP_GET_RANGE_SEL;
      if ((range_ts[0]>0) && (range_ts[1]>0)) {
        let item_date;
        let features = fc.features.filter(function(item) {
          if (!item.properties.date) return true;
          item_date = datesql_to_ts(item.properties.date);
          return ((item_date >= range_ts[0]) && (item_date <= range_ts[1]));
        });
        fc.features = features;
      }

      return fc;
    },

    cluster_options(map_ind) {
      return {
        // область при наведении курсора на кластер
        showCoverageOnHover: true,
        polygonOptions: { color: this.SCRIPT_GET_ITEM_COLOR(map_ind), },

        // для последующей коррекции цвета маркеров
        cluster_color: this.SCRIPT_GET_ITEM_COLOR(map_ind),

        // увеличение, при котором создавать кластеры
        disableClusteringAtZoom: this.MAP_GET_CLUSTER?17:0,

        // подмена иконки кластера
        iconCreateFunction: function (cluster) {
          return new L.DivIcon({
            html: '<div style="background-color:'+this.cluster_color+';"><span>' + cluster.getChildCount() + '</span></div>',
            className: 'marker-cluster marker-cluster-small marker-cluster-bg-new',
            iconSize: new L.Point(40, 40),
          });
        },

        // цвет региона сгруппированного кластера
        spiderLegPolylineOptions: { weight: 1.5, color: this.cluster_color, opacity: 0.5 },

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

          // подсказка
          if (self.MAP_GET_HINT && feature.properties.hint && feature.properties.hint!='') layer.bindTooltip(
            "<div>"+feature.properties.hint+"</div>",
            { permanent: false, sticky: true, }
          );

          // тип линии: бегущая пунктирная
          let line = self.SCRIPT_GET_ITEM_LINE(map_ind);
          if ((['LineString', ].indexOf(feature.geometry.type)>-1) && (line!=MAP_ITEM.LINE.DEFAULT)) {   // 'Polygon'
            layer.setStyle({'className': line, });
          }

          // редактирование запрещено - удалить pm - для уменьшения объема вычислений
          if (layer.pm) { delete layer.pm; }

          // тип полигона: color
          // let polygon = self.SCRIPT_GET_ITEM_POLYGON(map_ind);
          // if ((['Polygon', ].indexOf(feature.geometry.type)>-1) && (polygon!=POLYGON.DEFAULT)) {
          // }
        }.bind(this),


        // стиль маркеров
        pointToLayer: function(feature, latlng) {
          return marker_get(latlng, {
            name:  self.SCRIPT_GET_ITEM_MARKER(map_ind),
            color: self.SCRIPT_GET_ITEM_COLOR (map_ind),
            icon:  self.SCRIPT_GET_ITEM_ICON  (map_ind),
            // size:  self.SCRIPT_GET_ITEM_ICON(map_ind), не реализовано за ненадобностью
          });
        },


        // стиль фигур
        style: function(feature) {
          return {
            weight:      2,
            opacity:     .5,
            fillOpacity: .3,
            color:       self.SCRIPT_GET_ITEM_COLOR(map_ind),
            fillColor:   feature.color, // set in mixin
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

    on_map_dblclick(event) {
      this.appendErrorAlert({status: 501, content: event.latlng, show_time: 5, });
    },

    on_edit_ok(event, dat) {
      this.MAP_ACT_EDIT({data: dat});
    },


    // GET BUTTON
    btn_get_click(event) {
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
</style>
