// ОБЩИЙ ХАРАКТЕР
export const ICON = {
  // иконка стандарт
  'standart': {
    anchor_dx: 33.1,
    anchor_dy: 98.2,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 67 100">
        <g transform="matrix(4.1640031,0,0,4.0920941,-16.549318,-4208.0243)">
          <circle style="fill:#fff;" cx="12.196746" cy="1036.2429" r="4.545763"/>
          <path style="fill:url(#{id});stroke:#000;stroke-width:0.2" d="m 12.048682,1028.4328 c -4.4183005,0 -8.0000005,3.5817 -8.0000005,8 0,1.421 0.3816,2.75 1.0312,3.906 0.1079,0.192 0.221,0.381 0.3438,0.563 l 6.6250005,11.531 6.625,-11.531 c 0.102,-0.151 0.19,-0.311 0.281,-0.469 l 0.063,-0.094 c 0.649,-1.156 1.031,-2.485 1.031,-3.906 0,-4.4183 -3.582,-8 -8,-8 z m 0,4 c 2.209,0 4,1.7909 4,4 0,2.209 -1.791,4 -4,4 -2.2091005,0 -4.0000005,-1.791 -4.0000005,-4 0,-2.2091 1.7909,-4 4.0000005,-4 z"/>
        </g>
        <defs>
          <linearGradient id="{id}_grag1">
            <stop style="stop-color:{color};" offset="0"/>
            <stop style="stop-color:#fff;" offset="1"/>
          </linearGradient>
          <linearGradient id="{id}" x1="20" y1="1052" x2="-10" y2="1006" xlink:href="#{id}_grag1" gradientUnits="userSpaceOnUse"/>
        </defs>
      </svg>
    `,
  },


  // ПРОИСШЕСТВИЕ
  'point_detention_inside': {
    anchor_dx: 53,
    anchor_dy: 50.,
    zoom:      .7,
    svg: `
      <svg width={width} height={height} viewBox="0 0 106 100">
        <path style="fill:#ffffff00;stroke:#f00;stroke-width:6" d="M 78,6.7 A 53,53 0 0,1 78,93.3"/>
        <path style="fill:#ffffff00;stroke:#f00;stroke-width:6" d="M 28,93.3 A 53,53 0 0,1 28,6.7"/>
        <circle style="fill:#fff;stroke:#00f;stroke-width:6" cx="53" cy="53" r="25"/>
      </svg>
    `,
  },
}





export const DECOR = {
  // обычные маркеры
  'line-standart': {
    offset: 10, repeat: 150,
    symbol_type: 'marker', symbol_options: { rotate: false, markerOptions: { icon: 'icon-svg-standart', }, },
  },
}



export const SVG = {
  // скрыть основную фигуру или точку
  'hidden': {
    style: '{class} { opacity: 0; }',
  },
}



export const TEST = [
  {
    "type": "Feature",
    "properties": {
      "class": "line-standart line-text_lr_100 hatch-diagonal-1",
      "hint": "line-standart line-text_lr_100 hatch-diagonal-1",
      "text": "STOP",
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [
        [
          [25.0,55.5],
          [27.5,56.25],
          [31.0,55.5],
          [25.0,55.5],
        ]
      ]
    },
  },

  // иконка стандарт
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-standart",
      "hint": "icon-svg-standart",
      "date": "2021-01-02",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.0,54.5],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "hint":  "class=undefined color=undefined",
      "date":  "2021-01-04",
      "zoom":  false,
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.5,54.5],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-standart",
      "hint": "class=icon-svg-standart zoom=false",
      "date": "2021-01-02",
      "zoom": false,
    },
    "geometry": {
      "type": "Point",
      "coordinates": [25.0,54.5],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "hint":  "class=undefined color='gold'",
      "date":  "2021-01-04",
      "color": "gold",
      "zoom":  false,
    },
    "geometry": {
      "type": "Point",
      "coordinates": [25.5,54.5],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "hint":  "class=undefined color='#8d0099'",
      "date":  "2021-01-04",
      "color": "#8d0099",
      "zoom":  false,
    },
    "geometry": {
      "type": "Point",
      "coordinates": [26.0,54.5],
    },
  },




  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-point_detention_inside",
      "text": '"detention"',
      "hint": "icon-svg-point_detention_inside\ntest\nasdf asd fa sdf a sd fa sd f asd f as df a sd fa sd f asd f asd fa sd fa sdf asd",
      "date": "2021-04-01",
      "zoom": false,
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.0,54.75],
    },
  },

]
