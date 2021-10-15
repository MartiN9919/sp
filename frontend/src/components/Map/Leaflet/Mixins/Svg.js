import { MAP_SVG } from '@/components/Map/Leaflet/Mixins/Svg.const';

export default {
  data: () => ({
    color_id:   'head-arrow-2',
    color_temp: 'blue',
    svg: [],
  }),

  mounted: function() {
      let el = document.createElement('svg');
      document.body.prepend(el);
      el.outerHTML = MAP_SVG.CONST.TXT;
  },

  beforeDestroy: function() {
    this.svg_const_remove();
    this.svg_var_remove();
  },

  watch: {
    svg: function(val) {
      this.svg_var_remove();
    },
  },

  methods: {
    // вызывать из родительского mounted
    mounted_after_svg() {
      let el = document.createElement('svg');
      document.body.prepend(el);
      el.outerHTML =
        MAP_SVG.VAR.PREFIX+`
        <marker id='${this.color_id}' fill='${this.color_temp}' orient="auto" markerUnits='userSpaceOnUse' markerWidth='101' markerHeight='33' refX='0.1' refY='16.5' opacity='.5'>
          <path d='M1,17 L21,1 L21,33 Z'/>
          <path d='M101,17 L82,1 L82,33 Z'/>
          <rect x="20" y="6" width="64" height="5" />
          <rect x="20" y="23" width="64" height="5" />
        </marker>
        `+MAP_SVG.VAR.POSTFIX;
    },

    svg_const_remove() { let el = document.getElementById(MAP_SVG.CONST.ID); if (el) el.remove(); },
    svg_var_remove()   { let el = document.getElementById(MAP_SVG.VAR.ID);   if (el) el.remove(); },

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
