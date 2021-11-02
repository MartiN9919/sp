export const STYLE_DATA_ENGENEER_ICON = {
  'engineer_border_sign': {
    anchor_dx: 100,
    anchor_dy: 50.,
    zoom:      .5,
    svg: `
      <svg width={width} height={height} viewBox="0 0 200 115">
        <circle style="fill:#fff;stroke:#000;stroke-width:4" cx="100" cy="50" r="23"/>
        <circle style="fill:#000" cx="100" cy="50" r="8"/>
        <text style="font-style:normal;font-weight:bold;font-size:45px;font-family:sans-serif;text-anchor:middle" x="100" y="115">{text}</text>
      </svg>
    `,
  },

  // видео, фото
  'engineer_video': {
    anchor_dx: 100,
    anchor_dy: 20.,
    zoom:      .5,
    svg: `
      <svg width={width} height={height} viewBox="0 0 200 85">
        <rect style="fill:#fff;stroke:#000;stroke-width:2" width="70" height="40" x="60" y="1"/>
        <rect style="fill:#000;stroke-width:2" width="70"  height="13" x="60" y="27"/>
        <path style="fill:#000;stroke:#000;stroke-width:2" d="M 135,20 155,1 155,40 Z"/>
        <text style="font-style:normal;font-weight:bold;font-size:45px;font-family:sans-serif;text-anchor:middle" x="100" y="85">{text}</text>
      </svg>
    `,
  },

  // вышка промышленная
  'engineer_tower_industrial': {
    anchor_dx: 33,
    anchor_dy: 94.,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 300 94">
        <path style="fill:#fff;stroke:#000;stroke-width:4" d="M 3.53,91.11 h 60 l -30,-75.00 z"/>
        <path style="fill:#fff;stroke:#000;stroke-width:4" d="M 12.53,11.11 h 40 l 6,-10.00 -2,3 h -48 l -2,-3 z"/>
        <text style="font-style:normal;font-weight:bold;font-size:32px;font-family:sans-serif" x="66" y="88">{text}</text>
      </svg>
    `,
  },

  // Заграждение сигнализация -|-|-
  'engeneer_signal': {
    anchor_dx: 24,
    anchor_dy: 5,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 40 10">
        <path style="fill:none;stroke:#888;stroke-width:10;" d="m 5,0 h 40"/>
      </svg>
    `,
  },

  // Забор оградительный х х х
  'engeneer_ograd': {
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
  'line-engeneer_signal': {
    offset: 8, repeat: 18,
    symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-engeneer_signal', }, },
    icon_properties: { shadow: false, },
  },

  // Забор оградительный х х х
  'line-engeneer_ograd': {
    offset: 8, repeat: 30,
    symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-engeneer_ograd', }, },
    icon_properties: { shadow: false, },
  },
}
