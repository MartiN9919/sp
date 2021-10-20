<template>
  <div class="drd">
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

import { mapGetters } from 'vuex';
import { MAP_ITEM }   from '@/components/Map/Leaflet/Lib/Const';
import { dict_get }   from '@/components/Map/Leaflet/Lib/Lib';
import { CONST_SVG }  from '@/components/Map/Leaflet/Components/DecoratorSvgConst';

export default {
  name: 'LDecoratorSvg',

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
      // сформировать тексты defs и style
      let style = '';
      let defs = '';
      for(let ind=0; ind<items.length; ind++) {
        let item = items[ind];

        // с шины: списки классов и цвет
        let item_color   = dict_get(item, [MAP_ITEM.COLOR.KEY], 'gray');
        let item_classes =
          (
            dict_get(item, [MAP_ITEM.FC.KEY, MAP_ITEM.FC.STYLE.KEY, MAP_ITEM.FC.STYLE.LINE.KEY,    MAP_ITEM.FC.STYLE.LINE.CLASS.KEY],    '')+' '+
            dict_get(item, [MAP_ITEM.FC.KEY, MAP_ITEM.FC.STYLE.KEY, MAP_ITEM.FC.STYLE.POLYGON.KEY, MAP_ITEM.FC.STYLE.POLYGON.CLASS.KEY], '')
          ).trim().replace(/\s+/g, ' ').split(' ');

        // перебрать классы
        item_classes.forEach(function(item_class, ind_class) {
          // для класса: стиль и defs
          let svg = CONST_SVG.LIST[item_class];
          if (!svg) return;
          let svg_style = svg[CONST_SVG.KEY_STYLE];
          let svg_defs  = svg[CONST_SVG.KEY_DEFS ];

          // уникальный id
          let id = 'svg_'+ind+'_'+ind_class;

          // заменить переменные
          if (svg_style) {
            svg_style = svg_style.replace(/{id}/g, id).replace(/{color}/g, item_color);
            style    += '.'+item_class+' { '+svg_style+' }\n';
          }

          if (svg_defs ) {
            svg_defs  = svg_defs.replace(/{id}/g, id).replace(/{color}/g, item_color);
            defs  += svg_defs+'\n';
          }
        });
      }

      this.$refs.defs .innerHTML = defs;
      this.$refs.style.innerHTML = style;
    },
  },

}

</script>
