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
  'test3': {
    // anchor_dx: 0,
    // anchor_dy: 100,
    svg: `
      <svg fill="{color}" width={width} height={height} viewBox="0 0 55 100">
        <path
           style="fill:#ffffff;stroke:#ff0000;stroke-width:4.12501621;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
           d="M 2.2036433,100.17097 V 3.312438 L 50.729628,25.10104 2.2036433,47.805112"
        />
      </svg>
    `,
  },
}


let regexp_vb     = /<svg[^>]*viewBox\s*=\s*"\s*0\s*0\s*(?<width>\d+)\s*(?<height>\d+)\s*"/mi;
export function get_icon_data(key, color="gray", zoom=1) {
  let data = DATA[key];
  if (data === undefined) return;
  let svg  = JSON.parse(JSON.stringify(data.svg)).replace(/{color}/g, color);
  let svg_size   = svg.match(regexp_vb)?.groups;
  let svg_width  = svg_size?.width;
  let svg_height = svg_size?.height;
  if ((svg_width==undefined) || (svg_height==undefined)) return;
  svg_width  = svg_width *zoom|0;
  svg_height = svg_height*zoom|0;
  return {
    svg:       svg.replace(/{width}/g, svg_width).replace(/{height}/g, svg_height),
    width:     svg_width,
    height:    svg_height,
    anchor_dx: (data.anchor_dx) ? data.anchor_dx*zoom|0 : svg_width /2|0,      // точка привязки svg относительно верхнего левого угла
    anchor_dy: (data.anchor_dy) ? data.anchor_dy*zoom|0 : svg_height/2|0,      // по умолчанию: центр svg
  }
}
