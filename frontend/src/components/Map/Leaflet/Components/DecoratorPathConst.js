import { icon_path } from '@/components/Map/Leaflet/Markers/Fun';

export class CONST_PATH {
  constructor(color='gray') {
    this.dat = {
      'mark_iz': {
        offset: 12,  // '16%'
        repeat: 25,   // '8%'
        symbol: L.Symbol.marker({
          rotate: true,
          markerOptions: {
            icon: L.icon({
              iconUrl: icon_path('iz'),
              iconSize: [16, 16],  // не обязательно
              iconAnchor: [8, 8],
            }),
          },
        }),
      },


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

      // типа граница
      'test3_1': {
        offset: 12,
        repeat: 25,
        symbol: L.Symbol.dash({
          pixelSize: 10,
          pathOptions: {
            color: color,
            weight: 2
          }
        })
      },
      'test3_2': {
        offset: 0,
        repeat: 25,
        symbol: L.Symbol.dash({
          pixelSize: 0
        })
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

