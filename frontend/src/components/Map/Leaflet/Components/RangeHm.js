
import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { myUTC, ts_to_screen, datesql_to_ts } from '@/plugins/sys';

export default {
  computed: {
    hm_val_min() { return ts_to_screen(this.dt_prop_sel[0]) },
    hm_val_max() { return ts_to_screen(this.dt_prop_sel[1]) },
  },

  methods: {
    // обработчик изменения исходных данных
    hm_items_change(items) {
      // установить мин и макс
    },
  },
}
