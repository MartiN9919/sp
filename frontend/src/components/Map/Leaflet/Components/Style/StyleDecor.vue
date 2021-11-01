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

import { MAP_CONST, MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { get_feature_class, get_feature_coordinates } from '@/components/Map/Leaflet/Lib/LibFc';
import { dict_get } from '@/components/Map/Leaflet/Lib/Lib';
import { DATA_DECOR } from '@/components/Map/Leaflet/Components/Style/StyleDecorData';
//import { icon_file_path } from '@/components/Map/Leaflet/Components/Style/StyleIcon';

import { findRealParent, propsBinder } from 'vue2-leaflet';


const props = {
  fc: {
    type: Object,
    default: () => {},
  },
  color: {
    type: String,
    default: () => MAP_CONST.COLOR.DEFAULT_STYLE_PATH,
  },
  visible: {
    type: Boolean,
    custom: true,
    default: true,
  }
};

export default {
  name: 'LStyleDecor',
  props,
  data() {
    return {
      ready: true, //false,
      decorators: [],
    }
  },
  mounted() {
    const self        = this;
    const features    = this.fc.features;
    const obj_pattern = new DATA_DECOR(this.color);
    this.parent_obj   = findRealParent(this.$parent);

    this.ready = true;

    for(let ind=0; ind<features.length; ind++) {
      let feature       = features[ind];
      let geometry      = feature.geometry;
      let geometry_type = geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE];

      // L.объекты
      let l_obj         = get_feature_coordinates(feature, true);
      l_obj[MAP_CONST.TYPE_GEOMETRY.LINE   ] = l_obj[MAP_CONST.TYPE_GEOMETRY.LINE   ].map((val) => L.polyline(val));
      l_obj[MAP_CONST.TYPE_GEOMETRY.POLYGON] = l_obj[MAP_CONST.TYPE_GEOMETRY.POLYGON].map((val) => L.polygon (val));

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
      set_decorator(l_obj[MAP_CONST.TYPE_GEOMETRY.POLYGON]);
      set_decorator(l_obj[MAP_CONST.TYPE_GEOMETRY.LINE   ]);
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
