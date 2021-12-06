export const ICON = {
  'engineer_border_sign': {
    anchor_dx: 100,
    anchor_dy: 50.,
    zoom:      .7,   // .5;
    svg: `
      <svg width={width} height={height} viewBox="0 0 200 125">
        <circle style="fill:#fff;stroke:#555;stroke-width:4" cx="100" cy="50" r="23"/>
        <circle style="fill:#555" cx="100" cy="50" r="8"/>
        <text style="font-style:normal;font-size:35px;font-family:sans-serif;text-anchor:middle" x="100" y="120">{text}</text>
      </svg>
    `,
  },

  // видео, фото
  'engineer_video': {
    anchor_dx: 100,
    anchor_dy: 20.,
    zoom:      .7,  // .5
    svg: `
      <svg width={width} height={height} viewBox="0 0 200 95">
        <rect style="fill:#fff;stroke:#555;stroke-width:2" width="70" height="40" x="60" y="1"/>
        <rect style="fill:#555;stroke-width:2" width="70"  height="13" x="60" y="27"/>
        <path style="fill:#555;stroke:#555;stroke-width:2" d="M135,20 155,1 155,40 Z"/>
        <text style="font-style:normal;font-size:35px;font-family:sans-serif;text-anchor:middle" x="100" y="90">{text}</text>
      </svg>
    `,
  },


  // КСП
  'engeneer_ksp': {
    anchor_dx: 20,
    anchor_dy: 10,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 40 20">
        <path style="fill:none;stroke:#888;stroke-width:4;" d="M2,0 V20 M4,10 H40 M38,0 v20"/>
      </svg>
    `,
  },


  // вышка промышленная
  'engineer_tower_industrial': {
    anchor_dx: 150,
    anchor_dy: 94.,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 300 130">
        <path style="fill:#fff;stroke:#555;stroke-width:4" d="M120.53,91.11 h60 l-30,-75.00 z"/>
        <path style="fill:#fff;stroke:#555;stroke-width:4" d="M129.53,11.11 h40 l6,-10.00 -2,3 h-48 l-2,-3 z"/>
        <text style="font-style:normal;font-size:25px;font-family:sans-serif;text-anchor:middle" x="150" y="125">{text}</text>
      </svg>
    `,
  },

  // Заграждение сигнализация -|-|-
  'engeneer_zagr_signal': {
    anchor_dx: 24,
    anchor_dy: 5,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 40 10">
        <path style="fill:none;stroke:#888;stroke-width:10;" d="m5,0 h40"/>
      </svg>
    `,
  },

  // Заграждение малозам 0-0-0
  'engeneer_zagr_invisible': {
    anchor_dx: 16,
    anchor_dy: 5,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 32 26">
        <path
          style="fill:none;stroke:#888;stroke-width:3"
          d="m 0.50,0.07 c 0,0 3.81,27.26 19.45,22.63 C 26.08,20.88 29.99,18.37 30.37,13.80 30.63,10.65 27.60,6.59 20.45,4.26 4.22,-1.45 -0.18,28.26 1.0,25.75"
        />
      </svg>
    `,
  },

  // Забор оградительный х-х-х
  'engeneer_zagr_ograd': {
    anchor_dx: 18,
    anchor_dy: 15,
    zoom:      .7,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 30">
        <path style="fill:none;stroke:{color};stroke-width:4" d="M0,0 L30 30 M30,0 L0,30" />
      </svg>
    `,
  }

}


export const DECOR = {
  // КСП
  'line-engeneer_ksp': {
    offset: 8, repeat: 8,
    symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-engeneer_ksp', }, },
    icon_properties: { shadow: false, },
  },

  // Заграждение сигнализация -|-|-
  'line-engeneer_zagr_signal': {
    offset: 8, repeat: 18,
    symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-engeneer_zagr_signal', }, },
    icon_properties: { shadow: false, },
  },

  // Заграждение малозам 0-0-0
  'line-engeneer_zagr_invisible': {
    offset: 8, repeat: 9,
    symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-engeneer_zagr_invisible', }, },
    icon_properties: { shadow: false, },
  },

  // Забор оградительный х-х-х
  'line-engeneer_zagr_ograd': {
    offset: 8, repeat: 30,
    symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-engeneer_zagr_ograd', }, },
    icon_properties: { shadow: false, },
  },
}



export const SVG = {

}



export const TEST = [
  {
    "type": "Feature",
    "properties": {
      "class": "arc-layout-start-180 arrow-layout-double-end line-engeneer_zagr_signal line-text_rl_fill_100 ant",
      "hint": "arc-layout-start-180 arrow-layout-double-end line-engeneer_zagr_signal line-text_rl_fill_100 ant",
      "date": "2021-01-04 18:36",
      "text": "C-120",
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [32.0,56.5],
        [27.5,57.5],
        [24.0,56.5],
      ]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "arc-layout-start arrow-layout-double-end line-engeneer_zagr_signal line-text_lr_300 ant",
      "hint": "arc-layout-start arrow-layout-double-end line-engeneer_zagr_signal line-text_lr_300 ant",
      "date": "2021-01-04 02:10",
      "text": "C-120",
      // "zoom": 2,
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [24.0,56.0],
        [27.5,57.0],
        [32.0,56.0],
      ]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "line-engeneer_zagr_invisible hidden",
      "hint": "line-engeneer_zagr_invisible hidden",
      "date": "2021-05-04 03:45",
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [24.0,57.0],
        [27.5,58.0],
        [32.0,57.0],
      ]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "line-engeneer_zagr_ograd",
      "hint": "line-engeneer_zagr_ograd",
      "date": "2021-05-04 02:55",
      "color": "#888",
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [24.0,57.5],
        [27.5,58.5],
        [32.0,57.5],
      ]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "line-engeneer_ksp hidden",
      "hint": "line-engeneer_ksp hidden",
      "date": "2021-09-04 16:52",
      //"color": "#888",
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [24.0,58.0],
        [27.5,59.0],
        [32.0,58.0],
      ]
    },
  },







  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-engineer_border_sign",
      "text": "1234",
      "hint": "icon-svg-engineer_border_sign",
      "date": "2021-03-01 00:00",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.0,53.25],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-engineer_video",
      "text": "1234",
      "hint": "icon-svg-engineer_video",
      "date": "2021-04-01 00:01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.5,53.25],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-engineer_tower_industrial",
      "text": '"Зоркий"',
      "hint": "icon-svg-engineer_tower_industrial",
      "date": "2021-02-01 23:59",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [25.0,53.25],
    },
  },
]
