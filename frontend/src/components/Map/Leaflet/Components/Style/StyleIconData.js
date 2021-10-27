const DATA = {
  // стрелка: <=>
  'test1': `
    <svg id="{id}" fill="{color}" width={width} height={height} viewBox="0 0 101 33">
      <path d='M1,17 L21,1 L21,33 Z'/>
      <path d='M101,17 L82,1 L82,33 Z'/>
      <rect x="20" y="6" width="64" height="5" />
      <rect x="20" y="23" width="64" height="5" />
    </svg>
  `,

  //
  'test2': `
    <svg id="{id}" fill="{color}" width={width} height={height} viewBox="0 0 100 100">
      <g transform="translate(0,-270.54166)">
        <path
           style="fill:none;stroke:{color};stroke-width:2.5;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none"
       d="m 16.071429,363.75595 c 0,-86.25 0,-86.25 0,-86.25 v 0 0 c 71.25,26.25 71.25,26.25 71.25,26.25 -70.892858,22.32142 -70.892858,22.32142 -70.892858,22.32142"
        />
        <path
           style="fill:#ff0000;stroke:#ff0000;stroke-width:2;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none"
       d="m 44.642857,287.86309 c -28.214286,14.82143 -28.214286,14.82143 -28.214286,14.82143 27.857143,14.28571 27.857143,14.28571 27.857143,14.28571 0,-28.92857 0.357143,-29.10714 0.357143,-29.10714 z"
        />
      </g>
    </svg>
  `,
}

// return {svg: width: height: }
let regexp_vb     = /<svg[^>]*viewBox\s*=\s*"\s*0\s*0\s*(?<width>\d+)\s*(?<height>\d+)\s*"/mi;
export function get_icon_data(key, color="gray", zoom=1) {
  let data = DATA[key];
  if (data === undefined) return;
  let svg  = JSON.parse(JSON.stringify(data)).replace(/{color}/g, color);
  let svg_size   = svg.match(regexp_vb)?.groups;
  let svg_width  = svg_size?.width;
  let svg_height = svg_size?.height;
  if ((svg_width==undefined) || (svg_height==undefined)) return;
  svg_width  = svg_width  * zoom|0;
  svg_height = svg_height * zoom|0;
  return {
    svg:    svg.replace(/{width}/g, svg_width).replace(/{height}/g, svg_height),
    width:  svg_width,
    height: svg_height,
  }
}
