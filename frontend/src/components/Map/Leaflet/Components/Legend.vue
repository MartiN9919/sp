<template>
  <l-control
    v-if="(MAP_GET_LEGEND && (options.hover_map_ind>-1))"
    v-show="visible()"
    class="legend select_off pre-formatted"
    position="topright"
  >
    <div
      class="legend_top"
    >
      {{prop_hint()}}
    </div>
    <div
      class="legend_top legend-color-select"
    >
      {{prop_val()}}
    </div>
    <div
      v-for="(legend_color_item, legend_color_ind) in SCRIPT_GET_ITEM_LEGEND_COLOR(options.hover_map_ind)"
      class="legend-color"
    >
      <div
        :key="'control_color_'+options.hover_map_ind+'_'+options.hover_feature_ind"
      >
        <i :style="{ background: legend_color_item.color }"/>
        <span
          :class="class_select(legend_color_item)"
        >{{legend_color_item.from}}{{legend_color_item.to}}</span>
      </div>
    </div>
  </l-control>
</template>


<script>
// https://leafletjs.com/examples/choropleth/

import {
  mapGetters,
} from 'vuex';

import {
  LControl,
} from "vue2-leaflet";

import {
  MAP_ITEM,
} from '@/components/Map/Leaflet/Lib/Const';


const props = {
  options: {
    type: Object,
    default() { return {}; },
  },
};


export default {
  name: 'Legend',

  props,

  components: {
    LControl,
  },

  data: () => ({
    block_hint:  false,   // присутствует ли блок подсказки
    block_value: false,   // присутствует ли блок значения
    //block_color: false, // присутствует ли блок с цветовым диапазоном
  }),

  computed: {
    ...mapGetters([
      'SCRIPT_GET_ITEM',
      'SCRIPT_GET_ITEM_LEGEND_COLOR',
      'MAP_GET_LEGEND',
    ]),
  },

  methods: {
    visible() {
      let block_color = (this.SCRIPT_GET_ITEM_LEGEND_COLOR(this.options.hover_map_ind).length>0);
      let ret = (this.block_hint || this.block_value || block_color)
      return ret;
    },

    prop_hint() {
      let ret;
      if ((this.options.hover_map_ind>-1) && (this.options.hover_feature_ind>-1))
        ret = this.SCRIPT_GET_ITEM(this.options.hover_map_ind)
          .fc
          .features[this.options.hover_feature_ind]
          .properties[MAP_ITEM.FC.FEATURES.PROPERTIES.HINT];
      this.block_hint = (ret)?true:false;
      return ret
    },
    prop_val() {
      let ret;
      if ((this.options.hover_map_ind>-1) && (this.options.hover_feature_ind>-1))
        ret = this.SCRIPT_GET_ITEM(this.options.hover_map_ind)
          .fc
          .features[this.options.hover_feature_ind]
          .properties[MAP_ITEM.FC.FEATURES.PROPERTIES.VALUE];
      this.block_value = (ret)?true:false;
      return ret
    },

    // нужен ли класс - выделение пункта легенды color_dif
    class_select(legend_color_item) {
      // цвет фигуры
      let feature_color =
        ((this.options.hover_map_ind>-1) && (this.options.hover_feature_ind>-1))?
        this.SCRIPT_GET_ITEM(this.options.hover_map_ind)
          .fc
          .features[this.options.hover_feature_ind]
          .properties[MAP_ITEM.FC.FEATURES.PROPERTIES._COLOR_]:
        undefined;
      return {
        // выделить совпадение цвета фигуры и пункта легенды
        'legend-color-select': (feature_color==legend_color_item.color),
      }
    },
  },
}
</script>



<style scoped lang="scss">

  .legend {
    background: #fff;
    padding: 0.5em;
    border: 1px solid #aaa;
    border-radius: 0.3em;
    box-shadow: 0 0 15px rgb(0 0 0 / 20%);
    opacity: 0.9;
  }

  .legend_top {
    max-width: 10em;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }

  .legend-color i {
    width: 18px;
    height: 18px;
    float: left;
    margin-right: 8px;
    opacity: 0.6;
  }

  .legend-color-select {
    color: blue;
    font-weight: bold;
    background: #eee;
  }

  .pre-formatted {
    white-space: pre;
    text-overflow: ellipsis;
  }

</style>
