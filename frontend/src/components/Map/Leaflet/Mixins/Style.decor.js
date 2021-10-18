import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { dict_get } from '@/components/Map/Leaflet/Lib/Lib';
import { fc_key, fc_types_del, } from '@/components/Map/Leaflet/Lib/LibFc';

export default {
  data: () => ({
    style_patterns: [
      {
        offset: 12,
        repeat: 25,
        symbol: L.Symbol.arrowHead({
          pixelSize: 15,
          pathOptions: { color: "#f00", weight: 2, stroke: true },
        }),
      },
    ],
    style_decor_path: [
      // [47.334852, -1.509485],
      // [47.342596, -1.328731],
      // [47.241487, -1.190568],
      // [47.234787, -1.358337],
    ],
  }),

  methods: {
    style_decor_set(map_ind, map_item, fc) {
      //
      let fc_copy = JSON.parse(JSON.stringify(fc));
      fc_types_del(fc_copy, ['Point']);
      console.log(map_ind, map_item, fc)
      this.style_decor_path[map_ind] = [];
      for(let ind=0; ind<fc[MAP_ITEM.FC.FEATURES.KEY].length; ind++) {
        let tt = dict_get(fc_copy[MAP_ITEM.FC.FEATURES.KEY][ind], [MAP_ITEM.FC.FEATURES.GEOMETRY.KEY, MAP_ITEM.FC.FEATURES.GEOMETRY.COORDINATES.KEY], []);
        console.log(11, tt)
        this.style_decor_path[map_ind] = this.style_decor_path[map_ind].concat(tt);
      }
      console.log(22, this.style_decor_path[map_ind])

    },

    style_decor_get(map_ind, map_item) {
      return this.style_decor_path[map_ind];

      // this.style_patterns = [
      //   {
      //     offset: 12,
      //     repeat: 25,
      //     symbol: L.Symbol.arrowHead({
      //       pixelSize: 15,
      //       pathOptions: { color: "#00f", weight: 2, stroke: true },
      //     }),
      //   },
      // ];
      // return [
      //   [47.334852, -2.509485],
      //   [47.342596, -1.328731],
      //   [47.241487, -1.190568],
      //   [47.234787, -1.358337],
      // ];


      // var markerLine = L.polyline([[58.44773, -28.65234], [52.9354, -23.33496], [53.01478, -14.32617], [58.1707, -10.37109], [59.68993, -0.65918]], {}).addTo(this.map);
      // var markerPatterns = L.polylineDecorator(markerLine, {
      //   patterns: [
      //     { offset: '5%', repeat: '10%', symbol: L.Symbol.marker()}
      //   ]
      // }).addTo(this.map);
    },

  },


}