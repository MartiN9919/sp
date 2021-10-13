export default {
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

    <marker id='head-arrow-2' orient="auto" markerWidth='31' markerHeight='11' refX='0.1' refY='6' fill='#555' opacity='.5'>
      <path d='M1,6 L8,1 L8,11 Z' fill="context-stroke"/>
      <path d='M31,6 L24,1 L24,11 Z' fill="context-stroke"/>
      <path d='M8,3 L24,3 L24,4 L8,4'/>
      <path d='M8,8 L24,8 L24,9 L8,9'/>
    </marker>

  </defs>
</svg>
      `;
    },
  },


// markerUnits='userSpaceOnUse'
//
//       <path d='M1,6 L8,1 L8,11 Z' fill="white" stroke="context-stroke"/>
// fill="context-stroke"
//stroke="context-stroke"
//stroke:black;

}
