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
}




export const SVG = {

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
      "class": "line_layout_border_1 hidden",
      "hint": "line_layout_border_1 hidden",
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
