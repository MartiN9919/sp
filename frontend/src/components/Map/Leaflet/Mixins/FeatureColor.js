

import { mapGetters, mapActions, } from 'vuex';

import { MAP_ITEM, } from '@/components/Map/Leaflet/Lib/ConstOld';
import { MAP_STYLE, COLORING, } from '@/components/Map/Leaflet/Lib/Const';
import { scale_log, color_array, } from '@/components/Map/Leaflet/Lib/LibColor'
import { fc_key, fc_types_del, } from '@/components/Map/Leaflet/Lib/LibFc'

export default {
  data() {
    return {
    }
  },

  computed: {
    ...mapGetters([
      'SCRIPT_GET_ITEM',
    ]),
  },

  methods: {
    // ЗАПОЛНИТЬ fc.features[i][COLORING.FC.COLOR]
    data_normalize_color(map_ind) {
      // данные на шине
      let map_item = this.SCRIPT_GET_ITEM(map_ind);
      let fc       = map_item[MAP_ITEM.FC];

      // если установлена опция раскраски полигона от value
      if (this.color_dif_valid(map_ind)) {

        // исключить ненужные геометрии
        fc_types_del(fc, ['LineString', 'Point']);

        // COLORING.FC.VALUE определяет цвет полигона
        let val_list    = fc_key(fc, COLORING.FC.VALUE);
        let scale_value = scale_log(val_list);
        let scale_color = color_array(COLORING.COLOR.BEGIN, COLORING.COLOR.END, scale_value.length);

        let feature, value, ret;
        for (let i=0; i<fc.features.length; i++) {
          feature = fc.features[i];
          value   = feature.properties[COLORING.FC.VALUE];
          ret     = scale_color[scale_value.length-1];
          for (let i=0; i<scale_value.length-1; i++) {
            if (value >= scale_value[i] && value < scale_value[i+1]) {
              ret = scale_color[i];
              break;
            }
          }
          feature[COLORING.FC.COLOR] = '#'+ret;
        }

        // построить легенду в map_item
        function color_get(scale_value, value) {
          let ret = scale_color[scale_value.length-1];
          for (let i=0; i<scale_value.length-1; i++) {
            if (value >= scale_value[i] && value < scale_value[i+1]) {
              ret = scale_color[i];
              break;
            }
          }
          return '#'+ret;
        }
        map_item.color_legend = [];
        let from, to;
        for (let i=0; i<scale_value.length; i++) {
          from = scale_value[i];
          to   = scale_value[i+1];
          map_item.color_legend.push({
            color: color_get(scale_value, from+0.00000001),
            from:  from,
            to:    (to!=undefined)?'–'+to:'+',
          });
        }

      // иначе: копировать цвет MAP_ITEM.COLOR каждому feature
      } else if (MAP_ITEM.COLOR in map_item) {
        // for (let i=0; i<fc.features.length; i++) {
        //   fc.features[i][COLORING.FC.COLOR] = map_item[MAP_ITEM.COLOR];
        // }
      }

      // return fc;
    },


    // является ли слой разноцветным (раскраска зависит от value )
    color_dif_valid(map_ind) {
      let map_item = this.SCRIPT_GET_ITEM(map_ind);
      return ([COLORING.GREEN_MIN, COLORING.GREEN_MAX].indexOf(map_item[MAP_STYLE.POLYGON.KEY])>-1);
    },

  },


}
