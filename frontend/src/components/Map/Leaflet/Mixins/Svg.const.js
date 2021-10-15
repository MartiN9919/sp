export const MAP_SVG = {
  CONST: {
    DEFS_ID:  'map-svg-const-defs',
    STYLE_ID: 'map-svg-const-style',
    DEFS_TXT: `
      <svg id="map-svg-const-defs" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" width="0" height="0">
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
        </defs>
      </svg>
    `,
    STYLE_TXT: `
      <style id="map-svg-const-style">
        .head-arrow-end-22 { marker-end: url(#head-arrow-2); }
      </style>
    `,
  },

  VAR: {
    DEFS_ID:  'map-svg-var-defs',
    STYLE_ID: 'map-svg-var-style',
    DEFS_TXT_PREFIX: `
      <svg id="map-svg-var-defs" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" width="0" height="0">
        <defs>
      `,
    DEFS_TXT_POSTFIX: `
        </defs>
      </svg>
    `,
    STYLE_TXT_PREFIX: `
      <style id="map-svg-var-style">
      `,
    STYLE_TXT_POSTFIX: `
      </style>
    `,
  },

  STYLE_KEY: 'style',
  DEFS_KEY:  'defs',
  LIST: {
    // заливка: диагональные штрихи

    // стрелка: <=>
    'arrow-double': {
      style: 'marker-end: url(#{id});',
      defs: `
        <marker id='{id}' fill='{color}' orient="auto" markerUnits='userSpaceOnUse' markerWidth='101' markerHeight='33' refX='0.1' refY='16.5' opacity='.5'>
          <path d='M1,17 L21,1 L21,33 Z'/>
          <path d='M101,17 L82,1 L82,33 Z'/>
          <rect x="20" y="6" width="64" height="5" />
          <rect x="20" y="23" width="64" height="5" />
        </marker>
      `,
    },

    // ...

  },

}
