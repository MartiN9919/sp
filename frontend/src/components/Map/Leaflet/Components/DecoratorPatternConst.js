/* СПИСКИ ДЕКОРАТОРОВ ДЛЯ ЛИНИЙ И ГРАНИЦ ПОЛИГОНОВ
 * key - название класса, указывается в MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS
 * color - подставляется автоматически
 * offset - смещение первого маркера от начала, можно в %: '100%'
 * repeat - смещение, через которое повторить маркер, можно в %: '50%'
 */

import { icon_path } from '@/components/Map/Leaflet/Markers/Fun';

export class CONST_PATTERN {
  constructor(color='gray') {
    this.dat = {

      // Маркер обычный
      'mark': {
        offset: 10,
        repeat: 100,
        symbol: L.Symbol.marker(),
      },


      //
      // Забор оградительный
      //
      'mark_zabor_ograd': {
        offset: 8, repeat: 30,
        symbol: L.Symbol.marker({
          rotate: true,
          markerOptions: {
            icon: L.icon({
              iconUrl: icon_path('zabor_ogradit'),
              iconSize: [10, 10],   // original: [16, 16]
              iconAnchor: [5, 5],
            }),
          },
        }),
      },


      //
      // Заграждение сигнализация -|-|-
      //
      'line_zagrad_signal_1': {
        offset: 8, repeat: 18,
        symbol: L.Symbol.marker({
          rotate: true,
          markerOptions: {
            icon: L.icon({
              iconUrl: icon_path('zagragd_signal'),
              //iconSize: [2, 10],   // original: [3, 16]
              iconAnchor: [8, 0],
            }),
          },
        }),
      },


      //
      // Рубеж охраны 1 _ . _
      // class="hidden" для основной линии
      'line_border_1': [
        { offset: 12, repeat: 25, symbol: L.Symbol.dash({ pixelSize: 10, pathOptions: { color: color, weight: 2, }, }), },
        { offset: 0,  repeat: 25, symbol: L.Symbol.dash({ pixelSize: 0,  pathOptions: { color: color, }, }), },
      ],

      //
      // Рубеж охраны 2 _ .. _
      // class="hidden" для основной линии
      'line_border_2': [
        { offset: 18, repeat: 30, symbol: L.Symbol.dash({ pixelSize: 10, pathOptions: { color: color, weight: 2, }, }), },
        { offset: 0,  repeat: 30, symbol: L.Symbol.dash({ pixelSize: 0,  pathOptions: { color: color, }, }), },
        { offset: 5,  repeat: 30, symbol: L.Symbol.dash({ pixelSize: 0,  pathOptions: { color: color, }, }), },
      ],






      //
      // РАЗНОЕ ДЛЯ ПРИМЕРОВ
      //
      'test_mark_auto': {
        offset: 25,
        repeat: 120,
        symbol: L.Symbol.marker({
          rotate: false,
          markerOptions: {
            icon: L.icon({
              iconUrl: icon_path('test2'),
              iconAnchor: [30, 40],
            }),
          },
        }),
      },

      'test_mark_iz2': {
        offset: 12,
        repeat: 25,
        symbol: L.Symbol.arrowHead({
          pixelSize: 15,
          polygon: false,
          pathOptions: { color: color, weight: 2, stroke: true },
        }),
      },


      // стрелки с окантовкой
      'test_arrow': {
        offset: 12,
        repeat: 25,
        symbol: L.Symbol.arrowHead({ pixelSize: 15, pathOptions: { color: color, weight: 2, stroke: true }, }),
      },

      // стрелки закрашенные
      'test_arrow2': {
        offset: 25,
        repeat: 50,
        symbol: L.Symbol.arrowHead({ pixelSize: 15, pathOptions: { color: color, fillOpacity: 1, weight: 0, }, }),
      },

      // стрелка в конце, для полигонов не подходит
      'test_arrow3': {
        offset: '100%',
        repeat: 0,
        symbol: L.Symbol.arrowHead({
          pixelSize: 15,
          polygon: false,
          pathOptions: {
            color: color,
            stroke: true,
          }
        }),
      },

      // штрих линия светло-серая
      'test2': {
        offset: 0,
        repeat: 10,
        symbol: L.Symbol.dash({
          pixelSize: 5,
          pathOptions: {
            color: '#000',
            weight: 1,
            opacity: 0.2
          },
        }),
      },

    }

  }

  // список классов в список паттернов
  get = function(names_str) {
    let ret = [];
    let names_list = names_str.trim().replace(/\s+/g, ' ').split(' ');    // убрать лишние пробелы
    names_list = [...new Set(names_list)];                                // исключить повторы

    for(let i=0; i<names_list.length; i++) {
      let val = this.dat[names_list[i]];
      if (val) {
        if (val instanceof Array) { ret = ret.concat(val); }
        else                      { ret.push(val);         }
      }
    }
    return ret;
  }
}
