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

