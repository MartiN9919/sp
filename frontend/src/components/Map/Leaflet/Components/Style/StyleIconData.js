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
            style="fill:#ff0000;stroke:#f00;stroke-width:4;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none"
            d="m 42.678571,291.07738 -21.25,11.60714 21.607143,9.46428 c 0.178571,-22.32143 -0.357143,-21.07142 -0.357143,-21.07142 z"
          />
        </g>
      </svg>
    `,
  },

  // ИКОНКИ: СТАНДАРТНЫЕ
  // тор внутри <path style="fill:#fff" d="m 12,1031.2033 c -2.7613995,0 -4.9999995,2.2386 -4.9999995,5 0,2.761 2.2386,5 4.9999995,5 2.761,0 5,-2.239 5,-5 0,-2.7614 -2.239,-5 -5,-5 z m 0,2 c 1.657,0 3,1.3431 3,3 0,1.6569 -1.343,3 -3,3 -1.657,0 -2.9999995,-1.3431 -2.9999995,-3 0,-1.6569 1.3429995,-3 2.9999995,-3 z"/>
  'standart': {
    anchor_dx: 33.1,
    anchor_dy: 98.2,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 67 100">
        <g transform="matrix(4.1640031,0,0,4.0920941,-16.549318,-4208.0243)">
          <circle style="fill:#fff;" cx="12.196746" cy="1036.2429" r="4.545763"/>
          <path style="fill:url(#{id});stroke:#000;stroke-width:0.2" d="m 12.048682,1028.4328 c -4.4183005,0 -8.0000005,3.5817 -8.0000005,8 0,1.421 0.3816,2.75 1.0312,3.906 0.1079,0.192 0.221,0.381 0.3438,0.563 l 6.6250005,11.531 6.625,-11.531 c 0.102,-0.151 0.19,-0.311 0.281,-0.469 l 0.063,-0.094 c 0.649,-1.156 1.031,-2.485 1.031,-3.906 0,-4.4183 -3.582,-8 -8,-8 z m 0,4 c 2.209,0 4,1.7909 4,4 0,2.209 -1.791,4 -4,4 -2.2091005,0 -4.0000005,-1.791 -4.0000005,-4 0,-2.2091 1.7909,-4 4.0000005,-4 z"/>
        </g>
        <defs>
          <linearGradient id="{id}_grag1">
            <stop style="stop-color:{color};" offset="0"/>
            <stop style="stop-color:#fff;" offset="1"/>
          </linearGradient>
          <linearGradient id="{id}" x1="20" y1="1052" x2="-10" y2="1006" xlink:href="#{id}_grag1" gradientUnits="userSpaceOnUse"/>
        </defs>
      </svg>
    `,
  },




  //
  // ИКОНКИ: СПЕЦИАЛЬНЫЕ
  //
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
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif" x="6" y="20">ОПС</text>
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif" x="6" y="96">{text}</text>
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
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif" x="6" y="96">{text}</text>
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
        <text style="font-style:normal;font-weight:bold;font-size:16px;font-family:sans-serif;text-anchor:end" x="190" y="96">{text}</text>
      </svg>
    `,
  },





  //
  // CHECKPOINT
  //
  'checkpoint_auto_inside': {
    anchor_dx: 45.,
    anchor_dy: 50.,
    zoom:      1.,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#f00;stroke-width:4" d="M 3.8,72.6 46.7,3.5 96.6,72.5 Z"/>
        <path style="fill:#f00;stroke:#f00;stroke-width:4" d="m 32.0,38.4 32.7,-0.0 -16.6,28.5 z"/>
        <text style="font-style:normal;font-weight:bold;font-size:22px;font-family:sans-serif" x="100" y="70">{text}</text>
      </svg>
    `,
  },
  'checkpoint_auto_outside': {
    anchor_dx: 275.,
    anchor_dy: 50.,
    zoom:      1.,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#00f;stroke-width:4" d="m 223.3,72.1 42.9,-69.1 49.9,69.0 z"/>
        <path style="fill:#f00;stroke:#f00;stroke-width:4" d="m 251.5,37.9 h 32.7 l -16.6,28.5 z"/>
        <text style="font-style:normal;font-weight:bold;font-size:22px;font-family:sans-serif;text-anchor:end" x="220" y="70">{text}</text>
      </svg>
    `,
  },
  'checkpoint_flyer_inside': {
    anchor_dx: 45.,
    anchor_dy: 50.,
    zoom:      1.,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#f00;stroke-width:4" d="M 3.8,72.6 46.7,3.5 96.6,72.5 Z"/>
        <path style="fill:#00f;stroke:#00f;stroke-width:4" d="m 32.0,38.4 32.7,-0.0 -16.6,28.5 z"/>
        <text style="font-style:normal;font-weight:bold;font-size:22px;font-family:sans-serif" x="100" y="70">{text}</text>
      </svg>
    `,
  },
  'checkpoint_flyer_outside': {
    anchor_dx: 275.,
    anchor_dy: 50.,
    zoom:      1.,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#00f;stroke-width:4" d="m 223.3,72.1 42.9,-69.1 49.9,69.0 z"/>
        <path style="fill:#00f;stroke:#00f;stroke-width:4" d="m 251.5,37.9 h 32.7 l -16.6,28.5 z"/>
        <text style="font-style:normal;font-weight:bold;font-size:22px;font-family:sans-serif;text-anchor:end" x="220" y="70">{text}</text>
      </svg>
    `,
  },
  'checkpoint_rail_inside': {
    anchor_dx: 45.,
    anchor_dy: 50.,
    zoom:      1.,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#f00;stroke-width:4" d="M 3.8,72.6 46.7,3.5 96.6,72.5 Z"/>
        <path style="fill:#000;stroke:#000;stroke-width:4" d="m 31.9,38.4 32.7,-0.0 -16.6,28.5 z"/>
        <text style="font-style:normal;font-weight:bold;font-size:22px;font-family:sans-serif" x="100" y="70">{text}</text>
      </svg>
    `,
  },
  'checkpoint_rail_outside': {
    anchor_dx: 275.,
    anchor_dy: 50.,
    zoom:      1.,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#00f;stroke-width:4" d="m 223.3,72.1 42.9,-69.1 49.9,69.0 z"/>
        <path style="fill:#000;stroke:#000;stroke-width:4" d="m 251.5,37.9 h 32.7 l -16.6,28.5 z"/>
        <text style="font-style:normal;font-weight:bold;font-size:22px;font-family:sans-serif;text-anchor:end" x="220" y="70">{text}</text>
      </svg>
    `,
  },
  'checkpoint_simplified_inside': {
    anchor_dx: 45.,
    anchor_dy: 50.,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#f00;stroke-width:4" d="M 3.8,71.2 45.3,3.5 93.7,71.1 Z"/>
        <path style="fill:#f00;stroke:#f00;stroke-width:1" d="M 45.6,3.5 46.2,71.1 94.0,71.2 45.6,3.5"/>
        <text style="font-style:normal;font-weight:bold;font-size:22px;font-family:sans-serif" x="100" y="70">{text}</text>
      </svg>
    `,
  },
  'checkpoint_simplified_outside': {
    anchor_dx: 275.,
    anchor_dy: 50.,
    svg: `
      <svg width={width} height={height} viewBox="0 0 320 74">
        <path style="fill:#fff;stroke:#00f;stroke-width:4" d="m 226.17,71.7 41.5,-67.7 48.4,67.6 z"/>
        <path style="fill:#00f;stroke:#00f;stroke-width:1" d="m 267.97,4.0 0.6,67.6 47.8,0.1 -48.4,-67.7"/>
        <text style="font-style:normal;font-weight:bold;font-size:22px;font-family:sans-serif;text-anchor:end" x="220" y="70">{text}</text>
      </svg>
    `,
  },




  //
  // ENINEER
  //
  'engineer_border_sign': {
    anchor_dx: 50,
    anchor_dy: 50.,
    zoom:      .5,
    svg: `
      <svg width={width} height={height} viewBox="0 0 500 130">
        <circle style="fill:#fff;stroke:#000;stroke-width:4" cx="50" cy="50" r="23"/>
        <circle style="fill:#000" cx="50" cy="50" r="8"/>
        <text style="font-style:normal;font-weight:bold;font-size:45px;font-family:sans-serif" x="0" y="115">{text}</text>
      </svg>
    `,
  },
  'engineer_tower_industrial': {
    anchor_dx: 33,
    anchor_dy: 94.,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 300 94">
        <path style="fill:#fff;stroke:#000;stroke-width:4" d="m 3.53,91.11 h 60 l -30,-75.00 z"/>
        <path style="fill:#fff;stroke:#000;stroke-width:4" d="m 12.53,11.11 h 40 l 6,-10.00 -2,3 h -48 l -2,-3 z"/>
        <text style="font-style:normal;font-weight:bold;font-size:32px;font-family:sans-serif" x="66" y="88">{text}</text>
      </svg>
    `,
  },




  //
  // POINTS
  //
  'point_detention_inside': {
    anchor_dx: 53,
    anchor_dy: 50.,
    zoom:      .7,
    svg: `
      <svg width={width} height={height} viewBox="0 0 106 100">
        <path style="fill:#ffffff00;stroke:#f00;stroke-width:6" d="M 78,6.7 A 53,53 0 0,1 78,93.3"/>
        <path style="fill:#ffffff00;stroke:#f00;stroke-width:6" d="M 28,93.3 A 53,53 0 0,1 28,6.7"/>
        <circle style="fill:#fff;stroke:#00f;stroke-width:6" cx="53" cy="53" r="25"/>
      </svg>
    `,
  },









  'engeneer_signal': {
    anchor_dx: 24,
    anchor_dy: 5,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 40 10">
        <path style="fill:none;stroke:#888;stroke-width:10;" d="m 5,0 h 40"/>
      </svg>
    `,
  },



  // текст для линии
  'text_line_fill_100': {
    anchor_dx: 12,
    anchor_dy: 0,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 100">
        <rect x="-10" y="-2" width="38" height="102" fill="#fff" />
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(90)" x="50" y="-3">{text}</text>
      </svg>
    `,
  },
  'text_line_fill_300': {
    anchor_dx: 12,
    anchor_dy: 0,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 300">
        <rect x="-10" y="-2" width="38" height="302" fill="#fff" />
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(90)" x="150" y="-3">{text}</text>
      </svg>
    `,
  },
  'text_line_100': {
    anchor_dx: 12,
    anchor_dy: 0,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 100">
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(90)" x="50" y="-3">{text}</text>
      </svg>
    `,
  },
  'text_line_300': {
    anchor_dx: 12,
    anchor_dy: 0,
    zoom:      .8,
    svg: `
      <svg width={width} height={height} viewBox="0 0 30 300">
        <text style="font-style:normal;font-weight:bold;font-size:30px;font-family:sans-serif;fill:#444;text-anchor:middle" transform="rotate(90)" x="150" y="-3">{text}</text>
      </svg>
    `,
  },
}


import { MAP_CONST } from '@/components/Map/Leaflet/Lib/Const';
let regexp_vb  = /<svg[^>]*viewBox\s*=\s*"\s*0\s*0\s*(?<width>\d+(?:\.\d+)?)\s*(?<height>\d+(?:\.\d+)?)\s*"/mi;
export function get_icon_data(key, color="gray", zoom=1, text=undefined) {
  let data = DATA[key];
  if (data === undefined) return;
  if (text === undefined) text = '';
  let id   = 'icon_'+(new Date().getTime())+'_'+((Math.random()*1000000000)|0);
  let svg  = JSON.parse(JSON.stringify(data.svg)).replace(/{color}/g, color).replace(/{text}/g, text).replace(/{id}/g, id);
  let svg_size   = svg.match(regexp_vb)?.groups;
  let svg_width  = svg_size?.width;
  let svg_height = svg_size?.height;
  if ((svg_width==undefined) || (svg_height==undefined)) return;
  let zoom_common = zoom*MAP_CONST.CLASS.ICON.SVG_ZOOM_BASE*(data.zoom??1.);
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
