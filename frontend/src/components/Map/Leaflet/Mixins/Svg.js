import { mapGetters } from 'vuex';
import { dict_get } from '@/components/Map/Leaflet/Lib/Lib';
import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { MAP_SVG } from '@/components/Map/Leaflet/Mixins/Svg.const';

export default {
  data: () => ({
    svg: [],
  }),

  mounted: function() {
    this.svg_const_defs_create();
    this.svg_const_style_create();
  },

  beforeDestroy: function() {
    this.svg_remove();
  },

  watch: {
    SCRIPT_GET: {
      handler: function(val) { this.svg_var_create(val); },
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

    svg_var_create(items) {
      this.svg_var_remove();
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
          let svg = MAP_SVG.LIST[item_class];
          if (!svg) return;
          let svg_style = svg[MAP_SVG.STYLE_KEY];
          let svg_defs  = svg[MAP_SVG.DEFS_KEY];

          // уникальный id
          let id = 'svg_'+ind+'_'+ind_class;

          // заменить переменные
          if (svg_style) {
            svg_style = svg_style.replace(/{id}/g, id).replace(/{color}/g, item_color);
            style    += '.'+item_class+' { '+svg_style+' }';
          }

          if (svg_defs ) {
            svg_defs  = svg_defs.replace(/{id}/g, id).replace(/{color}/g, item_color);
            defs  += svg_defs;
          }
        });

        let el;
        if (style!='') {
          style = MAP_SVG.VAR.STYLE_TXT_PREFIX+style+MAP_SVG.VAR.STYLE_TXT_POSTFIX;
          el = document.createElement('style'); document.body.prepend(el); el.outerHTML = style;
        }
        if (defs!='') {
          defs = MAP_SVG.VAR.DEFS_TXT_PREFIX +defs +MAP_SVG.VAR.DEFS_TXT_POSTFIX;
          el = document.createElement('svg'); document.body.prepend(el); el.outerHTML = defs;
        }
      }


    },

    svg_const_defs_create()  { let el = document.createElement('svg');   document.body.prepend(el); el.outerHTML = MAP_SVG.CONST.DEFS_TXT; },
    svg_const_style_create() { let el = document.createElement('style'); document.body.prepend(el); el.outerHTML = MAP_SVG.CONST.STYLE_TXT; },

    svg_const_defs_remove()  { let el = document.getElementById(MAP_SVG.CONST.DEFS_ID);  if (el) el.remove(); },
    svg_const_style_remove() { let el = document.getElementById(MAP_SVG.CONST.STYLE_ID); if (el) el.remove(); },
    svg_var_defs_remove()    { let el = document.getElementById(MAP_SVG.VAR.DEFS_ID);    if (el) el.remove(); },
    svg_var_style_remove()   { let el = document.getElementById(MAP_SVG.VAR.STYLE_ID);   if (el) el.remove(); },
    svg_const_remove()       { this.svg_const_defs_remove(); this.svg_const_style_remove(); },
    svg_var_remove()         { this.svg_var_defs_remove  (); this.svg_var_style_remove(); },
    svg_remove()             { this.svg_const_remove();      this.svg_var_remove(); },
  },
}
