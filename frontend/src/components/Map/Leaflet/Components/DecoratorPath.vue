<template>
  <div style="display: none;">
    <slot v-if="ready"></slot>
  </div>
</template>

<script>
/*
 *  =====================================================
 *     ДЕКОРАТОР: НАЛОЖЕНИЕ НА ФИГУРУ ОТДЕЛЬНОГО СЛОЯ
 *  =====================================================
 *
 */

import 'leaflet-polylinedecorator'

import { MAP_ITEM }   from '@/components/Map/Leaflet/Lib/Const';
import { CONST_PATH } from '@/components/Map/Leaflet/Components/DecoratorPathConst';
import { findRealParent, propsBinder } from 'vue2-leaflet';
import { dict_get } from '@/components/Map/Leaflet/Lib/Lib';

const props = {
  fc: {
    type: Object,
    default: () => {},
  },
  visible: {
    type: Boolean,
    custom: true,
    default: true,
  }
};

export default {
  name: 'LDecoratorPath',
  props,
  data() {
    return {
      ready: false,
      objects: {                      // список объектов
        line: [],
        polygon: [],
      },
    }
  },
  mounted() {
    const features = this.fc[MAP_ITEM.FC.FEATURES.KEY];
    for(let ind=0; ind<features.length; ind++) {
      let feature       = features[ind];
      let geometry      = feature[MAP_ITEM.FC.FEATURES.GEOMETRY.KEY];
      let geometry_type = geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.KEY];

      // GeometryCollection: вложенные геометрии
      if (geometry_type == MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.GC) {
        for(let i=0; i<geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.GEOMETRIES.KEY].length; i++) {
          this.add_obj(geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.GEOMETRIES.KEY][i]);
        }
      } else { this.add_obj(geometry); }
    }

    const color   = dict_get(this.fc, [MAP_ITEM.FC.STYLE.KEY, MAP_ITEM.FC.STYLE._COLOR_.KEY], 'gray');
    const pattern = {
      line:    dict_get(this.fc, [MAP_ITEM.FC.STYLE.KEY, MAP_ITEM.FC.STYLE.LINE   .KEY, MAP_ITEM.FC.STYLE.LINE   .CLASS.KEY], ''),
      polygon: dict_get(this.fc, [MAP_ITEM.FC.STYLE.KEY, MAP_ITEM.FC.STYLE.POLYGON.KEY, MAP_ITEM.FC.STYLE.POLYGON.CLASS.KEY], ''),
    };
    let path               = new CONST_PATH(color);
    this.mapObject_line    = L.polylineDecorator(this.objects.line,    { patterns: path.get(pattern.line   ) });
    this.mapObject_polygon = L.polylineDecorator(this.objects.polygon, { patterns: path.get(pattern.polygon) });
    this.mapObject         = this.mapObject_line;

    L.DomEvent.on(this.mapObject, this.$listeners);
    propsBinder(this, this.mapObject, props);

    this.parentContainer = findRealParent(this.$parent);
    this.parentContainer.addLayer(this, !this.visible);
    this.ready = true;
  },

  beforeDestroy() {
    this.parentContainer.removeLayer(this);
  },

  methods: {
    add_obj(geometry) {
      let geometry_type = geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.KEY];
      if ([MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.LINE, MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.POLYGON].indexOf(geometry_type)<0) return;
      let geometry_coordinates = geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.COORDINATES.KEY];

      if (geometry_type == MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.LINE) {                                   // для линий [[x,y],...]
        geometry_coordinates = geometry_coordinates.map((val) => { return [val[1], val[0]] });          // поменять местами x y
        this.objects.line.push(L.polyline(geometry_coordinates));
      }
      if (geometry_type == MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.POLYGON) {                                // для полигонов [[[x,y],...],...]
        for(let i=0; i<geometry_coordinates.length;i++) {                                               // поменять местами x y
          geometry_coordinates[i] = geometry_coordinates[i].map((val) => { return [val[1], val[0]] });
        }
        this.objects.polygon.push(L.polygon(geometry_coordinates));
      }
    },



    // БЫЛО В ИСХОДНОМ КОДЕ
    setVisible(newVal, oldVal) {
      if (newVal == oldVal) return;
      if (newVal) {
        this.parentContainer.addLayer(this);
      } else {
        this.parentContainer.removeLayer(this);
      }
    },
    addLatLng(value) {
      this.mapObject.addLatLng(value);
    },
  }
};
</script>
