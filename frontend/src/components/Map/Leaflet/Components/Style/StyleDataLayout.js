// РАЗМЕТКА
export const ICON = {
  // Госграница
  'layout_border': {
    anchor_dx: 10,
    anchor_dy: 25,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 40 70">
        <path style="fill:none;stroke:#444;stroke-width:8;" d="M 0,2 H 20 M 10,0 V 50 M 0,48 h 20"/>
        <circle style="fill:#444" cx="10" cy="65" r="5" />
      </svg>
    `,
  },
}





export const DECOR = {
  // линия _ . _ произвольного цвета
  'line_layout_1': [
    { offset: 12, repeat: 25, symbol_type: 'dash', symbol_options: { pixelSize: 10, pathOptions: { color: '{color}', weight: 2, }, }, },
    { offset: 0,  repeat: 25, symbol_type: 'dash', symbol_options: { pixelSize: 0,  pathOptions: { color: '{color}', }, }, },
  ],

  // линия _ .. _ произвольного цвета
  'line_layout_2': [
    { offset: 18, repeat: 30, symbol_type: 'dash', symbol_options: { pixelSize: 10, pathOptions: { color: '{color}', weight: 2, }, }, },
    { offset: 0,  repeat: 30, symbol_type: 'dash', symbol_options: { pixelSize: 0,  pathOptions: { color: '{color}', }, }, },
    { offset: 5,  repeat: 30, symbol_type: 'dash', symbol_options: { pixelSize: 0,  pathOptions: { color: '{color}', }, }, },
  ],

  // Госграница
  // class="hidden" для основной линии
  'line_layout_border': { offset: 0, repeat: 31, symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-layout_border', }, }, icon_properties: { shadow: 'red', }, },

  // Рубеж охраны 1 _ . _
  // class="hidden" для основной линии
  'line_layout_border_1': [
    { offset: 12, repeat: 25, symbol_type: 'dash', symbol_options: { pixelSize: 10, pathOptions: { color: '#0a0', weight: 2, }, }, },
    { offset: 0,  repeat: 25, symbol_type: 'dash', symbol_options: { pixelSize: 0,  pathOptions: { color: '#0a0', }, }, },
  ],

  // Рубеж охраны 2 _ .. _
  // class="hidden" для основной линии
  'line_layout_border_2': [
    { offset: 18, repeat: 30, symbol_type: 'dash', symbol_options: { pixelSize: 10, pathOptions: { color: '#0a0', weight: 2, }, }, },
    { offset: 0,  repeat: 30, symbol_type: 'dash', symbol_options: { pixelSize: 0,  pathOptions: { color: '#0a0', }, }, },
    { offset: 5,  repeat: 30, symbol_type: 'dash', symbol_options: { pixelSize: 0,  pathOptions: { color: '#0a0', }, }, },
  ],



  // стрелки с окантовкой
  'line-test_arrow_stroke': {
    offset: 12, repeat: 100,
    symbol_type: 'arrow', symbol_options: { pixelSize: 8, pathOptions: { color: '{color}', weight: 2, stroke: true, }, },
    icon_properties: { shadow: false, },
  },

  // стрелки закрашенные
  'line-test_arrow_fill': {
    offset: 12, repeat: 100,
    symbol_type: 'arrow', symbol_options: { pixelSize: 8, pathOptions: { color: '{color}', weight: 0, fillOpacity: 1, }, },
    icon_properties: { shadow: false, },
  },

  // стрелка в конце, для полигонов не подходит
  'line-test_arrow_end': {
    offset: '100%', repeat: 0,
    symbol_type: 'arrow', symbol_options: { pixelSize: 8, polygon: false, pathOptions: { color: '{color}', stroke: true, }, },
    icon_properties: { shadow: false, },
  },
}




export const SVG = {
  // стрелка: <=>
  'layout-arrow-double': {
    zoom: 1.8,
    style: '{class} { marker-end: url(#{id}); }',
    defs: `
      <marker id="{id}" viewBox="0 0 101 82" fill="{color}" orient="auto" markerUnits="userSpaceOnUse" markerWidth="{width}" markerHeight="{height}" refX='0' refY='16.5' opacity='.7'>
        <path d='M1,17 L21,1 L21,33 Z'/>
        <path d='M101,17 L82,1 L82,33 Z'/>
        <rect x="20" y="6"  width="64" height="5" />
        <rect x="20" y="23" width="64" height="5" />
      </marker>
    `,
  },


  // штриховка: диагональные штрихи тонкие
  'hatch-diagonal-1': {
    style: '{class} { fill: url(#{id}); }',
    defs: `
      <pattern id="{id}" patternUnits="userSpaceOnUse" width="4" height="4">
        <path d="M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2" style="stroke:{color}; stroke-width:1;" />
      </pattern>
      `,
  },
  // штриховка: сетка  rotate-любой угол
  'hatch-grid-1': {
    style: '{class} { fill: url(#{id}); }',
    defs: `
      <pattern id="{id}" patternUnits="userSpaceOnUse" width="10" height="10" patternTransform="rotate(45)">
        <path d="M 5,0 V 10 M 0,5 H 10" style="stroke:{color}; stroke-width:1;" />
      </pattern>
    `,
  },
  // штриховка: сетка  rotate-любой угол
  'hatch-grid-2': {
    style: '{class} { fill: url(#{id}); }',
    defs: `
      <pattern id="{id}" patternUnits="userSpaceOnUse" width="10" height="10" patternTransform="rotate(25)">
        <path d="M 5,0 V 10 M 0,5 H 10" style="stroke:{color}; stroke-width:2;" />
      </pattern>
    `,
  },
  // штриховка: узор
  'hatch-uzor-1': {
    style: '{class} { fill: url(#{id}); }',
    defs: `
      <pattern id="{id}" patternUnits="userSpaceOnUse" width="10" height="10" style="stroke:{color}; stroke-width:4">
        <line x1="5" y1="0" x2="5" y2="10" opacity=".4" transform="rotate(16 5 5)"/>
        <line x1="5" y1="0" x2="5" y2="10" opacity=".4" transform="rotate(72 5 5)"/>
      </pattern>
    `,
  },
}



export const TEST = [
  {
    "type": "Feature",
    "properties": {
      "class": "line_layout_border hidden",
      "hint": "line_layout_border hidden",
      "date": "2021-01-08",
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [24.0,55.75],
        [27.5,56.75],
        [32.0,55.75],
      ]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "line_layout_2 hidden",
      "hint": "line_layout_2 hidden",
      "date": "2021-01-04",
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [24.0,55.5],
        [27.5,56.5],
        [32.0,55.5],
      ]
    },
  },
]
