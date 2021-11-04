// РАЗМЕТКА
export const STYLE_DATA_LAYOUT_ICON = {

}





export const STYLE_DATA_LAYOUT_DECOR = {
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





export const STYLE_DATA_LAYOUT_TEST = [
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
