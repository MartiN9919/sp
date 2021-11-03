/* СПИСКИ ДЕКОРАТОРОВ ДЛЯ ЛИНИЙ И ГРАНИЦ ПОЛИГОНОВ
 * key - название класса, указывается в MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS
 * color - подставляется автоматически
 * offset - смещение первого маркера от начала, можно в %: '100%'
 * repeat - смещение, через которое повторить маркер, можно в %: '50%'
 */

import { STYLE_DATA_FORCE_DECOR      } from '@/components/Map/Leaflet/Components/Style/StyleDataForce';
import { STYLE_DATA_CHECKPOINT_DECOR } from '@/components/Map/Leaflet/Components/Style/StyleDataCheckpoint';
import { STYLE_DATA_ENGENEER_DECOR   } from '@/components/Map/Leaflet/Components/Style/StyleDataEngeneer';
import { STYLE_DATA_LAYOUT_DECOR     } from '@/components/Map/Leaflet/Components/Style/StyleDataLayout';
import { STYLE_DATA_TEXT_DECOR       } from '@/components/Map/Leaflet/Components/Style/StyleDataText';
import { STYLE_DATA_COMMON_DECOR     } from '@/components/Map/Leaflet/Components/Style/StyleDataCommon';
import { STYLE_DATA_TEST_DECOR       } from '@/components/Map/Leaflet/Components/Style/StyleDataTest';
import { icon_get                    } from '@/components/Map/Leaflet/Components/Style/StyleIcon';

const DATA = {
  ...STYLE_DATA_FORCE_DECOR,
  ...STYLE_DATA_CHECKPOINT_DECOR,
  ...STYLE_DATA_ENGENEER_DECOR,
  ...STYLE_DATA_LAYOUT_DECOR,
  ...STYLE_DATA_TEXT_DECOR,
  ...STYLE_DATA_COMMON_DECOR,
  ...STYLE_DATA_TEST_DECOR,
}

import { MAP_CONST, MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
export function get_decor_data(classes_str, index, color="gray", zoom=1, icon_properties={}) {
  let ret = [];
  let classes_list = classes_str.trim().replace(/\s+/g, ' ').split(' ');  // убрать лишние пробелы
  classes_list = [...new Set(classes_list)];                              // исключить повторы

  // перебрать классы
  classes_list.forEach(function(class_item, class_ind) {
    let data = DATA[class_item];
    if (data === undefined) return;
    data = JSON.parse(JSON.stringify(data));
    if (!(data instanceof Array)) data = [data];                          // к единому формату

    data.forEach(function(data_item, data_ind) {
      // тип: маркер
      if (data[data_ind].symbol_type == 'marker') {
        data[data_ind].symbol_options.markerOptions.icon = icon_get(color, {
          [MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS   ]: data[data_ind].symbol_options.markerOptions.icon,
          ...icon_properties,
          ...data[data_ind].icon_properties,
        });
        data[data_ind].symbol = L.Symbol.marker(data[data_ind].symbol_options);
      }

      // тип: штрих
      if (data[data_ind].symbol_type == 'dash') {
        if (data[data_ind].symbol_options.pathOptions.color == '{color}') data[data_ind].symbol_options.pathOptions.color = color;
        data[data_ind].symbol = L.Symbol.dash(data[data_ind].symbol_options);
      }

      // тип: стрелка
      if (data[data_ind].symbol_type == 'arrow') {
        if (data[data_ind].symbol_options.pathOptions.color == '{color}') data[data_ind].symbol_options.pathOptions.color = color;
        data[data_ind].symbol = L.Symbol.arrowHead(data[data_ind].symbol_options);
      }

      // удалить ставшие ненужными записи
      if (data[data_ind].symbol_type     != undefined) delete data[data_ind]['symbol_type'    ];
      if (data[data_ind].symbol_options  != undefined) delete data[data_ind]['symbol_options' ];
      if (data[data_ind].icon_properties != undefined) delete data[data_ind]['icon_properties'];

      // запомнить результат
      ret.push(data[data_ind]);
    });
  });
  return ret;
}
