export const STYLE_DATA_POST_ICON = {
  'base_manage_inside': {
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
  'base_manage_outside': {
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
  'base_ops_inside': {
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
  'post_frontier_inside': {
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
  'post_frontier_outside': {
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
  'post_simple_inside': {
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
  'post_simple_outside': {
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
  'post_temp_inside': {
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
  'post_control_inside': {
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
  'post_control_outside': {
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
  'post_observation_hidden': {
    anchor_dx: 40.,
    anchor_dy: 40.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 80 80">
        <path style="fill:#fff;stroke:#444;stroke-width:2" d="M 1,1 V 79 H 79 V 1 Z m 9,9 H 70 M 40.5,13 4,70 h 72 z"/>
      </svg>
    `,
  },
}





export const STYLE_DATA_POST_DECOR = {

}





export const STYLE_DATA_POST_TEST = [
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-base_manage_inside",
      "zoom":  false,
      "text":  '130 пого',
      "hint":  "icon-svg-base_manage_inside",
      "date":  "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [23.5,54.25]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-base_manage_outside",
      "zoom":  false,
      "text":  '150',
      "hint":  "icon-svg-base_manage_outside",
      "date":  "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [23.5,54.0]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-base_ops_inside",
      "text":  '"Прудок"',
      "hint":  "icon-svg-base_ops_inside",
      "date":  "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.0,54.25]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-post_frontier_inside",
      "text": "10",
      "hint": "icon-svg-post_frontier_inside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.5,54.25]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-post_frontier_outside",
      "text": "10",
      "hint": "icon-svg-post_frontier_outside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [24.5,54.0]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-post_simple_inside",
      "text": "12",
      "hint": "icon-svg-post_simple_inside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [25.0,54.25]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-post_simple_outside",
      "text": "12",
      "hint": "icon-svg-post_simple_outside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [25.0,54.0]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-post_temp_inside",
      "text": "15",
      "hint": "icon-svg-post_temp_inside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [25.5,54.25]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-post_control_inside",
      "text": '"Зубренок"',
      "hint": "icon-svg-post_control_inside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [26.0,54.25]
    },
  },
  {
    "type": "Feature",
    "properties": {
      "class": "icon-svg-post_control_outside",
      "text": '"Дотишки"',
      "hint": "icon-svg-post_control_outside",
      "date": "2021-01-01",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [26.0,54.0]
    },
  },
]
