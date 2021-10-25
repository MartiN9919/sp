<template>
  <div v-if="ready" style="display: none;">
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

import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { get_feature_class, get_feature_coordinates } from '@/components/Map/Leaflet/Lib/LibFc';
import { dict_get } from '@/components/Map/Leaflet/Lib/Lib';
import { DATA_PATTERN } from '@/components/Map/Leaflet/Components/StylePatternData';
//import { DECORATOR_CLASSES } from '@/components/Map/Leaflet/Components/DecoratorClasses';
//import { icon_path } from '@/components/Map/Leaflet/Markers/StyleIcon';

import { findRealParent, propsBinder } from 'vue2-leaflet';


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
  name: 'LStylePattern',
  props,
  data() {
    return {
      ready: true, //false,
      decorators: [],
    }
  },
  mounted() {
    // // test
    // const test = new DECORATOR_CLASSES(color);
    // var   dd = test.get_patterns('mark_zabor_ograd line_border_1');
    // debugger


    const self         = this;
    const features     = this.fc[MAP_ITEM.FC.FEATURES.KEY];
    const color        = dict_get(this.fc, [MAP_ITEM.FC.STYLE.KEY, MAP_ITEM.FC.STYLE._COLOR_.KEY], 'gray');
    const obj_pattern  = new DATA_PATTERN(color);
    this.parent_obj    = findRealParent(this.$parent);

    this.ready = true;

    for(let ind=0; ind<features.length; ind++) {
      let feature       = features[ind];
      let geometry      = feature[MAP_ITEM.FC.FEATURES.GEOMETRY.KEY];
      let geometry_type = geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.KEY];

      // L.объекты
      let l_obj         = get_feature_coordinates(feature, true);
      l_obj[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.LINE   ] = l_obj[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.LINE   ].map((val) => L.polyline(val));
      l_obj[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.POLYGON] = l_obj[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.POLYGON].map((val) => L.polygon (val));

      // patterns на основании classes и color
      let classes = get_feature_class(feature);
      let patterns = obj_pattern.get(classes);
      if (patterns.length == 0) continue;

      // создать декорации
      function set_decorator(objects) {
        if (objects.length == 0) return;
        const decorator = L.polylineDecorator(objects, { patterns: patterns, });
        self.decorators.push(decorator);
        L.DomEvent.on(decorator, self.$listeners);
        propsBinder(self, decorator, props);
        self.parent_obj.mapObject.addLayer(decorator, !self.visible);
      }
      set_decorator(l_obj[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.POLYGON]);
      set_decorator(l_obj[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.LINE   ]);
    }
  },

  beforeDestroy() {
    for(let i=0; i<this.decorators.length; i++) {
      this.parent_obj.mapObject.removeLayer(this.decorators[i]);
    }
  },

  methods: {
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
