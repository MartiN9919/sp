import { STYLE_DATA_POST_ICON       } from '@/components/Map/Leaflet/Components/Style/StyleDataPost';
import { STYLE_DATA_CHECKPOINT_ICON } from '@/components/Map/Leaflet/Components/Style/StyleDataCheckpoint';
import { STYLE_DATA_ENGENEER_ICON   } from '@/components/Map/Leaflet/Components/Style/StyleDataEngeneer';
import { STYLE_DATA_TEXT_ICON       } from '@/components/Map/Leaflet/Components/Style/StyleDataText';

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




  ...STYLE_DATA_POST_ICON,
  ...STYLE_DATA_CHECKPOINT_ICON,
  ...STYLE_DATA_ENGENEER_ICON,
  ...STYLE_DATA_TEXT_ICON,
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
