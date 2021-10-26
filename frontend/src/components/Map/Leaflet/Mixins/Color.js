// РАСКРАСКА ПОЛИГОНА ОТ ЗНАЧЕНИЯ
// вход:  fc.features[i].property.value - значение определяет цвет полигона
// выход: fc.features[i].color - расчитанный цвет полигона


import { mapGetters, mapActions, } from 'vuex';

import { MAP_CONST, MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { color_scale_log, color_array, } from '@/components/Map/Leaflet/Lib/LibColor'
import { fc_properties_keys_get, fc_types_del, } from '@/components/Map/Leaflet/Lib/LibFc'

export default {
  // data() {
  //   return {
  //   }
  // },

  computed: {
    ...mapGetters([
      'SCRIPT_GET_ITEM',
    ]),
  },

  methods: {
    // ЗАПОЛНИТЬ fc.features[i][MAP_ITEM.COLOR]
    data_normalize_color(map_item) {
      // данные на шине
      let color_green = this.color_green(map_item);
      let fc          = map_item[MAP_ITEM.FC.KEY];

      // если установлена опция раскраски полигона от value
      if (this.color_valid(color_green)) {

        // исключить ненужные геометрии
        fc_types_del(fc, [MAP_CONST.GEOMETRY_TYPE.LINE, MAP_CONST.GEOMETRY_TYPE.POINT]);

        // начальный и конечный цвет
        var [color_begin, color_end] = this.color_set(color_green);

        // COLORING.FC.VALUE.KEY определяет цвет полигона
        let val_list    = fc_properties_keys_get(fc, MAP_ITEM.FC.FEATURES.PROPERTIES.VALUE.KEY);  // список fc.features[i].properties.value
        let scale_value = color_scale_log(val_list);                                              // шкала значений
        let scale_color = color_array(color_begin, color_end, scale_value.length);                // шкала цветов

        let feature, value, ret;
        for (let i=0; i<fc.features.length; i++) {
          feature = fc.features[i];
          value   = feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.VALUE.KEY];
          ret     = scale_color[scale_value.length-1];
          for (let i=0; i<scale_value.length-1; i++) {
            if (value >= scale_value[i] && value < scale_value[i+1]) {
              ret = scale_color[i];
              break;
            }
          }
          feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES._COLOR_.KEY] = '#'+ret;    // записать цвет
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

      // // иначе: копировать цвет MAP_ITEM.COLOR каждому feature
      // } else if (MAP_ITEM.COLOR in map_item) {
      //   // for (let i=0; i<fc.features.length; i++) {
      //   //   fc.features[i][MAP_ITEM.FC.FEATURES.PROPERTIES._COLOR_] = map_item[MAP_ITEM.COLOR];
      //   // }
      }
    },


    // является ли слой разноцветным (раскраска зависит от value )
    color_valid(color_green) {
      return (
        [
          MAP_ITEM.FC.STYLE.POLYGON.COLORING.GREEN.MIN,
          MAP_ITEM.FC.STYLE.POLYGON.COLORING.GREEN.MAX,
        ].indexOf(color_green)>-1);
    },

    // тип раскраски (по зеленому цвету)
    color_green(map_item) {
      return ((((((((
        map_item
        [MAP_ITEM.FC.KEY                            ]) ?? {})
        [MAP_ITEM.FC.STYLE.KEY                      ]) ?? {})
        [MAP_ITEM.FC.STYLE.POLYGON.KEY              ]) ?? {})
        [MAP_ITEM.FC.STYLE.POLYGON.COLORING.KEY     ]) ?? {})
        [MAP_ITEM.FC.STYLE.POLYGON.COLORING.GREEN.KEY];
    },

    // значения цветов (с, по)
    color_set(color_green) {
      return (color_green == MAP_ITEM.FC.STYLE.POLYGON.COLORING.GREEN.MIN) ?
        [MAP_ITEM.FC.STYLE.POLYGON.COLORING.BEGIN, MAP_ITEM.FC.STYLE.POLYGON.COLORING.END  ] :
        [MAP_ITEM.FC.STYLE.POLYGON.COLORING.END,   MAP_ITEM.FC.STYLE.POLYGON.COLORING.BEGIN];
    },

  },


}
