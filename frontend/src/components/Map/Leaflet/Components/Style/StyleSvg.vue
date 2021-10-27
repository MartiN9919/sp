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
import { fc_properties_keys_get } from '@/components/Map/Leaflet/Lib/LibFc'
import { data_svg }               from '@/components/Map/Leaflet/Components/Style/StyleSvgData';

export default {
  name: 'LStyleSvg',

  // beforeDestroy: function() {
  //   this.$refs.defs .innerHTML = '';
  //   this.$refs.style.innerHTML = '';
  // },

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
      for(let ind=0; ind<items.length; ind++) {
        let item    = items[ind];
        let color   = item[MAP_ITEM.COLOR] ?? MAP_CONST.COLOR.DEFAULT_STYLE_PATH;
        let classes = fc_properties_keys_get(item.fc, MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS);  // список fc.features[i].properties.class
        let data    = data_svg(classes.join(' '), ind, color);
        if (data.style!='') style += data.style;
        if (data.defs !='') defs  += data.defs;
      }
      this.$refs.defs .innerHTML = defs;
      this.$refs.style.innerHTML = style;
    },
  },

}

</script>
