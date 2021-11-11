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
import { findRealParent, propsBinder } from 'vue2-leaflet';

import { MAP_CONST, MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { dict_get } from '@/components/Map/Leaflet/Lib/Lib';
import { get_feature_class, get_feature_coordinates, set_feature_hint } from '@/components/Map/Leaflet/Lib/LibFc';
import { get_style_data_decor } from '@/components/Map/Leaflet/Components/Style/StyleData';


const props = {
  fc: {
    type: Object,
    default: () => {},
  },
  color: {                  // цвет скрипта, цвет фигуры имеет приоритет над цветом скрипта
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
    const self      = this;
    const features  = this.fc.features;
    this.parent_obj = findRealParent(this.$parent);

    this.ready = true;

    for(let ind=0; ind<features.length; ind++) {
      let feature         = features[ind];
      let geometry        = feature.geometry;
      let geometry_type   = geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE];
      let color           = feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.COLOR];
      if (color == undefined) { color = this.color; }           // приоритет цвета фигуры над цветом скрипта
      let icon_properties = {                                   // распространяем свойства фигуры на декорации
      //[MAP_ITEM.FC.FEATURES.PROPERTIES.DATE  ]: feature.properties?.[MAP_ITEM.FC.FEATURES.PROPERTIES.DATE  ],
      //[MAP_ITEM.FC.FEATURES.PROPERTIES.HINT  ]: feature.properties?.[MAP_ITEM.FC.FEATURES.PROPERTIES.HINT  ],
        [MAP_ITEM.FC.FEATURES.PROPERTIES.TEXT  ]: feature.properties?.[MAP_ITEM.FC.FEATURES.PROPERTIES.TEXT  ],
        [MAP_ITEM.FC.FEATURES.PROPERTIES.SHADOW]: feature.properties?.[MAP_ITEM.FC.FEATURES.PROPERTIES.SHADOW],
      };

      // L.объекты
      let l_obj = get_feature_coordinates(feature, true);
      l_obj[MAP_CONST.TYPE_GEOMETRY.LINE   ] = l_obj[MAP_CONST.TYPE_GEOMETRY.LINE   ].map((val) => L.polyline(val));
      l_obj[MAP_CONST.TYPE_GEOMETRY.POLYGON] = l_obj[MAP_CONST.TYPE_GEOMETRY.POLYGON].map((val) => L.polygon (val));

      // patterns на основании classes_str и color
      let patterns    = get_style_data_decor({
        classes_str:     get_feature_class(feature),
        color:           color,
        icon_properties: icon_properties,
      });
      if (patterns.length == 0) continue;

      // создать декорации
      function set_decorator(objects) {
        if (objects.length == 0) return;
        const layer_decor = L.polylineDecorator(objects, { patterns: patterns, });

        set_feature_hint(layer_decor, feature.properties, true);

        self.decorators.push(layer_decor);
        L.DomEvent.on(layer_decor, self.$listeners);
        propsBinder(self, layer_decor, props);
        self.parent_obj.mapObject.addLayer(layer_decor, !self.visible);
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
