// РАЗРАБОТКА
export const STYLE_DATA_TEST_ICON = {
  // стрелка: <=>
  'test1': {
    anchor_dx: 0,
    anchor_dy: 0,
    svg: `
      <svg fill="{color}" width={width} height={height} viewBox="0 0 101 33">
        <path d='M1,17 L21,1 L21,33 Z'/>
        <path d='M101,17 L82,1 L82,33 Z'/>
        <rect x="20" y="6" width="64" height="5" />
        <rect x="20" y="23" width="64" height="5" />
      </svg>
    `,
  },

  //
  'test2': {
    anchor_dx: 3,
    anchor_dy: 100,
    svg: `
      <svg fill="{color}" width={width} height={height} viewBox="0 0 100 100">
        <g transform="translate(0,-270.54166)">
          <path
            style="fill:none;stroke:{color};stroke-width:4;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none"
            d="m 16.071429,363.75595 v -43.75 -42.5 0 0 l 71.25,26.25 -70.892858,22.32142"
          />
          <path
            style="fill:#ff0000;stroke:#f00;stroke-width:4;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none"
            d="m 42.678571,291.07738 -21.25,11.60714 21.607143,9.46428 c 0.178571,-22.32143 -0.357143,-21.07142 -0.357143,-21.07142 z"
          />
        </g>
      </svg>
    `,
  },
}





export const STYLE_DATA_TEST_DECOR = {

}





export const STYLE_DATA_TEST_TEST = [
  // "style": {
  //   "marker": {
  //     "icon": "test",     // "mdi-flag mdi-spin", "fs-spec0", "pulse" (size: 12), "#0f0", "gold", "file_name" (size_w: 25, size_h: 41)
  //     "zoom": 2,
  //   },
  //   "line": {
  //     "class": "test_mark_auto arrow-double-end",
  //   },
  {
    "type": "Feature",
    "properties": {
      "hint": "Подсказка 2",
      "date": "2021-01-05 09:00",
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [
        [
          [30.0,54.5],
          [32.0,53.5],
          [30.0,52.5],
          [30.0,54.5],
        ]
      ]
    },
  },

  {
    "type": "Feature",
    "properties": {
      "class": "icon-mdi-flag sss icon-mdi-spin tst",
      "hint": "Demo",
      "date": "2021-01-03",
      //"zoom": false,
    },
    "geometry": {
      "type": "Point",
      "coordinates": [45,53.0],
    },
  },
]
