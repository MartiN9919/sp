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
    svg: `
      <svg width={width} height={height} viewBox="0 0 100 74">
        <path
           style="fill:#ffffff;stroke:{color};stroke-width:4"
           d="M 3.8292234,72.585793 46.686366,3.4786426 96.59708,72.496513 Z"
        />
        <path
           style="fill:#ff0000;stroke:#ff0000;stroke-width:4"
           d="m 31.965985,38.367703 32.671297,-0.0415 -16.61163,28.456 z"
        />
      </svg>
    `,
  },
  'checkpoint_flyer': {
    svg: `
      <svg width={width} height={height} viewBox="0 0 100 74">
        <path
           style="fill:#ffffff;stroke:{color};stroke-width:4"
           d="M 3.8292234,72.585793 46.686366,3.4786426 96.59708,72.496513 Z"
        />
        <path
           style="fill:#000080;stroke:#000080;stroke-width:4"
           d="m 31.965985,38.367703 32.671297,-0.0415 -16.61163,28.456 z"
        />
      </svg>
    `,
  },
  'checkpoint_rail': {
    svg: `
      <svg width={width} height={height} viewBox="0 0 98.490715 73.707695">
        <path
           style="fill:#ffffff;stroke:{color};stroke-width:4"
           d="M 3.8292234,72.585793 46.686366,3.4786426 96.59708,72.496513 Z"
        />
        <path
           style="fill:#000000;stroke:#000000;stroke-width:4"
           d="m 31.965985,38.367703 32.671297,-0.0415 -16.61163,28.456 z"
        />
      </svg>
    `,
  },
  'checkpoint_simplified': {
    svg: `
      <svg width={width} height={height} viewBox="0 0 97.206421 73.215599">
        <path
           style="fill:#ffffff;stroke:{color};stroke-width:4"
           d="M 3.7797086,71.212431 45.327076,3.4753509 93.712449,71.124921 Z"
        />
        <path
           style="fill:#ff0000;stroke:#fe0000;stroke-width:0.97479194px"
           d="M 45.571896,3.5372209 46.246954,71.072261 93.957269,71.186801 45.571896,3.5372209"
        />
      </svg>
    `,
  },



  'place_ops': {
    anchor_dx: 0,
    anchor_dy: 100.,
    zoom:      1.5,
    svg: `
      <svg width={width} height={height} viewBox="0 0 150 100">
        <path
           style="fill:#ffffff;stroke:{color};stroke-width:4"
           d="M 2.4354161,99.822978 V 2.5810581 H 71.529824 L 2.6211544,46.900936"
        />
        <text style="font-style:normal;font-weight:bold;font-size:16px;line-height:1.25;font-family:sans-serif">
          <tspan x="6" y="20">ОПС</tspan>
        </text>
        <text style="font-style:normal;font-weight:bold;font-size:16px;line-height:1.25;font-family:sans-serif">
          <tspan x="6" y="90">{text}</tspan>
        </text>
      </svg>
    `,
  },
  'place_outpost': {
    anchor_dx: 0,
    anchor_dy: 100.,
    zoom:      1.2,
    svg: `
      <svg width={width} height={height} viewBox="0 0 55.537838 100">
        <path
          style="fill:#ffffff;stroke:{color};stroke-width:4"
          d="M 2.2036433,100 V 3.312438 L 50.729628,25.10104 2.2036433,47.805112"
        />
        <text style="font-style:normal;font-weight:bold;font-size:16px;line-height:1.25;font-family:sans-serif">
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
      <svg width={width} height={height} viewBox="0 0 55.537838 100">
        <path
          style="fill:#ffffff;stroke:{color};stroke-width:4"
          d="M 2.2036433,100 V 3.312438 L 50.729628,25.10104 2.2036433,47.805112"
        />
        <text style="font-style:normal;font-weight:bold;font-size:16px;line-height:1.25;font-family:sans-serif">
          <tspan x="6" y="29">{text}</tspan>
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
