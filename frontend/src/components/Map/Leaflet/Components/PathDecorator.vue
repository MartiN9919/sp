<template>
  <div style="display: none;">
    <slot v-if="ready"></slot>
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet-polylinedecorator'

import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { findRealParent, propsBinder } from 'vue2-leaflet'
//import { fc_types_del, } from '@/components/Map/Leaflet/Lib/LibFc';

const props = {
  fc: {
    type: Object,
    default: () => {},
  },
  paths: {
    type: Array,
    custom: true,
    default: () => [],
  },
  patterns: {
    type: Array,
    custom: true,
    default: () => [],
  },
  visible: {
    type: Boolean,
    custom: true,
    default: true,
  }
};

export default {
  name: 'LPathDecorator',
  props,
  data() {
    return {
      ready: false,
    }
  },
  mounted() {
    let features = this.fc[MAP_ITEM.FC.FEATURES.KEY];
    let objects  = [];                                                                                  // список объектов
    for(let ind=0; ind<features.length; ind++) {
      let feature       = features[ind];
      let geometry      = feature[MAP_ITEM.FC.FEATURES.GEOMETRY.KEY];
      let geometry_type = geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.KEY];
      if ([MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.LINE, MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.POLYGON].indexOf(geometry_type)<0) continue;
      let geometry_coordinates = geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.COORDINATES.KEY];

      if (geometry_type == MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.LINE) {                                   // для линий [[x,y],...]
        geometry_coordinates = geometry_coordinates.map((val) => { return [val[1], val[0]] });          // поменять местами x y
        objects.push(L.polyline(geometry_coordinates));
      }
      if (geometry_type == MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.POLYGON) {                                // для полигонов [[[x,y],...],...]
        for(let i=0; i<geometry_coordinates.length;i++) {                                               // поменять местами x y
          geometry_coordinates[i] = geometry_coordinates[i].map((val) => { return [val[1], val[0]] });
        }
        objects.push(L.polygon(geometry_coordinates));
      }
    }

    const options = { patterns: this.patterns };
    this.mapObject = L.polylineDecorator(objects, options);

    L.DomEvent.on(this.mapObject, this.$listeners);
    propsBinder(this, this.mapObject, props);

    this.ready = true;
    this.parentContainer = findRealParent(this.$parent);
    this.parentContainer.addLayer(this, !this.visible);
  },

  beforeDestroy() {
    this.parentContainer.removeLayer(this);
  },

  methods: {
    // setVisible(newVal, oldVal) {
    //   if (newVal == oldVal) return;
    //   if (newVal) {
    //     this.parentContainer.addLayer(this);
    //   } else {
    //     this.parentContainer.removeLayer(this);
    //   }
    // },
    // addLatLng(value) {
    //   this.mapObject.addLatLng(value);
    // },
  }
};
</script>
