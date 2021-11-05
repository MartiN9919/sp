import { MAP_CONST, MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { icon_get } from '@/components/Map/Leaflet/Components/Style/StyleIcon';

import * as DATA_FORCE      from '@/components/Map/Leaflet/Components/Style/StyleDataForce';
import * as DATA_CHECKPOINT from '@/components/Map/Leaflet/Components/Style/StyleDataCheckpoint';
import * as DATA_ENGENEER   from '@/components/Map/Leaflet/Components/Style/StyleDataEngeneer';
import * as DATA_LAYOUT     from '@/components/Map/Leaflet/Components/Style/StyleDataLayout';
import * as DATA_TEXT       from '@/components/Map/Leaflet/Components/Style/StyleDataText';
import * as DATA_COMMON     from '@/components/Map/Leaflet/Components/Style/StyleDataCommon';
import * as DATA_TEST       from '@/components/Map/Leaflet/Components/Style/StyleDataTest';

const DATA_ICON = {
  ...DATA_FORCE.ICON,
  ...DATA_CHECKPOINT.ICON,
  ...DATA_ENGENEER.ICON,
  ...DATA_LAYOUT.ICON,
  ...DATA_TEXT.ICON,
  ...DATA_COMMON.ICON,
  ...DATA_TEST.ICON,
}

const DATA_DECOR = {
  ...DATA_FORCE.DECOR,
  ...DATA_CHECKPOINT.DECOR,
  ...DATA_ENGENEER.DECOR,
  ...DATA_LAYOUT.DECOR,
  ...DATA_TEXT.DECOR,
  ...DATA_COMMON.DECOR,
  ...DATA_TEST.DECOR,
}

const DATA_SVG = {
  ...DATA_FORCE.SVG,
  ...DATA_CHECKPOINT.SVG,
  ...DATA_ENGENEER.SVG,
  ...DATA_LAYOUT.SVG,
  ...DATA_TEXT.SVG,
  ...DATA_COMMON.SVG,
  ...DATA_TEST.SVG,
}

/*
 *
 * ICON
 *
 */
let regexp_vb  = /<svg[^>]*viewBox\s*=\s*"\s*0\s*0\s*(?<width>\d+(?:\.\d+)?)\s*(?<height>\d+(?:\.\d+)?)\s*"/mi;
export function get_style_data_icon(icon_data_key, color="gray", zoom=1, text=undefined) {
  let data = DATA_ICON[icon_data_key];
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



/*
 * DECOR
 *
 * СПИСКИ ДЕКОРАТОРОВ ДЛЯ ЛИНИЙ И ГРАНИЦ ПОЛИГОНОВ
 * key - название класса, указывается в MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS
 * color - подставляется автоматически
 * offset - смещение первого маркера от начала, можно в %: '100%'
 * repeat - смещение, через которое повторить маркер, можно в %: '50%'
 */
export function get_style_data_decor(classes_str, index, color="gray", zoom=1, icon_properties={}) {
  let ret = [];
  let classes_list = classes_str.trim().replace(/\s+/g, ' ').split(' ');  // убрать лишние пробелы
  classes_list = [...new Set(classes_list)];                              // исключить повторы

  // перебрать классы
  classes_list.forEach(function(class_item, class_ind) {
    let data = DATA_DECOR[class_item];
    if (data === undefined) return;
    data = JSON.parse(JSON.stringify(data));
    if (!(data instanceof Array)) data = [data];                          // к единому формату

    data.forEach(function(data_item, data_ind) {
      // тип: маркер
      if (data[data_ind].symbol_type == 'marker') {
        data[data_ind].symbol_options.markerOptions.icon = icon_get(color, {
          [MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS   ]: data[data_ind].symbol_options.markerOptions.icon,
          ...icon_properties,
          ...data[data_ind].icon_properties,
        });
        data[data_ind].symbol = L.Symbol.marker(data[data_ind].symbol_options);
      }

      // тип: штрих
      if (data[data_ind].symbol_type == 'dash') {
        if (data[data_ind].symbol_options.pathOptions.color == '{color}') data[data_ind].symbol_options.pathOptions.color = color;
        data[data_ind].symbol = L.Symbol.dash(data[data_ind].symbol_options);
      }

      // тип: стрелка
      if (data[data_ind].symbol_type == 'arrow') {
        if (data[data_ind].symbol_options.pathOptions.color == '{color}') data[data_ind].symbol_options.pathOptions.color = color;
        data[data_ind].symbol = L.Symbol.arrowHead(data[data_ind].symbol_options);
      }

      // удалить ставшие ненужными записи
      if (data[data_ind].symbol_type     != undefined) delete data[data_ind]['symbol_type'    ];
      if (data[data_ind].symbol_options  != undefined) delete data[data_ind]['symbol_options' ];
      if (data[data_ind].icon_properties != undefined) delete data[data_ind]['icon_properties'];

      // запомнить результат
      ret.push(data[data_ind]);
    });
  });
  return ret;
}


/*
 *
 * ICON
 *
 */
