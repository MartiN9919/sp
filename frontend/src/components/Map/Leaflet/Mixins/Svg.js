import { mapGetters } from 'vuex';
import { dict_get } from '@/components/Map/Leaflet/Lib/Lib';
import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { MAP_SVG } from '@/components/Map/Leaflet/Mixins/Svg.const';

export default {
  data: () => ({ }),

  mounted: function() { },

  beforeDestroy: function() {
    this.svg_remove();
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
    // вызывать из родительского mounted
    mounted_after_svg() {
    },

    svg_refresh(items) {
      this.svg_remove();
      if (items.length == 0) return;

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
          let svg = MAP_SVG.DAT.VAL[item_class];
          if (!svg) return;
          let svg_style = svg[MAP_SVG.DAT.KEY_STYLE];
          let svg_defs  = svg[MAP_SVG.DAT.KEY_DEFS ];

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

        let el;
        if (style!='') {
          style = MAP_SVG.STYLE.PREFIX+style+MAP_SVG.STYLE.POSTFIX;
          el = document.createElement('style'); document.body.prepend(el); el.outerHTML = style;
        }
        if (defs!='') {
          defs = MAP_SVG.DEFS.PREFIX+defs+MAP_SVG.DEFS.POSTFIX;
          el = document.createElement('svg'); document.body.prepend(el); el.outerHTML = defs;
        }
      }


    },

    svg_defs_remove()  { let el = document.getElementById(MAP_SVG.DEFS.ID);  if (el) el.remove(); },
    svg_style_remove() { let el = document.getElementById(MAP_SVG.STYLE.ID); if (el) el.remove(); },
    svg_remove()       { this.svg_defs_remove  (); this.svg_style_remove(); },
  },
}
