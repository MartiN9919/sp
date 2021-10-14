export default {
  data: () => ({
    color_temp: 'blue'
  }),
  methods: {
    // ВАЖНО
    // вызывать из родительского mounted или method.onMapReady
    mounted_after_svg() {
      let el = document.createElement('svg');
      document.body.prepend(el);
      el.outerHTML = `
<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" width="0" height="0">
  <defs>
    <pattern id="fill-star" x="0" y="0" width="25" height="25" patternUnits="userSpaceOnUse">
      <circle cx="10" cy="10" r="10"/>
    </pattern>

    <pattern id="fill-diagonal-hatch" patternUnits="userSpaceOnUse" width="4" height="4">
      <path d="M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2" style="stroke:black; stroke-width:1;" />
    </pattern>

    <marker id='head-arrow' orient="auto" markerUnits='userSpaceOnUse' markerWidth='2' markerHeight='4' refX='0.1' refY='0'>
      <path d='M0,0 V4 L2,2 Z' fill="red"/>
    </marker>

    <marker id='head-arrow-2' orient="auto" markerUnits='userSpaceOnUse' markerWidth='101' markerHeight='33' refX='0.1' refY='16.5' fill='${this.color_temp}' opacity='.5'>
      <path d='M1,17 L21,1 L21,33 Z'/>
      <path d='M101,17 L82,1 L82,33 Z'/>
      <rect x="20" y="6" width="64" height="5" />
      <rect x="20" y="23" width="64" height="5" />
    </marker>

  </defs>
</svg>
      `;
    },
  },


//
//fill='#555'
//       <path d='M1,6 L8,1 L8,11 Z' fill="white" stroke="context-stroke"/>
// fill="context-stroke"
//stroke="context-stroke"
//stroke:black;

}
