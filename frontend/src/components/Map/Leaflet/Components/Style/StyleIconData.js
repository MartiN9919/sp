const DATA = {
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
            style="fill:#ff0000;stroke:#ff0000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none"
            d="m 42.678571,291.07738 -21.25,11.60714 21.607143,9.46428 c 0.178571,-22.32143 -0.357143,-21.07142 -0.357143,-21.07142 z"
          />
        </g>
      </svg>
    `,
  },

  //
  'checkpoint_auto': {
    anchor_dx: 45.,
    anchor_dy: 50.,
    zoom:      1.,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path
           style="fill:#ffffff;stroke:{color};stroke-width:4"
           d="M 3.8292234,72.585793 46.686366,3.4786426 96.59708,72.496513 Z"
        />
        <path
           style="fill:#ff0000;stroke:#ff0000;stroke-width:4"
           d="m 31.965985,38.367703 32.671297,-0.0415 -16.61163,28.456 z"
        />
        <text style="font-style:normal;font-weight:bold;font-size:22px;font-family:sans-serif">
          <tspan x="100" y="70">{text}</tspan>
        </text>
      </svg>
    `,
  },
  'checkpoint_flyer': {
    anchor_dx: 45.,
    anchor_dy: 50.,
    zoom:      1.,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path
           style="fill:#ffffff;stroke:{color};stroke-width:4"
           d="M 3.8292234,72.585793 46.686366,3.4786426 96.59708,72.496513 Z"
        />
        <path
           style="fill:#0000FF;stroke:#0000FF;stroke-width:4"
           d="m 31.965985,38.367703 32.671297,-0.0415 -16.61163,28.456 z"
        />
        <text style="font-style:normal;font-weight:bold;font-size:22px;font-family:sans-serif">
          <tspan x="100" y="70">{text}</tspan>
        </text>
      </svg>
    `,
  },
  'checkpoint_rail': {
    anchor_dx: 45.,
    anchor_dy: 50.,
    zoom:      1.,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path
           style="fill:#ffffff;stroke:{color};stroke-width:4"
           d="M 3.8292234,72.585793 46.686366,3.4786426 96.59708,72.496513 Z"
        />
        <path
           style="fill:#000000;stroke:#000000;stroke-width:4"
           d="m 31.965985,38.367703 32.671297,-0.0415 -16.61163,28.456 z"
        />
        <text style="font-style:normal;font-weight:bold;font-size:22px;font-family:sans-serif">
          <tspan x="100" y="70">{text}</tspan>
        </text>
      </svg>
    `,
  },
  'checkpoint_simplified': {
    anchor_dx: 45.,
    anchor_dy: 50.,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path
           style="fill:#ffffff;stroke:{color};stroke-width:4"
           d="M 3.8,71.2 45.3,3.5 93.7,71.1 Z"
        />
        <path
           style="fill:#ff0000;stroke:#fe0000;stroke-width:0.97479194px"
           d="M 45.6,3.5 46.2,71.1 94.0,71.2 45.6,3.5"
        />
        <text style="font-style:normal;font-weight:bold;font-size:22px;font-family:sans-serif">
          <tspan x="100" y="70">{text}</tspan>
        </text>
      </svg>
    `,
  },



  'place_cp': {
    anchor_dx: 0,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 200 100">
        <path
          style="fill:#ffffff;stroke:{color};stroke-width:4"
          d="M 2.2,99.8 V 2.2 H 90.0 L 70.0,38.6 2.3,38.6"
        />
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif">
            <tspan x="6" y="25">{text}</tspan>
        </text>
        <text style="font-style:normal;font-weight:normal;font-size:35px;font-family:sans-serif">
            <tspan x="17" y="99">КП</tspan>
        </text>
      </svg>
    `,
  },
  'place_ops': {
    anchor_dx: 0,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 200 100">
        <path
           style="fill:#ffffff;stroke:{color};stroke-width:4"
           d="M 2.4354161,99.822978 V 2.5810581 H 71.529824 L 2.6211544,46.900936"
        />
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif">
          <tspan x="6" y="20">ОПС</tspan>
        </text>
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif">
          <tspan x="6" y="96">{text}</tspan>
        </text>
      </svg>
    `,
  },
  'place_outpost': {
    anchor_dx: 0,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 55 100">
        <path
          style="fill:#ffffff;stroke:{color};stroke-width:4"
          d="M 2.2036433,100 V 3.312438 L 50.729628,25.10104 2.2036433,47.805112"
        />
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif">
          <tspan x="6" y="29">{text}</tspan>
        </text>
      </svg>
    `,
  },
  'place_post': {
    anchor_dx: 0,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 57 100">
        <path
          style="fill:#ffffff;stroke:{color};stroke-width:4"
          d="M 2.3,100.15925 V 4.2910497 L 51.601627,42 2.3,42"
        />
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif">
          <tspan x="6" y="35">{text}</tspan>
        </text>
      </svg>
    `,
  },
  'place_post_temp': {
    anchor_dx: 0,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 60 102">
        <path
          style="fill:#ffffff;stroke:{color};stroke-width:4"
          d="M 7,94 V 4.2910497 L 55,43 7,43"
        />
        <ellipse style="opacity:1;fill:#ff0000;stroke:#ff0000;stroke-width:2" cx="7" cy="94" rx="5" ry="5"/>
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif">
          <tspan x="10" y="35">{text}</tspan>
        </text>
      </svg>
    `,
  },
  'place_post_control': {
    anchor_dx: 0,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 200 100">
        <path
          style="fill:#ffffff;stroke:{color};stroke-width:4"
          d="M 1.9,100 2.6,22.7 2.5,3.2 44.0,23.5 2.1,41.0"
        />
        <path
          style="fill:#ff0000;stroke:#ff0000;stroke-width:1px"
          d="M 22.6,13.1 3.0,22.6 22.8,32.2 44.0,23.5 Z"
        />
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif">
          <tspan x="6" y="96">{text}</tspan>
        </text>
      </svg>
    `,
  },


}


const ZOOM_DOP = .5;
let regexp_vb  = /<svg[^>]*viewBox\s*=\s*"\s*0\s*0\s*(?<width>\d+(?:\.\d+)?)\s*(?<height>\d+(?:\.\d+)?)\s*"/mi;
export function get_icon_data(key, color="gray", zoom=1, text=undefined) {
  let data = DATA[key];
  if (data === undefined) return;
  if (text === undefined) text = '';
  let svg  = JSON.parse(JSON.stringify(data.svg)).replace(/{color}/g, color).replace(/{text}/g, text);
  let svg_size   = svg.match(regexp_vb)?.groups;
  let svg_width  = svg_size?.width;
  let svg_height = svg_size?.height;
  if ((svg_width==undefined) || (svg_height==undefined)) return;
  let zoom_common = zoom*ZOOM_DOP*(data.zoom??1.);
  svg_width  = svg_width *zoom_common;//|0;
  svg_height = svg_height*zoom_common;//|0;
  return {
    svg:       svg.replace(/{width}/g, svg_width).replace(/{height}/g, svg_height),
    width:     svg_width,
    height:    svg_height,
    anchor_dx: (data.anchor_dx!==undefined) ? data.anchor_dx*zoom_common : svg_width /2,      // точка привязки svg относительно верхнего левого угла
    anchor_dy: (data.anchor_dy!==undefined) ? data.anchor_dy*zoom_common : svg_height/2,      // по умолчанию: центр svg
  }
}
