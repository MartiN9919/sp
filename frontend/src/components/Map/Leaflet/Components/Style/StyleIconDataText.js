// текст для линий
export const STYLE_ICON_DATA_TEXT = {
  'text_line_rl_fill_100': {
    anchor_dx: 14,
    anchor_dy: 0,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 100">
        <rect x="-10" y="-2" width="38" height="102" fill="#fff" />
        <text class="ddd" style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(90)" x="50" y="-3">{text}</text>
      </svg>
    `,
  },
  'text_line_lr_fill_100': {
    anchor_dx: 14,
    anchor_dy: 0,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 100">
        <rect x="-10" y="-2" width="38" height="102" fill="#fff" />
        <text class="ddd" style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(270)" x="-50" y="26">{text}</text>
      </svg>
    `,
  },
  'text_line_rl_fill_300': {
    anchor_dx: 14,
    anchor_dy: 0,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 300">
        <rect x="-10" y="-2" width="38" height="302" fill="#fff" />
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(90)" x="150" y="-3">{text}</text>
      </svg>
    `,
  },
  'text_line_lr_fill_300': {
    anchor_dx: 14,
    anchor_dy: 0,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 300">
        <rect x="-10" y="-2" width="38" height="302" fill="#fff" />
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(270)" x="-150" y="26">{text}</text>
      </svg>
    `,
  },
  'text_line_rl_100': {
    anchor_dx: 14,
    anchor_dy: 0,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 100">
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(90)" x="50" y="-3">{text}</text>
      </svg>
    `,
  },
  'text_line_lr_100': {
    anchor_dx: 14,
    anchor_dy: 0,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 100">
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(270)" x="-50" y="26">{text}</text>
      </svg>
    `,
  },
  'text_line_rl_300': {
    anchor_dx: 14,
    anchor_dy: 0,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 300">
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(90)" x="150" y="-3">{text}</text>
      </svg>
    `,
  },
  'text_line_lr_300': {
    anchor_dx: 14,
    anchor_dy: 0,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 300">
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(270)" x="-150" y="26">{text}</text>
      </svg>
    `,
  },
}
