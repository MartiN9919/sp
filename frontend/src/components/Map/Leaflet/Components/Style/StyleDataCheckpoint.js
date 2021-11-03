const PREF_INSIDE = {
  anchor_dx: 45.,
  anchor_dy: 50.,
  zoom:      1.,
}
const PREF_OUTSIDE = {
  anchor_dx: 275.,
  anchor_dy: 50.,
  zoom:      1.,
}

export const STYLE_DATA_CHECKPOINT_ICON = {
  'checkpoint_auto_inside': { ...PREF_INSIDE,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#f00;stroke-width:4" d="M 3.8,72.6 46.7,3.5 96.6,72.5 Z"/>
        <path style="fill:#f00;stroke:#f00;stroke-width:4" d="m 32.0,38.4 32.7,-0.0 -16.6,28.5 z"/>
        <text style="font-style:normal;font-size:22px;font-family:sans-serif" x="100" y="70">{text}</text>
      </svg>
    `,
  },
  'checkpoint_auto_outside': { ...PREF_OUTSIDE,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#00f;stroke-width:4" d="m 223.3,72.1 42.9,-69.1 49.9,69.0 z"/>
        <path style="fill:#f00;stroke:#f00;stroke-width:4" d="m 251.5,37.9 h 32.7 l -16.6,28.5 z"/>
        <text style="font-style:normal;font-size:22px;font-family:sans-serif;text-anchor:end" x="220" y="70">{text}</text>
      </svg>
    `,
  },
  'checkpoint_flyer_inside': { ...PREF_INSIDE,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#f00;stroke-width:4" d="M 3.8,72.6 46.7,3.5 96.6,72.5 Z"/>
        <path style="fill:#00f;stroke:#00f;stroke-width:4" d="m 32.0,38.4 32.7,-0.0 -16.6,28.5 z"/>
        <text style="font-style:normal;font-size:22px;font-family:sans-serif" x="100" y="70">{text}</text>
      </svg>
    `,
  },
  'checkpoint_flyer_outside': { ...PREF_OUTSIDE,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#00f;stroke-width:4" d="m 223.3,72.1 42.9,-69.1 49.9,69.0 z"/>
        <path style="fill:#00f;stroke:#00f;stroke-width:4" d="m 251.5,37.9 h 32.7 l -16.6,28.5 z"/>
        <text style="font-style:normal;font-size:22px;font-family:sans-serif;text-anchor:end" x="220" y="70">{text}</text>
      </svg>
    `,
  },
  'checkpoint_rail_inside': { ...PREF_INSIDE,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#f00;stroke-width:4" d="M 3.8,72.6 46.7,3.5 96.6,72.5 Z"/>
        <path style="fill:#000;stroke:#000;stroke-width:4" d="m 31.9,38.4 32.7,-0.0 -16.6,28.5 z"/>
        <text style="font-style:normal;font-size:22px;font-family:sans-serif" x="100" y="70">{text}</text>
      </svg>
    `,
  },
  'checkpoint_rail_outside': { ...PREF_OUTSIDE,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#00f;stroke-width:4" d="m 223.3,72.1 42.9,-69.1 49.9,69.0 z"/>
        <path style="fill:#000;stroke:#000;stroke-width:4" d="m 251.5,37.9 h 32.7 l -16.6,28.5 z"/>
        <text style="font-style:normal;font-size:22px;font-family:sans-serif;text-anchor:end" x="220" y="70">{text}</text>
      </svg>
    `,
  },
  'checkpoint_simplified_inside': { ...PREF_INSIDE,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#f00;stroke-width:4" d="M 3.8,71.2 45.3,3.5 93.7,71.1 Z"/>
        <path style="fill:#f00;stroke:#f00;stroke-width:1" d="M 45.6,3.5 46.2,71.1 94.0,71.2 45.6,3.5"/>
        <text style="font-style:normal;font-size:22px;font-family:sans-serif" x="100" y="70">{text}</text>
      </svg>
    `,
  },
  'checkpoint_simplified_outside': { ...PREF_OUTSIDE,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#00f;stroke-width:4" d="m 226.17,71.7 41.5,-67.7 48.4,67.6 z"/>
        <path style="fill:#00f;stroke:#00f;stroke-width:1" d="m 267.97,4.0 0.6,67.6 47.8,0.1 -48.4,-67.7"/>
        <text style="font-style:normal;font-size:22px;font-family:sans-serif;text-anchor:end" x="220" y="70">{text}</text>
      </svg>
    `,
  },
}



export const STYLE_DATA_CHECKPOINT_DECOR = {

}



export const STYLE_DATA_CHECKPOINT_TEST = [
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-checkpoint_auto_inside",
      "text":  '"Молодечненское"',
      "hint": "icon-svg-checkpoint_auto_inside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.0,53.75],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-checkpoint_auto_outside",
      "text":  '"Labas denas"',
      "hint": "icon-svg-checkpoint_auto_outside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.0,53.50],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-checkpoint_flyer_inside",
      "text":  '"Высокое"',
      "hint": "icon-svg-checkpoint_flyer_inside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.5,53.75],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-checkpoint_flyer_outside",
      "text":  '"Высокое"',
      "hint": "icon-svg-checkpoint_flyer_outside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.5,53.50],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-checkpoint_rail_inside",
      "text":  '"Стальное"',
      "hint": "icon-svg-checkpoint_rail_inside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [25.0,53.75],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-checkpoint_rail_outside",
      "text":  '"Bruzg"',
      "hint": "icon-svg-checkpoint_rail_outside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [25.0,53.50],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-checkpoint_simplified_inside",
      "text":  '"Леший"',
      "hint": "icon-svg-checkpoint_simplified_inside",
      "date": "2021-01-02",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [25.5,53.75],
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-checkpoint_simplified_outside",
      "text":  '"Швiденькi"',
      "hint": "icon-svg-checkpoint_simplified_outside",
      "date": "2021-01-02",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [25.5,53.50],
    },
  },
]