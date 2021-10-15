import { mapGetters } from 'vuex';
import { dict_get } from '@/components/Map/Leaflet/Lib/Lib';
import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { MAP_SVG } from '@/components/Map/Leaflet/Mixins/Svg.const';

export default {
  data: () => ({
    color_id:   'head-arrow-2',
    color_temp: 'blue',
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
    //   this.svg.push(`
    //     <marker id='${this.color_id}' fill='${this.color_temp}' orient="auto" markerUnits='userSpaceOnUse' markerWidth='101' markerHeight='33' refX='0.1' refY='16.5' opacity='.5'>
    //       <path d='M1,17 L21,1 L21,33 Z'/>
    //       <path d='M101,17 L82,1 L82,33 Z'/>
    //       <rect x="20" y="6" width="64" height="5" />
    //       <rect x="20" y="23" width="64" height="5" />
    //     </marker>
    //     `);
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
          let svg = MAP_SVG.LIST[item_class] ?? [undefined, undefined];
          let svg_style = svg[0];
          let svg_defs  = svg[1];
          if ((!svg_style) || (!svg_defs)) return;

          // уникальный id
          let id = 'svg_'+ind+'_'+ind_class;

          // заменить переменные
          svg_style = svg_style.replace(/{id}/g, id).replace(/{color}/g, item_color);
          svg_defs  = svg_defs.replace(/{id}/g, id).replace(/{color}/g, item_color);

          // запомнить
          style += '.'+item_class+' { '+svg_style+' }';
          defs  += svg_defs;
          console.log(id, item_color, item_class, ind_class, svg_style, svg_defs);
        });

        if ((style=='') || (defs=='')) return;
        style = MAP_SVG.VAR.STYLE_TXT_PREFIX+style+MAP_SVG.VAR.STYLE_TXT_POSTFIX;
        defs  = MAP_SVG.VAR.DEFS_TXT_PREFIX +defs +MAP_SVG.VAR.DEFS_TXT_POSTFIX;

        console.log(style, defs)

        let el;
        el = document.createElement('style'); document.body.prepend(el); el.outerHTML = style;
        el = document.createElement('svg');   document.body.prepend(el); el.outerHTML = defs;
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

    // <marker id='head-arrow-2' fill='${this.color_temp}' orient="auto" markerUnits='userSpaceOnUse' markerWidth='101' markerHeight='33' refX='0.1' refY='16.5' opacity='.5'>
    //   <path d='M1,17 L21,1 L21,33 Z'/>
    //   <path d='M101,17 L82,1 L82,33 Z'/>
    //   <rect x="20" y="6" width="64" height="5" />
    //   <rect x="20" y="23" width="64" height="5" />
    // </marker>



  //   <pattern id='head-arrow-1' width='101' height='33'>
  //     <path d='M1,17 L21,1 L21,33 Z'/>
  //     <path d='M101,17 L82,1 L82,33 Z'/>
  //     <rect x="20" y="6" width="64" height="5" />
  //     <rect x="20" y="23" width="64" height="5" />
  //   </pattern>

  // </defs>

  // <defs>
  //   <marker id='head-arrow-2' xlink:href="#head-arrow-1" fill="red" orient="auto" markerUnits='userSpaceOnUse' markerWidth='101' markerHeight='33' refX='0.1' refY='16.5' >
  //   </marker>
  // </defs>

// return process.env.BASE_URL+MAP_ITEM.FC.STYLE.MARKER.PATH+name+'.png';
// import                 '@/components/Map/Leaflet/Markers/Pulse';

// refX='center' 'left', 'top'
// xlink:href="#head-arrow-1"
// fill='${this.color_temp}'
// fill='#555'
// fill="context-stroke"
// <path d='M1,6 L8,1 L8,11 Z' fill="white" stroke="context-stroke"/>
// stroke="context-stroke"
// stroke:black;

}
