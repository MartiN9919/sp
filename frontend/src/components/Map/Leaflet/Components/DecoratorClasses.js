/* СПИСКИ ДЕКОРАТОРОВ ДЛЯ ЛИНИЙ И ГРАНИЦ ПОЛИГОНОВ
 * key - название класса, указывается в MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS
 * color - подставляется автоматически
 * offset - смещение первого маркера от начала, можно в %: '100%'
 * repeat - смещение, через которое повторить маркер, можно в %: '50%'
 */

import { icon_path } from '@/components/Map/Leaflet/Markers/Fun';

export class DECORATOR_CLASSES {
  constructor(color='gray') {
    this.DATA = {

      // скрыто
      'hidden': {
        style: 'opacity: 0;',
      },

      // Маркер обычный
      'mark': {
        pattern: {
          offset: 10,
          repeat: 100,
          symbol: L.Symbol.marker(),
        },
      },


    // штриховка: диагональные штрихи тонкие
    'hatch-diagonal-1': {
      style: 'fill: url(#{id});',
      defs: `
          <pattern id="{id}" patternUnits="userSpaceOnUse" width="4" height="4">
            <path d="M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2" style="stroke:{color}; stroke-width:1;" />
          </pattern>
        `,
    },


    // стрелка: <=>
    'arrow-double-end': {
      style: 'marker-end: url(#{id});',
      defs: `
        <marker id="{id}" fill="{color}" orient="auto" markerUnits='userSpaceOnUse' markerWidth='101' markerHeight='33' refX='0' refY='16.5' opacity='.5'>
          <path d='M1,17 L21,1 L21,33 Z'/>
          <path d='M101,17 L82,1 L82,33 Z'/>
          <rect x="20" y="6" width="64" height="5" />
          <rect x="20" y="23" width="64" height="5" />
        </marker>
      `,
    },




    //
    // РАЗНОЕ ДЛЯ ПРИМЕРОВ
    //

    // черта: тройная
    'dash-3': {
      style: 'marker-pattern: "40 url(#{id}_2) 40 url(#{id}_1)"',
      defs: `
        <marker id="{id}_2" orient="auto" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="12" refX="0" refY="0" viewBox="-4 -6 8 12">
          <rect x="-3" y="-5" width="2" height="10"/>
          <rect x="1" y="-5" width="2" height="10"/>
        </marker>
        <marker id="{id}_1" orient="auto" markerUnits="userSpaceOnUse" markerWidth="4" markerHeight="12" refX="0" refY="0" viewBox="-2 -6 4 12">
          <rect x="-1" y="-5" width="2" height="10"/>
        </marker>
      `,
    },


    // тест
    'fill-test': {
      style: 'fill: url(#{id});',
      defs: `
          <pattern id="{id}" fill="{color}" x="0" y="0" width="25" height="25" patternUnits="userSpaceOnUse">
            <circle cx="10" cy="10" r="10"/>
          </pattern>
        `,
    },

      //
      // Забор оградительный
      //
      'mark_zabor_ograd': {
        pattern: {
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
      },


      //
      // Заграждение сигнализация -|-|-
      //
      'line_zagrad_signal_1': {
        pattern: {
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
      },


      //
      // Рубеж охраны 1 _ . _
      // class="hidden" для основной линии
      'line_border_1': {
        pattern: [
          { offset: 12, repeat: 25, symbol: L.Symbol.dash({ pixelSize: 10, pathOptions: { color: color, weight: 2, }, }), },
          { offset: 0,  repeat: 25, symbol: L.Symbol.dash({ pixelSize: 0,  pathOptions: { color: color, }, }), },
        ],
      },

      //
      // Рубеж охраны 2 _ .. _
      // class="hidden" для основной линии
      'line_border_2': {
        'pattern': [
          { offset: 18, repeat: 30, symbol: L.Symbol.dash({ pixelSize: 10, pathOptions: { color: color, weight: 2, }, }), },
          { offset: 0,  repeat: 30, symbol: L.Symbol.dash({ pixelSize: 0,  pathOptions: { color: color, }, }), },
          { offset: 5,  repeat: 30, symbol: L.Symbol.dash({ pixelSize: 0,  pathOptions: { color: color, }, }), },
        ],
      },






      //
      // РАЗНОЕ ДЛЯ ПРИМЕРОВ
      //
      'test_mark_auto': {
        'pattern': {
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
      },

      'test_mark_iz2': {
        'pattern': {
          offset: 12,
          repeat: 25,
          symbol: L.Symbol.arrowHead({
            pixelSize: 15,
            polygon: false,
            pathOptions: { color: color, weight: 2, stroke: true },
          }),
        },
      },


      // стрелки с окантовкой
      'test_arrow': {
        'pattern': {
          offset: 12,
          repeat: 25,
          symbol: L.Symbol.arrowHead({ pixelSize: 15, pathOptions: { color: color, weight: 2, stroke: true }, }),
        },
      },

      // стрелки закрашенные
      'test_arrow2': {
        'pattern': {
          offset: 25,
          repeat: 50,
          symbol: L.Symbol.arrowHead({ pixelSize: 15, pathOptions: { color: color, fillOpacity: 1, weight: 0, }, }),
        },
      },

      // стрелка в конце, для полигонов не подходит
      'test_arrow3': {
        'pattern': {
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
      },

      // штрих линия светло-серая
      'test2': {
        'pattern': {
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
      },

    }

  }


  // список классов в словарь style, defs
  get_svg = function(names_str) {
    let ret = [];
    let names_list = names_str.trim().replace(/\s+/g, ' ').split(' ');    // убрать лишние пробелы
    names_list = [...new Set(names_list)];                                // исключить повторы

    for(let i=0; i<names_list.length; i++) {
      let val = this.DATA[names_list[i]]?.pattern;
      if (val) {
        if (val instanceof Array) { ret = ret.concat(val); }
        else                      { ret.push(val);         }
      }
    }
    return ret;
  }


  // список классов в список паттернов
  get_patterns = function(names_str) {
    let ret = [];
    let names_list = names_str.trim().replace(/\s+/g, ' ').split(' ');    // убрать лишние пробелы
    names_list = [...new Set(names_list)];                                // исключить повторы

    for(let i=0; i<names_list.length; i++) {
      let val = this.DATA[names_list[i]]?.pattern;
      if (val) {
        if (val instanceof Array) { ret = ret.concat(val); }
        else                      { ret.push(val);         }
      }
    }
    return ret;
  }
}
