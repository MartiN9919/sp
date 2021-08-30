

import { mapGetters, mapActions, } from 'vuex';

import { MAP_ITEM, } from '@/components/Leaflet/L.Const';
import { scale_log, color_array, } from '@/components/Leaflet/L.Lib'
import { fc_key, fc_types_del, } from '@/components/Leaflet/L.LibFc'

const COLOR_BEGIN = '00FF00';       // цвет: начальный
const COLOR_END   = 'FF0000';       // цвет: конечный
const COLOR_KEY   = 'value';        // property[COLOR_KEY]: значение определяет цвет полигона

export default {
  data() {
    return {
    }
  },

  computed: {
    ...mapGetters([
      'MAP_GET_ITEM',
    ]),
  },

  methods: {
    // ЗАПОЛНИТЬ MAP_ITEM.FC.features[i][MAP_ITEM.FC_COLOR]
    data_normalize_color(map_ind) {
      // данные на шине
      let map_item = this.MAP_GET_ITEM(map_ind);
      let fc       = map_item[MAP_ITEM.FC];

      // если установлена опция раскраски полигона от value
      if (this.color_dif_valid(map_ind)) {

        // исключить ненужные геометрии
        fc_types_del(fc, ['LineString', 'Point']);

        // MAP_ITEM.FC_PROP_VALUE значение которого определяет цвет полигона
        let val_list    = fc_key(fc, COLOR_KEY);
        let scale_value = scale_log(val_list);
        let scale_color = color_array(COLOR_BEGIN, COLOR_END, scale_value.length);

        let feature, value, ret;
        for (let i=0; i<fc.features.length; i++) {
          feature = fc.features[i];
          value   = feature.properties[COLOR_KEY];
          ret     = scale_color[scale_value.length-1];
          for (let i=0; i<scale_value.length-1; i++) {
            if (value >= scale_value[i] && value < scale_value[i+1]) {
              ret = scale_color[i];
              break;
            }
          }
          feature[MAP_ITEM.FC_COLOR] = '#'+ret;
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
        //   fc.features[i][MAP_ITEM.FC_COLOR] = map_item[MAP_ITEM.COLOR];
        // }
      }

      // return fc;
    },


    // является ли слой разноцветным (раскраска зависит от value )
    color_dif_valid(map_ind) {
      let map_item = this.MAP_GET_ITEM(map_ind);
      return ([MAP_ITEM.POLYGON.GREEN_MIN, MAP_ITEM.POLYGON.GREEN_MAX].indexOf(map_item[MAP_ITEM.POLYGON.NAME])>-1);
    },

  },


}
