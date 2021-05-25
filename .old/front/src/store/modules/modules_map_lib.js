
import {
  datesql_to_ts,
} from '@/plugins/sys';


export function  MAP_FUN_RANGE_TS(state) {
  // установить мин и макс даты
  let date_min = '';
  let date_max = '';
  state.map.forEach(function(layer){
    layer.fc.features.forEach(function(feature){
      let date = feature.properties.date;
      if (!date) return;
      if ((date < date_min) || (date_min == '')) date_min=date;
      if ((date > date_max) || (date_max == '')) date_max=date;
    }.bind(this));
  }.bind(this));
  state.range.limit_min = datesql_to_ts(date_min);
  state.range.limit_max = datesql_to_ts(date_max);

  // скорректирвать выбранный диапазон
  state.range.sel_min = ((state.range.limit_min <= state.range.sel_min) && ( state.range.sel_min <= state.range.limit_max))?state.range.sel_min:state.range.limit_min;
  state.range.sel_max = ((state.range.limit_min <= state.range.sel_max) && ( state.range.sel_max <= state.range.limit_max))?state.range.sel_max:state.range.limit_max;
}
