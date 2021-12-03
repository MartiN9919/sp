// СИЛЫ
export const ICON = {
  // пункт управления прикордон
  'force_manage_inside': {
    anchor_dx: 0,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 100 100">
        <path style="fill:#fff;stroke:#f00;stroke-width:4" d="M 2.2,99.8 V 2.2 H 90.0 L 70.0,38.6 2.3,38.6"/>
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif" x="6" y="25">{text}</text>
        <text style="font-style:normal;font-weight:normal;font-size:35px;font-family:sans-serif" x="17" y="99">КП</text>
      </svg>
    `,
  },
  // пункт управления закордон
  'force_manage_outside': {
    anchor_dx: 92,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 100 100">
        <path style="fill:#fff;stroke:#00f;stroke-width:4" d="M 91.38,99.8 V 2.2 H 3.58 L 23.58,38.6 h 67.7"/>
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif;text-anchor:end" x="87" y="25">{text}</text>
      </svg>
    `,
  },
  // отдел пограничной службы прикордон
  'force_ops_inside': {
    anchor_dx: 0,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 200 100">
        <path style="fill:#fff;stroke:{color};stroke-width:4" d="M 2.4,99.8 V 2.6 H 71.5 L 2.6,46.9"/>
        <text style="font-style:normal;font-size:16px;font-family:sans-serif;font-weight:bold" x="6" y="20">ОПС</text>
        <text style="font-style:normal;font-size:16px;font-family:sans-serif;font-weight:normal" x="6" y="96">{text}</text>
      </svg>
    `,
  },
  // подразделение погранзаставы прикордон
  'force_frontier_inside': {
    anchor_dx: 0,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 55 100">
        <path style="fill:#fff;stroke:#f00;stroke-width:4" d="M 2.2,100 V 3.3 L 50.7,25.1 2.2,47.8"/>
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif" x="6" y="29">{text}</text>
      </svg>
    `,
  },
  // подразделение погранохраны закордон
  'force_frontier_outside': {
    anchor_dx: 54,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 55 100">
        <path style="fill:#fff;stroke:#00f;stroke-width:4" d="M 53.5,100 V 3.3 L 5.0,25.1 53.5,47.8"/>
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif;text-anchor:end" x="49" y="29">{text}</text>
      </svg>
    `,
  },
  // пост погранохраны прикордон
  'force_guard_inside': {
    anchor_dx: 0,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 57 100">
        <path style="fill:#fff;stroke:#f00;stroke-width:4" d="M 2.3,100 V 4.3 L 51.6,42 2.3,42"/>
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif" x="6" y="35">{text}</text>
      </svg>
    `,
  },
  // пост погранохраны закордон
  'force_guard_outside': {
    anchor_dx: 54,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 57 100">
        <path style="fill:#fff;stroke:#00f;stroke-width:4" d="M 55.5,100 V 4.3 L 6.2,42 H 55.5"/>
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif;text-anchor:end" x="50" y="35">{text}</text>
      </svg>
    `,
  },
  // погранпост временный прикордон
  'force_guard_temp_inside': {
    anchor_dx: 0,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 60 102">
        <path style="fill:#fff;stroke:{color};stroke-width:4" d="M 7,94 V 4.2910497 L 55,43 7,43"/>
        <circle style="fill:{color};stroke:{color};stroke-width:2" cx="7" cy="94" r="5"/>
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif" x="10" y="35">{text}</text>
      </svg>
    `,
  },
  // погранконтроль прикордон
  'force_unit_control_inside': {
    anchor_dx: 0,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 200 100">
        <path style="fill:#fff;stroke:#f00;stroke-width:4"   d="M 1.9,100 2.6,22.7 2.5,3.2 44.0,23.5 2.1,41.0"/>
        <path style="fill:#f00;stroke:#f00;stroke-width:1px" d="M 22.6,13.1 3.0,22.6 22.8,32.2 44.0,23.5 Z"/>
        <text style="font-style:normal;font-size:16px;font-family:sans-serif" x="6" y="96">{text}</text>
      </svg>
    `,
  },
  // погранконтроль закордон
  'force_unit_control_outside': {
    anchor_dx: 198,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 200 100">
        <path style="fill:#fff;stroke:#00f;stroke-width:4"   d="m 198.0,100.1 -0.7,-77.3 0.1,-19.5 -41.5,20.3 41.9,17.5"/>
        <path style="fill:#00f;stroke:#00f;stroke-width:1px" d="m 177.3,13.2 19.6,9.5 -19.8,9.6 -21.2,-8.7 z"/>
        <text style="font-style:normal;font-size:16px;font-family:sans-serif;text-anchor:end" x="190" y="96">{text}</text>
      </svg>
    `,
  },
  // НП скрытый
  'force_point_observation_hidden': {
    anchor_dx: 40.,
    anchor_dy: 40.,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 80 80">
        <path style="fill:#fff;stroke:#555;stroke-width:4" d="M 2,2 V 78 H 78 V 2 Z m 9,9 H 70 M 40.5,17 8,70 h 64 z"/>
      </svg>
    `,
  },
  // НП открытый
  'force_point_observation_open': {
    anchor_dx: 40.,
    anchor_dy: 40.,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 80 80">
        <path style="fill:#fff;stroke:#555;stroke-width:4" d="M 2,2 V 78 H 78 V 2 Z M 40.5,17 8,70 h 64 z"/>
      </svg>
    `,
  },
  // контрольный пункт
  'force_point_control': {
    anchor_dx: 50.,
    anchor_dy: 25.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 100 50">
        <path style="fill:#fff;stroke:#555;stroke-width:4" d="M 2,10 V 40 M 100,10 V 40 M 2,24.5 h 96"/>
        <circle style="fill:#fff;stroke:#555;stroke-width:4" cx="50" cy="24.5" r="22"/>
      </svg>
    `,
  },
  // пограничный наряд прикордон
  'force_patrol_inside': {
    anchor_dx: 72,
    anchor_dy: 70,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 244 140">
        <g transform="rotate({rotate} 72 70)">
          <circle style="fill:#fff;stroke:#f00;stroke-width:4" cx="72" cy="70" r="20"/>
          <path style="fill:none;stroke:#f00;stroke-width:4" d="M72,51 V5 M82,26 72,5 62,26"/>
        </g>
        <text style="font-style:normal;font-size:16px;font-family:sans-serif;text-anchor:start" x="100" y="75">{text}</text>
      </svg>
    `,
  },
  // пограничный наряд закордон
  'force_patrol_outside': {
    anchor_dx: 172,
    anchor_dy: 70,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 244 140">
        <g transform="rotate({rotate} 172 70)">
          <circle style="fill:#fff;stroke:#00f;stroke-width:4" cx="172" cy="70" r="20"/>
          <path style="fill:none;stroke:#00f;stroke-width:4" d="M172,51 V5 M182,26 172,5 162,26"/>
        </g>
        <text style="font-style:normal;font-size:16px;font-family:sans-serif;text-anchor:end" x="140" y="75">{text}</text>
      </svg>
    `,
  },
  // вертолет прикордон
  'force_helicopter_inside': {
    anchor_dx: 20,
    anchor_dy: 100,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 200 100">
        <path style="fill:none;stroke:#f00;stroke-width:4" d="M2,2 38,38 M2,38 38,2 M20,20 V100"/>
        <text style="font-style:normal;font-size:16px;font-family:sans-serif;text-anchor:start" x="25" y="95">{text}</text>
      </svg>
    `,
  },
  // вертолет закордон
  'force_helicopter_outside': {
    anchor_dx: 180,
    anchor_dy: 100,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 200 100">
        <path style="fill:none;stroke:#00f;stroke-width:4" d="M162,2 198,38 M162,38 198,2 M180,20 V100"/>
        <text style="font-style:normal;font-size:16px;font-family:sans-serif;text-anchor:end" x="170" y="95">{text}</text>
      </svg>
    `,
  },
  // вертолет для траектории
  'force_helicopter_route': {
    anchor_dx: 20,
    anchor_dy: 20,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 40 40">
        <path style="fill:none;stroke:{color};stroke-width:4" d="M2,2 38,38 M2,38 38,2"/>
      </svg>
    `,
  },
  // квадрокоптер для траектории
  'force_quadcopter_route': {
    anchor_dx: 20,
    anchor_dy: 20,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 40 40">
        <path style="fill:none;stroke:{color};stroke-width:4" d="M6,6 34,34 M6,34 34,6 M2,10 10,2 M30,2 38,10  M30,38 38,30  M2,30 10,38"/>
      </svg>
    `,
  },
}





export const DECOR = {
  // линия - Х - траектория вертолета прикордон
  'line-force_helicopter_route_inside': [
    { offset: '100%', repeat: 0,   symbol_type: 'arrow',  symbol_options: { pixelSize: 8,  pathOptions:   { color: '#f00', weight: 2, stroke: true, }, }, icon_properties: { shadow: false, }, },
    { offset: 0,      repeat: 150, symbol_type: 'marker', symbol_options: { rotate: true,  markerOptions: { color: '#f00', icon: 'icon-svg-force_helicopter_route', }, }, icon_properties: { shadow: false, }, },
    { offset: 0,      repeat: 20,  symbol_type: 'dash',   symbol_options: { pixelSize: 10, pathOptions:   { color: '#f00', weight: 2, }, }, },
  ],
  // линия - Х - траектория вертолета закордон
  'line-force_helicopter_route_outside': [
    { offset: '100%', repeat: 0,   symbol_type: 'arrow',  symbol_options: { pixelSize: 8,  pathOptions:   { color: '#00f', weight: 2, stroke: true, }, }, icon_properties: { shadow: false, }, },
    { offset: 0,      repeat: 150, symbol_type: 'marker', symbol_options: { rotate: true,  markerOptions: { color: '#00f', icon: 'icon-svg-force_helicopter_route', }, }, icon_properties: { shadow: false, }, },
    { offset: 0,      repeat: 20,  symbol_type: 'dash',   symbol_options: { pixelSize: 10, pathOptions:   { color: '#00f', weight: 2, }, }, },
  ],
  // линия - Х - траектория вертолета прикордон
  'line-force_quadcopter_route_inside': [
    { offset: '100%', repeat: 0,   symbol_type: 'arrow',  symbol_options: { pixelSize: 8,  pathOptions:   { color: '#f00', weight: 2, stroke: true, }, }, icon_properties: { shadow: false, }, },
    { offset: 0,      repeat: 150, symbol_type: 'marker', symbol_options: { rotate: true,  markerOptions: { color: '#f00', icon: 'icon-svg-force_quadcopter_route', }, }, icon_properties: { shadow: false, }, },
    { offset: 0,      repeat: 20,  symbol_type: 'dash',   symbol_options: { pixelSize: 10, pathOptions:   { color: '#f00', weight: 2, }, }, },
  ],
  // линия - Х - траектория вертолета закордон
  'line-force_quadcopter_route_outside': [
    { offset: '100%', repeat: 0,   symbol_type: 'arrow',  symbol_options: { pixelSize: 8,  pathOptions:   { color: '#00f', weight: 2, stroke: true, }, }, icon_properties: { shadow: false, }, },
    { offset: 0,      repeat: 150, symbol_type: 'marker', symbol_options: { rotate: true,  markerOptions: { color: '#00f', icon: 'icon-svg-force_quadcopter_route', }, }, icon_properties: { shadow: false, }, },
    { offset: 0,      repeat: 20,  symbol_type: 'dash',   symbol_options: { pixelSize: 10, pathOptions:   { color: '#00f', weight: 2, }, }, },
  ],
}




export const SVG = {

}



export const TEST = [
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_manage_inside",
      "zoom":  false,
      "text":  '130 пого',
      "hint":  "icon-svg-force_manage_inside",
      "date":  "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [23.5,54.25],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_manage_outside",
      "zoom":  false,
      "text":  '150',
      "hint":  "icon-svg-force_manage_outside",
      "date":  "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [23.5,54.0],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_ops_inside",
      "text":  '"Прудок"',
      "hint":  "icon-svg-force_ops_inside",
      "date":  "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.0,54.25],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_frontier_inside",
      "text": "10",
      "hint": "icon-svg-force_frontier_inside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.5,54.25],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_frontier_outside",
      "text": "10",
      "hint": "icon-svg-force_frontier_outside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.5,54.0],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_guard_inside",
      "text": "12",
      "hint": "icon-svg-force_guard_inside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [25.0,54.25],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_guard_outside",
      "text": "12",
      "hint": "icon-svg-force_guard_outside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [25.0,54.0],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_guard_temp_inside",
      "text": "15",
      "hint": "icon-svg-force_guard_temp_inside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [25.5,54.25],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_unit_control_inside",
      "text": '"Зубренок"',
      "hint": "icon-svg-force_unit_control_inside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [26.0,54.25],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_unit_control_outside",
      "text": '"Дотишки"',
      "hint": "icon-svg-force_unit_control_outside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [26.0,54.0],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_point_observation_hidden",
      "hint": "icon-svg-force_point_observation_hidden",
      "date": "2021-05-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [26.5,54.25],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_point_observation_open",
      "hint": "icon-svg-force_point_observation_open",
      "date": "2021-05-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [26.5,54.0],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_point_control",
      "hint": "icon-svg-force_point_control",
      "date": "2021-05-09",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [27.0,54.25],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_patrol_inside",
      "hint": "icon-svg-force_patrol_inside",
      "rotate": 270,
      "date": "2021-06-09",
      "text": "Д-2чел-3погз",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [27.5,54.25],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_patrol_outside",
      "hint": "icon-svg-force_patrol_outside",
      "rotate": 90,
      "date": "2021-03-09",
      "text": "Д-3чел-2погз",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [27.5,54.0],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_helicopter_inside",
      "hint": "icon-svg-force_helicopter_inside",
      "date": "2021-06-09",
      "text": "МИ-8",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [28.0,54.25],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-force_helicopter_outside",
      "hint": "icon-svg-force_helicopter_outside",
      "date": "2021-06-09",
      "text": "Apache",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [28.0,54.0],
    },
  },




  {
    "type": "Feature",
    "properties": {
      "class": "line-force_helicopter_route_inside hidden",
      "hint": "line-force_helicopter_route_inside hidden",
      "date": "2021-05-03",
      //"color": "#888",
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [24.0,58.5],
        [27.5,59.5],
      ]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "line-force_quadcopter_route_outside hidden",
      "hint": "line-force_quadcopter_route_outside hidden",
      "date": "2021-05-03",
      //"color": "#888",
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [27.5,59.5],
        [32.0,58.5],
      ]
    },
  },
]
