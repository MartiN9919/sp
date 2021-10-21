<template>
  <div v-if="ready" style="display: none;">
    <div ref="dpline"/>
    <div ref="dppolygon"/>
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
import { CONST_PATTERN } from '@/components/Map/Leaflet/Components/DecoratorPatternConst';
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
  name: 'LDecoratorPattern',
  props,
  data() {
    return {
      ready: true, //false,
      objects: {                      // список объектов
        line: [],
        polygon: [],
      },
      pl: {
        line: undefined,
        polygon: undefined,
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

    // из свойств fc: цвет и классы шаблонов фигур
    const color   = dict_get(this.fc, [MAP_ITEM.FC.STYLE.KEY, MAP_ITEM.FC.STYLE._COLOR_.KEY], 'gray');
    const classes = {
      line:    dict_get(this.fc, [MAP_ITEM.FC.STYLE.KEY, MAP_ITEM.FC.STYLE.LINE   .KEY, MAP_ITEM.FC.STYLE.LINE   .CLASS.KEY], ''),
      polygon: dict_get(this.fc, [MAP_ITEM.FC.STYLE.KEY, MAP_ITEM.FC.STYLE.POLYGON.KEY, MAP_ITEM.FC.STYLE.POLYGON.CLASS.KEY], ''),
    };

    // классы шаблонов в шаблоны с учетом цвета
    const pattern_obj     = new CONST_PATTERN(color);
    const pattern_line    = pattern_obj.get(classes.line   );
    const pattern_polygon = pattern_obj.get(classes.polygon);

    this.parentContainer  = findRealParent(this.$parent);

    // должен быть видимым
    this.ready = true;

    // декорация линий
    if (pattern_line.length > 0) {
      this.pl.line = this.$refs.dpline;
      this.pl.line.mapObject = L.polylineDecorator(this.objects.line, { patterns: pattern_line, });
      L.DomEvent.on(this.pl.line.mapObject, this.$listeners);
      propsBinder(this, this.pl.line.mapObject, props);
      this.parentContainer.addLayer(this.pl.line, !this.visible);
    }

    // декорация полигонов
    if (pattern_polygon.length > 0) {
      this.pl.polygon = this.$refs.dppolygon;
      this.pl.polygon.mapObject = L.polylineDecorator(this.objects.polygon, { patterns: pattern_polygon, });
      L.DomEvent.on(this.pl.polygon.mapObject, this.$listeners);
      propsBinder(this, this.pl.polygon.mapObject, props);
      this.parentContainer.addLayer(this.pl.polygon, !this.visible);
    }

    this.$nextTick(() => {
      this.$emit('ready', this.mapObject);
    });
  },

  beforeDestroy() {
    if (this.pl.line)    this.parentContainer.removeLayer(this.pl.line);
    if (this.pl.polygon) this.parentContainer.removeLayer(this.pl.polygon);
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
