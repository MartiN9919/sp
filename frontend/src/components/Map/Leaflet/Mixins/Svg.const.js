export const MAP_SVG = {
  DEFS: {
    ID:      'map-svg-defs',
    PREFIX:  '<svg id="map-svg-defs" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" width="0" height="0">\n<defs>\n',
    POSTFIX: '</defs>\n</svg>',
  },

  STYLE: {
    ID:      'map-svg-style',
    PREFIX:  '<style id="map-svg-style">\n',
    POSTFIX: '\n</style>',
  },

  DAT: {
    KEY_STYLE: 'style',
    KEY_DEFS:  'defs',
    VAL: {
      // штриховка: диагональные штрихи тонкие
      'hatch-diagonal-1': {
        style: 'fill: url(#{id});',
        defs: `
            <pattern id="{id}" patternUnits="userSpaceOnUse" width="4" height="4">
              <path d="M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2" style="stroke:{color}; stroke-width:1;" />
            </pattern>
          `,
      },


      // черта: тройная
      'dash-3': {
        style: 'marker-pattern: "40 url(#{id}_2) 40 url(#{id}_1)"',
        defs: `
          <marker id="{id}_2" orient="auto" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="12" refX="0" refY="0" viewBox="-4 -6 8 12">
            <rect x="-3" y="-5" width="2" height="10"/>
            <rect x="1" y="-5" width="2" height="10"/>
          </marker>
          <marker id="{id}_1" orient="auto" markerUnits="userSpaceOnUse" markerWidth="4" markerHeight="12" refX="0" refY="0" viewBox="-2 -6 4 12">
            <rect x="-1" y="-5" width="2" height="10"/>
          </marker>
        `,
      },


      // стрелка: <=>
      'arrow-double-end': {
        style: 'marker-end: url(#{id});',
        defs: `
          <marker id="{id}" fill="{color}" orient="auto" markerUnits='userSpaceOnUse' markerWidth='101' markerHeight='33' refX='51' refY='16.5' opacity='.5'>
            <path d='M1,17 L21,1 L21,33 Z'/>
            <path d='M101,17 L82,1 L82,33 Z'/>
            <rect x="20" y="6" width="64" height="5" />
            <rect x="20" y="23" width="64" height="5" />
          </marker>
        `,
      },


      // скрыто
      'hidden': {
        style: 'opacity: 0;',
      },

      // тест
      'fill-test': {
        style: 'fill: url(#{id});',
        defs: `
            <pattern id="{id}" fill="{color}" x="0" y="0" width="25" height="25" patternUnits="userSpaceOnUse">
              <circle cx="10" cy="10" r="10"/>
            </pattern>
          `,
      },

      // ...

    },
  },
}
