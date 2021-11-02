export const STYLE_DATA_ENGENEER_ICON = {
  'engineer_border_sign': {
    anchor_dx: 50,
    anchor_dy: 50.,
    zoom:      .5,
    svg: `
      <svg width={width} height={height} viewBox="0 0 500 130">
        <circle style="fill:#fff;stroke:#000;stroke-width:4" cx="50" cy="50" r="23"/>
        <circle style="fill:#000" cx="50" cy="50" r="8"/>
        <text style="font-style:normal;font-weight:bold;font-size:45px;font-family:sans-serif" x="0" y="115">{text}</text>
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
        <path style="fill:#fff;stroke:#000;stroke-width:4" d="m 3.53,91.11 h 60 l -30,-75.00 z"/>
        <path style="fill:#fff;stroke:#000;stroke-width:4" d="m 12.53,11.11 h 40 l 6,-10.00 -2,3 h -48 l -2,-3 z"/>
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
    symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-file-zabor_ogradit-10-10', }, },
    icon_properties: { shadow: false, },
  },
}
