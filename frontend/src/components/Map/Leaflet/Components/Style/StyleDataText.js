// текст для линий

const PREF = {
  anchor_dx: 14,
  anchor_dy: 0,
  zoom:      .8,
}

export const ICON = {
  'text_line_rl_fill_100': { ...PREF,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 100">
        <rect x="-10" y="-2" width="38" height="102" fill="#fff" />
        <text class="ddd" style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(90)" x="50" y="-3">{text}</text>
      </svg>
    `,
  },
  'text_line_lr_fill_100': { ...PREF,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 100">
        <rect x="-10" y="-2" width="38" height="102" fill="#fff" />
        <text class="ddd" style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(270)" x="-50" y="26">{text}</text>
      </svg>
    `,
  },
  'text_line_rl_fill_300': { ...PREF,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 300">
        <rect x="-10" y="-2" width="38" height="302" fill="#fff" />
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(90)" x="150" y="-3">{text}</text>
      </svg>
    `,
  },
  'text_line_lr_fill_300': { ...PREF,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 300">
        <rect x="-10" y="-2" width="38" height="302" fill="#fff" />
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(270)" x="-150" y="26">{text}</text>
      </svg>
    `,
  },
  'text_line_rl_100': { ...PREF,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 100">
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(90)" x="50" y="-3">{text}</text>
      </svg>
    `,
  },
  'text_line_lr_100': { ...PREF,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 100">
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(270)" x="-50" y="26">{text}</text>
      </svg>
    `,
  },
  'text_line_rl_300': { ...PREF,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 300">
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(90)" x="150" y="-3">{text}</text>
      </svg>
    `,
  },
  'text_line_lr_300': { ...PREF,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 300">
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(270)" x="-150" y="26">{text}</text>
      </svg>
    `,
  },
};



export const DECOR = {
  'line-text_rl_fill_100': { offset: 8, repeat: 300, symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-text_line_rl_fill_100', }, }, icon_properties: { shadow: false, top: true, }, },
  'line-text_lr_fill_100': { offset: 8, repeat: 300, symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-text_line_lr_fill_100', }, }, icon_properties: { shadow: false, top: true, }, },
  'line-text_rl_fill_300': { offset: 8, repeat: 300, symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-text_line_rl_fill_300', }, }, icon_properties: { shadow: false, top: true, }, },
  'line-text_lr_fill_300': { offset: 8, repeat: 300, symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-text_line_lr_fill_300', }, }, icon_properties: { shadow: false, top: true, }, },
  'line-text_rl_100':      { offset: 8, repeat: 300, symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-text_line_rl_100',      }, }, icon_properties: { shadow: false, top: true, }, },
  'line-text_lr_100':      { offset: 8, repeat: 300, symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-text_line_lr_100',      }, }, icon_properties: { shadow: false, top: true, }, },
  'line-text_rl_300':      { offset: 8, repeat: 300, symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-text_line_rl_300',      }, }, icon_properties: { shadow: false, top: true, }, },
  'line-text_lr_300':      { offset: 8, repeat: 300, symbol_type: 'marker', symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-text_line_lr_300',      }, }, icon_properties: { shadow: false, top: true, }, },
}



export const STYLE_DATA_TEXT_TEST = [

]
