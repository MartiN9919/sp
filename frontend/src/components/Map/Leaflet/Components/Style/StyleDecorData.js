/* СПИСКИ ДЕКОРАТОРОВ ДЛЯ ЛИНИЙ И ГРАНИЦ ПОЛИГОНОВ
 * key - название класса, указывается в MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS
 * color - подставляется автоматически
 * offset - смещение первого маркера от начала, можно в %: '100%'
 * repeat - смещение, через которое повторить маркер, можно в %: '50%'
 */

import { icon_get } from '@/components/Map/Leaflet/Components/Style/StyleIcon';

const DATA = {
  //
  // Рубеж охраны 1 _ . _
  //
  // class="hidden" для основной линии
  'line_border_1': [
    { offset: 12, repeat: 25, symbol_type: 'dash', symbol_options: { pixelSize: 10, pathOptions: { color: '#0a0', weight: 2, }, }, },
    { offset: 0,  repeat: 25, symbol_type: 'dash', symbol_options: { pixelSize: 0,  pathOptions: { color: '#0a0', }, }, },
  ],

  //
  // Рубеж охраны 2 _ .. _
  //
  // class="hidden" для основной линии
  'line_border_2': [
    { offset: 18, repeat: 30, symbol_type: 'dash', symbol_options: { pixelSize: 10, pathOptions: { color: '#0a0', weight: 2, }, }, },
    { offset: 0,  repeat: 30, symbol_type: 'dash', symbol_options: { pixelSize: 0,  pathOptions: { color: '#0a0', }, }, },
    { offset: 5,  repeat: 30, symbol_type: 'dash', symbol_options: { pixelSize: 0,  pathOptions: { color: '#0a0', }, }, },
  ],

  //
  // Забор оградительный х х х
  //
  'line-engeneer_ograd': {
    offset: 8, repeat: 30,
    symbol_type: 'marker',
    symbol_options: { rotate: true, markerOptions: { icon: 'icon-file-zabor_ogradit-10-10', }, },
  },

  //
  // Заграждение сигнализация -|-|-
  //
  'line-engeneer_signal': {
    offset: 8, repeat: 18,
    symbol_type: 'marker',
    symbol_options: { rotate: true, markerOptions: { icon: 'icon-svg-engeneer_signal', }, },
  },
}



import { MAP_CONST } from '@/components/Map/Leaflet/Lib/Const';
export function get_decor_data(classes_str, index, color="gray", zoom=1) {
  let ret = [];
  let classes_list = classes_str.trim().replace(/\s+/g, ' ').split(' ');  // убрать лишние пробелы
  classes_list = [...new Set(classes_list)];                              // исключить повторы

  // перебрать классы
  classes_list.forEach(function(class_item, class_ind) {
    let data = DATA[class_item];
    if (data === undefined) return;
    data = JSON.parse(JSON.stringify(data));
    if (!(data instanceof Array)) data = [data];                          // к единому формату

    data.forEach(function(data_item, data_ind) {
      // тип: маркер
      if (data[data_ind].symbol_type == 'marker') {
        data[data_ind].symbol_options.markerOptions.icon = icon_get(color, {class: data[data_ind].symbol_options.markerOptions.icon});
        data[data_ind].symbol = L.Symbol.marker(data[data_ind].symbol_options);
      }

      // тип: штрих
      if (data[data_ind].symbol_type == 'dash') {
        if (data[data_ind].symbol_options.pathOptions.color == '{color}') data[data_ind].symbol_options.pathOptions.color = color;
        data[data_ind].symbol = L.Symbol.dash(data[data_ind].symbol_options);
      }

      // удалить ставшие ненужными записи
      if (data[data_ind].symbol_type    != undefined) delete data[data_ind]['symbol_type'   ];
      if (data[data_ind].symbol_options != undefined) delete data[data_ind]['symbol_options'];

      // запомнить результат
      ret.push(data[data_ind]);
    });
  });
  return ret;
}




  // get = function(classes_str) {
  //   let ret = [];
  //   let classes_list = classes_str.trim().replace(/\s+/g, ' ').split(' ');  // убрать лишние пробелы
  //   classes_list = [...new Set(classes_list)];                              // исключить повторы

  //   for(let i=0; i<classes_list.length; i++) {
  //     let val = this.dat[classes_list[i]];
  //     if (val) {
  //       if (val instanceof Array) { ret = ret.concat(val); }
  //       else                      { ret.push(val);         }
  //     }
  //   }
  //   return ret;
  // }


//   constructor(color='gray') {


//     this.dat = {

