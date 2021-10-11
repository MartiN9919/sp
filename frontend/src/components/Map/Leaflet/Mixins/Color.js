

import { mapGetters, mapActions, } from 'vuex';

import { MAP_STYLE, COLORING, } from '@/components/Map/Leaflet/Lib/Const';
var MAP_STYLE2 = MAP_STYLE;
var COLORING2 = COLORING;
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
      let map_item    = this.SCRIPT_GET_ITEM(map_ind);
      let color_green = this.color_green(map_ind);
      let fc          = map_item[MAP_STYLE.FC];

      // если установлена опция раскраски полигона от value
      if (this.color_valid(color_green)) {

        // исключить ненужные геометрии
        fc_types_del(fc, ['LineString', 'Point']);

        // начальный и конечный цвет
        var [color_begin, color_end] = this.color_set(color_green);

        // COLORING.FC.VALUE определяет цвет полигона
        let val_list    = fc_key(fc, COLORING2.FC.VALUE);
        let scale_value = scale_log(val_list);
        let scale_color = color_array(color_begin, color_end, scale_value.length);

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

      // иначе: копировать цвет MAP_STYLE.COLOR.KEY каждому feature
      } else if (MAP_STYLE.COLOR.KEY in map_item) {
        // for (let i=0; i<fc.features.length; i++) {
        //   fc.features[i][COLORING.FC.COLOR] = map_item[MAP_STYLE.COLOR.KEY];
        // }
      }

      // return fc;
    },


    // является ли слой разноцветным (раскраска зависит от value )
    color_valid(color_green) {
      return (
        [
          MAP_STYLE.POLYGON.COLORING.GREEN.MIN,
          MAP_STYLE.POLYGON.COLORING.GREEN.MAX,
        ].indexOf(color_green)>-1);
    },

    // тип раскраски (по зеленому цвету)
    color_green(map_ind) {
      return ((((((((
        this.SCRIPT_GET_ITEM(map_ind)
        [MAP_STYLE.FC                       ]) ?? {})
        [MAP_STYLE.KEY                      ]) ?? {})
        [MAP_STYLE.POLYGON.KEY              ]) ?? {})
        [MAP_STYLE.POLYGON.COLORING.KEY     ]) ?? {})
        [MAP_STYLE.POLYGON.COLORING.GREEN.KEY];
    },

    // значения цветов (с, по)
    color_set(color_green) {
      return (color_green == MAP_STYLE.POLYGON.COLORING.GREEN.MIN) ?
        [MAP_STYLE.POLYGON.COLORING.BEGIN, MAP_STYLE.POLYGON.COLORING.END  ] :
        [MAP_STYLE.POLYGON.COLORING.END,   MAP_STYLE.POLYGON.COLORING.BEGIN];
    },

  },


}
