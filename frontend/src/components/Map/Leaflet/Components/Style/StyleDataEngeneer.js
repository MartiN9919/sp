export const STYLE_DATA_ENGENEER_ICON = {
  'engineer_border_sign': {
    anchor_dx: 100,
    anchor_dy: 50.,
    zoom:      .5,
    svg: `
      <svg width={width} height={height} viewBox="0 0 200 125">
        <circle style="fill:#fff;stroke:#000;stroke-width:4" cx="100" cy="50" r="23"/>
        <circle style="fill:#000" cx="100" cy="50" r="8"/>
        <text style="font-style:normal;font-size:40px;font-family:sans-serif;text-anchor:middle" x="100" y="120">{text}</text>
      </svg>
    `,
  },

  // видео, фото
  'engineer_video': {
    anchor_dx: 100,
    anchor_dy: 20.,
    zoom:      .5,
    svg: `
      <svg width={width} height={height} viewBox="0 0 200 95">
        <rect style="fill:#fff;stroke:#000;stroke-width:2" width="70" height="40" x="60" y="1"/>
        <rect style="fill:#000;stroke-width:2" width="70"  height="13" x="60" y="27"/>
        <path style="fill:#000;stroke:#000;stroke-width:2" d="M 135,20 155,1 155,40 Z"/>
        <text style="font-style:normal;font-size:37px;font-family:sans-serif;text-anchor:middle" x="100" y="90">{text}</text>
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
        <path style="fill:#fff;stroke:#000;stroke-width:4" d="M 120.53,91.11 h 60 l -30,-75.00 z"/>
        <path style="fill:#fff;stroke:#000;stroke-width:4" d="M 129.53,11.11 h 40 l 6,-10.00 -2,3 h -48 l -2,-3 z"/>
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
        <path style="fill:none;stroke:#888;stroke-width:10;" d="m 5,0 h 40"/>
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
    anchor_dx: 15,
    anchor_dy: 15,
    zoom:      .7,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 30">
        <path style="fill:none;stroke:#888;stroke-width:4" d="M 0,0 L 30 30 M 30,0 L 0,30" />
      </svg>
    `,
  }

}


export const STYLE_DATA_ENGENEER_DECOR = {
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
