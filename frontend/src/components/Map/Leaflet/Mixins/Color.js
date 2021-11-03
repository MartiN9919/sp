// РАСКРАСКА ПОЛИГОНА ОТ ЗНАЧЕНИЯ
// вход:  fc.features[i].properties[MAP_ITEM.FC.FEATURES.PROPERTIES.VALUE       ] - значение определяет цвет полигона
// выход: fc.features[i].properties[MAP_ITEM.FC.FEATURES.PROPERTIES._FILL_COLOR_] - расчитанный цвет полигона


import { mapGetters, mapActions, } from 'vuex';

import { MAP_CONST, MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { dict_get } from '@/components/Map/Leaflet/Lib/Lib';
import { color_scale_log, color_array, } from '@/components/Map/Leaflet/Lib/LibColor'
import { fc_properties_keys_get, fc_types_del, } from '@/components/Map/Leaflet/Lib/LibFc'

export default {
  computed: {
    ...mapGetters([
      'SCRIPT_GET_ITEM',
    ]),
  },

  methods: {
    // ЗАПОЛНИТЬ fc.features[i].properties[MAP_ITEM.FC.FEATURES.PROPERTIES._FILL_COLOR_]
    data_normalize_color(map_item) {
      // данные на шине
      let color_green = this.color_green(map_item);
      let fc          = map_item.fc;

      // если установлена опция раскраски полигона от value
      if (this.color_valid(color_green)) {

        // исключить ненужные геометрии
        fc_types_del(fc, [MAP_CONST.TYPE_GEOMETRY.LINE, MAP_CONST.TYPE_GEOMETRY.POINT]);

        // начальный и конечный цвет
        var [color_begin, color_end] = this.color_set(color_green);

        // MAP_ITEM.FC.FEATURES.PROPERTIES.VALUE определяет цвет полигона
        let val_list    = fc_properties_keys_get(fc, MAP_ITEM.FC.FEATURES.PROPERTIES.VALUE);  // список fc.features[i].properties.value
        let scale_value = color_scale_log(val_list);                                          // шкала значений
        let scale_color = color_array(color_begin, color_end, scale_value.length);            // шкала цветов

        let feature, value, ret;
        for (let i=0; i<fc.features.length; i++) {
          feature = fc.features[i];
          value   = feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.VALUE];
          ret     = scale_color[scale_value.length-1];
          for (let i=0; i<scale_value.length-1; i++) {
            if (value >= scale_value[i] && value < scale_value[i+1]) {
              ret = scale_color[i];
              break;
            }
          }
          feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES._FILL_COLOR_] = '#'+ret;    // записать цвет
        }

        // построить легенду в MAP_ITEM._LEGEND_COLOR_
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
        map_item[MAP_ITEM._LEGEND_COLOR_] = [];
        let from, to;
        for (let i=0; i<scale_value.length; i++) {
          from = scale_value[i];
          to   = scale_value[i+1];
          map_item[MAP_ITEM._LEGEND_COLOR_].push({
            color: color_get(scale_value, from+0.00000001),
            from:  from,
            to:    (to!=undefined)?'–'+to:'+',
          });
        }
      }
    },


    // является ли слой разноцветным (раскраска зависит от value )
    color_valid(color_green) {
      return (
        [
          MAP_CONST.COLOR.COLORING.GREEN_MIN,
          MAP_CONST.COLOR.COLORING.GREEN_MAX,
        ].indexOf(color_green)>-1);
    },

    // тип раскраски (по зеленому цвету)
    color_green(map_item) {
      return dict_get(map_item, ['fc', MAP_ITEM.FC.STYLE.KEY, MAP_ITEM.FC.STYLE.COLORING, ], undefined);
    },

    // значения цветов (с, по)
    color_set(color_green) {
      return (color_green == MAP_CONST.COLOR.COLORING.GREEN_MIN) ?
        [MAP_CONST.COLOR.COLORING.BEGIN, MAP_CONST.COLOR.COLORING.END  ] :
        [MAP_CONST.COLOR.COLORING.END,   MAP_CONST.COLOR.COLORING.BEGIN];
    },

  },


}