//       // Маркер обычный
//       'mark': {
//         offset: 10,
//         repeat: 100,
//         symbol: L.Symbol.marker(),
//       },


//       'marker_test': {

//       },

//     //   "marker": {
//     //     "icon": "test",     // "mdi-flag mdi-spin", "fs-spec0", "pulse" (size: 12), "#0f0", "gold", "file_name" (size_w: 25, size_h: 41)
//     //     "zoom": 2,
//     //   },




//       //
//       // Забор оградительный
//       //
//       'mark_zabor_ograd': {
//         offset: 8, repeat: 30,
//         symbol: L.Symbol.marker({
//           rotate: true,
//           markerOptions: {
//             icon: icon_get(color, {class: 'icon-file-zabor_ogradit-10-10'}),
//           },
//         }),
//       },


//       //
//       // Заграждение сигнализация -|-|-
//       //
//       'line-engeneer_signal': {
//         offset: 8, repeat: 18,
//         symbol: L.Symbol.marker({
//           rotate: true,
//           markerOptions: {
//             icon: icon_get(color, {class: 'icon-svg-engeneer_signal'}),
//           },
//         }),
//       },


//       //
//       // Рубеж охраны 1 _ . _
//       // class="hidden" для основной линии
//       'line_border_1': [
//         { offset: 12, repeat: 25, symbol: L.Symbol.dash({ pixelSize: 10, pathOptions: { color: color, weight: 2, }, }), },
//         { offset: 0,  repeat: 25, symbol: L.Symbol.dash({ pixelSize: 0,  pathOptions: { color: color, }, }), },
//       ],

//       //
//       // Рубеж охраны 2 _ .. _
//       // class="hidden" для основной линии
//       'line_border_2': [
//         { offset: 18, repeat: 30, symbol: L.Symbol.dash({ pixelSize: 10, pathOptions: { color: color, weight: 2, }, }), },
//         { offset: 0,  repeat: 30, symbol: L.Symbol.dash({ pixelSize: 0,  pathOptions: { color: color, }, }), },
//         { offset: 5,  repeat: 30, symbol: L.Symbol.dash({ pixelSize: 0,  pathOptions: { color: color, }, }), },
//       ],






//       //
//       // РАЗНОЕ ДЛЯ ПРИМЕРОВ
//       //
//       'test_mark_auto': {
//         offset: 25,
//         repeat: 120,
//         symbol: L.Symbol.marker({
//           rotate: false,
//           markerOptions: {
//             icon: icon_get(color, {class: 'icon-file-test2-30-40'}),
//           },
//         }),
//       },

//       'test_mark_iz2': {
//         offset: 12,
//         repeat: 25,
//         symbol: L.Symbol.arrowHead({
//           pixelSize: 15,
//           polygon: false,
//           pathOptions: { color: color, weight: 2, stroke: true },
//         }),
//       },


//       // стрелки с окантовкой
//       'test_arrow': {
//         offset: 12,
//         repeat: 25,
//         symbol: L.Symbol.arrowHead({ pixelSize: 15, pathOptions: { color: color, weight: 2, stroke: true }, }),
//       },

//       // стрелки закрашенные
//       'test_arrow2': {
//         offset: 25,
//         repeat: 50,
//         symbol: L.Symbol.arrowHead({ pixelSize: 15, pathOptions: { color: color, fillOpacity: 1, weight: 0, }, }),
//       },

//       // стрелка в конце, для полигонов не подходит
//       'test_arrow3': {
//         offset: '100%',
//         repeat: 0,
//         symbol: L.Symbol.arrowHead({
//           pixelSize: 15,
//           polygon: false,
//           pathOptions: {
//             color: color,
//             stroke: true,
//           }
//         }),
//       },

//       // штрих линия светло-серая
//       'test2': {
//         offset: 0,
//         repeat: 10,
//         symbol: L.Symbol.dash({
//           pixelSize: 5,
//           pathOptions: {
//             color: '#000',
//             weight: 1,
//             opacity: 0.2
//           },
//         }),
//       },

//     }

//   }

//   // список классов в список паттернов
//   get = function(classes_str) {
//     let ret = [];
//     let classes_list = classes_str.trim().replace(/\s+/g, ' ').split(' ');  // убрать лишние пробелы
//     classes_list = [...new Set(classes_list)];                              // исключить повторы

//     for(let i=0; i<classes_list.length; i++) {
//       let val = this.dat[classes_list[i]];
//       if (val) {
//         if (val instanceof Array) { ret = ret.concat(val); }
//         else                      { ret.push(val);         }
//       }
//     }
//     return ret;
//   }
// }
