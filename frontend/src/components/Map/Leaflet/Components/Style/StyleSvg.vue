<template>
  <div>
    <svg
      id="map-svg-defs"
      xmlns="http://www.w3.org/2000/svg"
      preserveAspectRatio="none"
      width="0"
      height="0"
    >
      <defs ref="defs"/>
    </svg>
    <div is="style"
      id="map-svg-style"
      ref="style"
    ></div>
  </div>
</template>

<script>
/*
 *  ============================================================
 *     ДЕКОРАТОР: СТРИЛИЗАЦИЯ SVG
 *  ============================================================
 *
 */

import { mapGetters }             from 'vuex';
import { MAP_CONST, MAP_ITEM }    from '@/components/Map/Leaflet/Lib/Const';
import { data_svg }               from '@/components/Map/Leaflet/Components/Style/StyleSvgData';

export default {
  name: 'LStyleSvg',

  beforeDestroy: function() {
    this.$refs.defs .innerHTML = '';
    this.$refs.style.innerHTML = '';
  },

  watch: {
    SCRIPT_GET: {
      handler: function(val) { this.svg_refresh(val); },
      deep: true,
    },
  },

  computed: {
    ...mapGetters(['SCRIPT_GET']),
  },

  methods: {
    svg_refresh(items) {
      // сформировать defs и style
      let style = '';
      let defs = '';
      for(let items_ind=0; items_ind<items.length; items_ind++) {
        let item    = items[items_ind];
        for(let features_ind=0; features_ind<item.fc.features.length; features_ind++) {
          let properties = item.fc.features[features_ind].properties;
          let color =                                                             // цвет, приоритет fc.features[i].prop.color перед цветом скрипта
            ( properties[MAP_ITEM.FC.FEATURES.PROPERTIES.COLOR] != undefined) ?
              properties[MAP_ITEM.FC.FEATURES.PROPERTIES.COLOR] :
            ((item[MAP_ITEM.COLOR] ?? MAP_CONST.COLOR.DEFAULT_STYLE_PATH).toLowerCase());
          let classes = properties[MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS] ?? '';  // список fc.features[i].properties.class
          let data    = data_svg(classes, items_ind, color);
          if (data.style!='') style += data.style;
          if (data.defs !='') defs  += data.defs;
        }
      }
      this.$refs.defs .innerHTML = defs;
      this.$refs.style.innerHTML = style;
    },
  },

}

</script>
