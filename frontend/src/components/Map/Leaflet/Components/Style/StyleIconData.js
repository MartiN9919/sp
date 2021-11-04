import { STYLE_DATA_FORCE_ICON      } from '@/components/Map/Leaflet/Components/Style/StyleDataForce';
import { STYLE_DATA_CHECKPOINT_ICON } from '@/components/Map/Leaflet/Components/Style/StyleDataCheckpoint';
import { STYLE_DATA_ENGENEER_ICON   } from '@/components/Map/Leaflet/Components/Style/StyleDataEngeneer';
import { STYLE_DATA_LAYOUT_ICON     } from '@/components/Map/Leaflet/Components/Style/StyleDataLayout';
import { STYLE_DATA_TEXT_ICON       } from '@/components/Map/Leaflet/Components/Style/StyleDataText';
import { STYLE_DATA_COMMON_ICON     } from '@/components/Map/Leaflet/Components/Style/StyleDataCommon';
import { STYLE_DATA_TEST_ICON       } from '@/components/Map/Leaflet/Components/Style/StyleDataTest';

const DATA = {
  ...STYLE_DATA_FORCE_ICON,
  ...STYLE_DATA_CHECKPOINT_ICON,
  ...STYLE_DATA_ENGENEER_ICON,
  ...STYLE_DATA_LAYOUT_ICON,
  ...STYLE_DATA_TEXT_ICON,
  ...STYLE_DATA_COMMON_ICON,
  ...STYLE_DATA_TEST_ICON,
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
