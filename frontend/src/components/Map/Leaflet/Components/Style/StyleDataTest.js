// РАЗРАБОТКА
export const ICON = {
  // стрелка: <=> использовать в качестве конечной не получается
  'test_arrow_double': {
    anchor_dx: 0,
    anchor_dy: 0,
    zoom:      .8,
    svg: `
      <svg fill="{color}" width={width} height={height} viewBox="0 0 101 33">
        <path d='M1,17 L21,1 L21,33 Z'/>
        <path d='M101,17 L82,1 L82,33 Z'/>
        <rect x="20" y="6" width="64" height="5" />
        <rect x="20" y="23" width="64" height="5" />
      </svg>
    `,
  },
}



export const DECOR = {
  // стрелка: <=>
  'line-test_arrow_double_end': {
    offset: '100%', repeat: 0,
    symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-test_arrow_double', }, },
    icon_properties: { shadow: false, },
  },

  // иконка file
  'line-test_file': {
    offset: 25, repeat: 120,
    symbol_type: 'marker', symbol_options: { rotate: false, markerOptions: { icon: 'icon-file-test_auto-30-20', }, },
    icon_properties: { shadow: false, },
  },

  // штрих линия
  'line-test2': {
    offset: 0, repeat: 10,
    symbol_type: 'dash', symbol_options: { pixelSize: 5, pathOptions: { color: '#f0f', weight: 1, opacity: 0.5, }, },
    icon_properties: { shadow: false, },
  },

}



export const SVG = {
  // стрелка: <=>
  'arrow-double-end': {
    style: '{class} { marker-end: url(#{id}); }',
    defs: `
      <marker id="{id}" fill="{color}" orient="auto" markerUnits='userSpaceOnUse' markerWidth='101' markerHeight='33' refX='0' refY='16.5' opacity='.5'>
        <path d='M1,17 L21,1 L21,33 Z'/>
        <path d='M101,17 L82,1 L82,33 Z'/>
        <rect x="20" y="6" width="64" height="5" />
        <rect x="20" y="23" width="64" height="5" />
      </marker>
    `,
  },


  // черта: тройная
  'dash-3': {
    style: '{class} { marker-pattern: "40 url(#{id}_2) 40 url(#{id}_1)"; }',
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
}



export const TEST = [
  // стрелки с окантовкой
  {
    "type": "Feature",
    "properties": {
      "class": "line-test_arrow_stroke",
      "hint": "line-test_arrow_stroke",
      "date": "2021-01-05",
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [43,55.5],
        [46,56.5],
        [48,55.5],
      ]
    },
  },
  // стрелки закрашенные
  {
    "type": "Feature",
    "properties": {
      "class": "line-test_arrow_fill line-test_arrow_double_end",
      "hint": "line-test_arrow_fill line-test_arrow_double_end",
      "date": "2021-01-04",
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [43,56.0],
        [46,57.0],
        [48,56.0],
      ]
    },
  },
  // стрелка в конце, для полигонов не подходит
  {
    "type": "Feature",
    "properties": {
      "class": "line-test_arrow_end",
      "hint":  "line-test_arrow_end",
      "date":  "2021-01-06 09:00",
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [43,56.5],
        [46,57.5],
        [48,56.5],
      ]
    },
  },
  // иконка file
  {
    "type": "Feature",
    "properties": {
      "class": "line-test_file",
      "hint":  "line-test_file",
      "date":  "2021-01-06 09:00",
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [43,57.0],
        [46,58.0],
        [48,57.0],
      ]
    },
  },
  // штрих линия
  {
    "type": "Feature",
    "properties": {
      "class": "line-test2 hidden",
      "hint":  "line-test2 hidden",
      "date":  "2021-01-06 09:00",
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [43,57.5],
        [46,58.5],
        [48,57.5],
      ]
    },
  },



  // иконка font-mdi
  {
    "type": "Feature",
    "properties": {
      "class": "icon-mdi-flag sss icon-mdi-spin tst",
      "hint": "icon-mdi-flag icon-mdi-spin",
      "date": "2021-01-03",
      //"zoom": false, - не масштабируется
    },
    "geometry": {
      "type": "Point",
      "coordinates": [45,53.0],
    },
  },
  // иконка font-fs
  {
    "type": "Feature",
    "properties": {
      "class": "icon-fs-spec0",
      "hint": "icon-fs-spec0",
      "date": "2021-01-04",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [45.5,53.0],
    },
  },







  {
    "type": "Feature",
    "properties": {
      "class": "line-test_arrow_stroke hatch-uzor-1",
      //"color": "blue",
      "hint":  "line-test_arrow_stroke hatch-uzor-1",
      "date":  "2021-01-05 09:00",
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [
        [
          [46.0,52.5],
          [47.0,51.5],
          [46.0,50.5],
          [46.0,52.5],
        ]
      ]
    },
  },
]
