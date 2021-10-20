/* СПИСКИ ДЕКОРАТОРОВ ДЛЯ ЛИНИЙ И ГРАНИЦ ПОЛИГОНОВ
 * key - название класса, указывается в MAP_ITEM.FC.STYLE.CLASS
 * color - подставляется автоматически
 * offset - смещение первого маркера от начала, можно в %: '100%'
 * repeat - смещение, через которое повторить маркер, можно в %: '50%'
 * symbol
 *   markerOptionssymbol
 */

import { icon_path } from '@/components/Map/Leaflet/Markers/Fun';

export class CONST_PATH {
  constructor(color='gray') {
    this.dat = {

      // Забор оградительный
      'mark_zabor_ograd': {
        offset: 8, repeat: 30,
        symbol: L.Symbol.marker({
          rotate: true,
          markerOptions: {
            icon: L.icon({
              iconUrl: icon_path('Забор оградительный'),
              iconSize: [10, 10],   // original: [16, 16]
              iconAnchor: [5, 5],
            }),
          },
        }),
      },


      //
      // Рубеж охраны 1 _ . _
      //
      'line_border_1_1': { offset: 12, repeat: 25, symbol: L.Symbol.dash({ pixelSize: 10, pathOptions: { color: color, weight: 2, }, }), },
      'line_border_1_2': { offset: 0,  repeat: 25, symbol: L.Symbol.dash({ pixelSize: 0,  pathOptions: { color: color, }, }), },

      //
      // Рубеж охраны 2 _ .. _
      //
      'line_border_2_1': { offset: 12, repeat: 25, symbol: L.Symbol.dash({ pixelSize: 10, pathOptions: { color: color, weight: 2, }, }), },
      'line_border_2_2': { offset: 0,  repeat: 25, symbol: L.Symbol.dash({ pixelSize: 0,  pathOptions: { color: color, }, }), },


      'mark_iz2': {
        offset: 12,
        repeat: 25,
        symbol: L.Symbol.arrowHead({
          pixelSize: 15,
          polygon: false,
          pathOptions: { color: color, weight: 2, stroke: true },
        }),
      },


      // стрелки с окантовкой
      'arrow': {
        offset: 12,
        repeat: 25,
        symbol: L.Symbol.arrowHead({ pixelSize: 15, pathOptions: { color: color, weight: 2, stroke: true }, }),
      },

      // стрелки закрашенные
      'arrow2': {
        offset: 25,
        repeat: 50,
        symbol: L.Symbol.arrowHead({ pixelSize: 15, pathOptions: { color: color, fillOpacity: 1, weight: 0, }, }),
      },




      // стрелка в конце, для полигонов не подходит
      'arrow3': {
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


      // маркеры обычные
      'mark': {
        offset: '5%',
        repeat: '10%',
        symbol: L.Symbol.marker(),
      },

      'mark2': {
        offset: '16%',
        repeat: '8%',
        symbol: L.Symbol.marker({
          rotate: false,
          markerOptions: {
            icon: L.icon({
              iconUrl: icon_path('test2'),
              iconAnchor: [0, 50]
            }),
          },
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

  get = function(names_str) {
    let ret = [];
    let names_list = names_str.trim().replace(/\s+/g, ' ').split(' ');

    for(let i=0; i<names_list.length; i++) {
      let pattern = this.dat[names_list[i]];
      if (pattern) { ret.push(pattern); }
    }
    return ret;
  }
}



      // var markerLine = L.polyline([[58.44773, -28.65234], [52.9354, -23.33496], [53.01478, -14.32617], [58.1707, -10.37109], [59.68993, -0.65918]], {}).addTo(this.map);
      // var markerPatterns = L.polylineDecorator(markerLine, {
      //   //patterns: this.style_patterns,
      //   patterns: [
      //     { offset: '5%', repeat: '10%', symbol: L.Symbol.marker()}
      //   ]
      // }).addTo(this.map);

