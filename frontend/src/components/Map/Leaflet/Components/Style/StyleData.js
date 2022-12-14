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

/* СПИСКИ ДЕКОРАТОРОВ ДЛЯ ЛИНИЙ И ГРАНИЦ ПОЛИГОНОВ
 * key - название класса, указывается в MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS
 * color - подставляется автоматически
 * offset - смещение первого маркера от начала, можно в %: '100%'
 * repeat - смещение, через которое повторить маркер, можно в %: '50%'
 */
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
 * ICON
 *
 * options:
 *   class_item - класс иконки (без icon-svg-)
 *   color
 *   zoom - вычислено с учетом zoom_map, feature[].properties.[MAP_ITEM.FC.FEATURES.PROPERTIES.ZOOM]
 *   rotate - угол поворота, в градусах
 *   text -
 */
export function get_style_data_icon(options) {
  // const class_item = options.class_item;
  const color  = options.color  ?? MAP_CONST.COLOR.DEFAULT_STYLE_ICON;
  const zoom   = options.zoom   ?? 1;
  const rotate = options.rotate ?? 0;
  const text   = options.text   ?? '';

  const data   = DATA_ICON[options.class_item];
  if (data === undefined) return;
  const id     = 'icon-'+get_random();
  const svg    =
    JSON.parse(JSON.stringify(data.svg))
      .replace(/{color}/g, color)
      .replace(/{text}/g, text)
      .replace(/{id}/g, id)
      .replace(/{rotate}/g, rotate);
  const zoom_common = zoom*MAP_CONST.CLASS.ICON.SVG_ZOOM_BASE*(data.zoom??1.);
  const [svg_width, svg_height] = calc_svg_size(svg, zoom_common);
  if ((svg_width==undefined) || (svg_height==undefined)) return;
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
 * options:
 *   classes_str - список классов
 *   color
 *   icon_properties
 * sel:
 *   true - устанавливается класс MAP_CONST.CLASS.SEL
 */
export function get_style_data_decor(options, sel=false) {
  const classes_str     = options.classes_str;
  let   color           = options.color           ?? MAP_CONST.COLOR.DEFAULT_STYLE_PATH;
  const icon_properties = options.icon_properties ?? {};

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
      switch (data[data_ind].symbol_type) {
        // тип: маркер
        case 'marker':
          // приоритет цвета декорации над цветом фигуры и цветом скрипта
          if (data[data_ind].symbol_options.markerOptions.color != undefined) color = data[data_ind].symbol_options.markerOptions.color;
          let class_str = data[data_ind].symbol_options.markerOptions.icon;
          if (sel) class_str = class_str + ' ' + MAP_CONST.CLASS.SEL;
          data[data_ind].symbol_options.markerOptions.icon = icon_get(color, {
            [MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS]: class_str,
            ...icon_properties,
            ...data[data_ind].icon_properties,
          });
          data[data_ind].symbol = L.Symbol.marker(data[data_ind].symbol_options);
          break;

        // тип: штрих
        case 'dash':
          if (data[data_ind].symbol_options.pathOptions.color == '{color}') data[data_ind].symbol_options.pathOptions.color = color;
          if (sel) data[data_ind].symbol_options.pathOptions.className = MAP_CONST.CLASS.SEL;
          data[data_ind].symbol = L.Symbol.dash(data[data_ind].symbol_options);
          break;

        // тип: стрелка
        case 'arrow':
          if (data[data_ind].symbol_options.pathOptions.color == '{color}') data[data_ind].symbol_options.pathOptions.color = color;
          if (sel) data[data_ind].symbol_options.pathOptions.className = MAP_CONST.CLASS.SEL;
          data[data_ind].symbol = L.Symbol.arrowHead(data[data_ind].symbol_options);
          break;
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
 * SVG
 *
 * options:
 *   classes_str - список классов
 *   color
 *   zoom - вычислено с учетом zoom_map, feature[].properties.[MAP_ITEM.FC.FEATURES.PROPERTIES.ZOOM]
 *   rotate - угол поворота, в градусах
 *   index_item - state.selectedTemplate.activeAnalysts
 *   index_feature
 * return {style: '...', defs: '...'}
 */
export function get_style_data_svg(options) {
  const classes_str   = options.classes_str;
  const color         = options.color  ?? MAP_CONST.COLOR.DEFAULT_STYLE_PATH;
  const zoom          = options.zoom   ?? 1;
  const rotate        = options.rotate ?? 0;
  const index_item    = options.index_item;
  const index_feature = options.index_feature;
  let ret = {style: '', defs: ''};

  let classes_list = classes_str.trim().replace(/\s+/g, ' ').split(' ');  // убрать лишние пробелы
  classes_list = [...new Set(classes_list)];                              // исключить повторы

  // перебрать классы
  classes_list.forEach(function(class_item, class_ind) {
    // для класса: стиль и defs
    let data = DATA_SVG[class_item];
    if (data === undefined) return;
    let data_style = (data.style)?JSON.parse(JSON.stringify(data.style)):undefined;
    let data_defs  = (data.defs )?JSON.parse(JSON.stringify(data.defs)) :undefined;
    let zoom_common = zoom*MAP_CONST.CLASS.ICON.SVG_ZOOM_BASE*(data.zoom??1.);

    // уникальные id и имя класса
    let id        = 'svg-'+get_random();
    let class_str = '.'+correct_class_name(class_item, index_item, index_feature);

    // заменить переменные
    if (data_style) {
      data_style = data_style.replace(/{id}/g, id).replace(/{color}/g, color).replace(/{class}/g, class_str).replace(/{rotate}/g, rotate);
      ret.style += data_style+'\n';
    }

    if (data_defs) {
      const [svg_width, svg_height] = calc_svg_size(data_defs, zoom_common);
      if ((svg_width!=undefined) && (svg_height!=undefined)) {
        data_defs = data_defs.replace(/{width}/g, svg_width).replace(/{height}/g, svg_height);
      }
      data_defs = data_defs.replace(/{id}/g, id).replace(/{color}/g, color).replace(/{rotate}/g, rotate);
      ret.defs += data_defs+'\n';
    }
  });

  return ret;
}


// расчитать реальный размер SVG
const regexp_vb  = /^\s*<[^>]*viewBox\s*=\s*"\s*0\s*0\s*(?<width>\d+(?:\.\d+)?)\s*(?<height>\d+(?:\.\d+)?)\s*"/mi;
function calc_svg_size(svg, zoom_common=1) {
  let svg_size   = svg.match(regexp_vb)?.groups;
  let svg_width  = svg_size?.width;
  let svg_height = svg_size?.height;
  if ((svg_width==undefined) || (svg_height==undefined)) return [undefined, undefined];
  svg_width  = svg_width *zoom_common;//|0;
  svg_height = svg_height*zoom_common;//|0;
  return [svg_width, svg_height];
}



// скоректированный список классов с учетом state.selectedTemplate.activeAnalysts[index_item]
// сейчас только для DATA_SVG
export function correct_classes_name(classes_str, index_item, index_feature) {
  classes_str, index_item, index_feature
  let classes_list = classes_str.trim().replace(/\s+/g, ' ').split(' ');  // убрать лишние пробелы
  classes_list = [...new Set(classes_list)];                              // исключить повторы

  classes_list.forEach(function(class_item, class_ind) {
    let data = DATA_SVG[class_item];
    if (data !== undefined) {
      classes_list[class_ind] = correct_class_name(class_item, index_item, index_feature);
    }
  });

  return classes_list.join(' ');
}


// скоректированное название класса с учетом state.selectedTemplate.activeAnalysts[index]
function correct_class_name(class_str, index_item, index_feature) {
  return class_str+'-'+index_item+'-'+index_feature;
}



function get_random() {
  return (new Date().getTime())+'_'+((Math.random()*1000000000)|0);
}
