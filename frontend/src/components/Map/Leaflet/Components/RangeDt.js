
import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { myUTC, ts_to_screen, datesql_to_ts } from '@/plugins/sys';

const SEL_STEP_MIN = 60*1000;     // посекундно

export default {
  data: () => ({
    dt: {
      limit_min:   0,             // минимально / максимально допустимое значение, ts
      limit_max:   0,
      sel_min:     0,             // выбранное минимальное / максимальное значение, ts
      sel_max:     0,
      sel_step:    SEL_STEP_MIN,
      hint:        '111',
      menu_struct: undefined,
      menu_struct_base: [
        {
          title: 'период',
          icon:  'mdi-arrow-expand-horizontal', //'mdi-clock-start',
          menu:  [
            { title: 'все',      icon: 'mdi-calendar-check', action: 'dt_menu_sel', ts: 0, },
            { title: '30 суток', icon: 'mdi-calendar-month', action: 'dt_menu_sel', ts: 1000*2592000, },
            { title: '1 неделя', icon: 'mdi-calendar-range', action: 'dt_menu_sel', ts: 1000*604800, },
            { title: '1 сутки',  icon: 'mdi-calendar-today', action: 'dt_menu_sel', ts: 1000*86400, },
            { title: '1 час',    icon: 'mdi-clock-time-one', action: 'dt_menu_sel', ts: 1000*3600, },
          ],
        },
        {
          title: 'шаг',
          icon:  'mdi-run',
          menu: [
            { title: 'сутки',  icon: 'mdi-calendar-blank',         action: 'dt_menu_step', ts: 1000*86400, },
            { title: 'часы',   icon: 'mdi-clock-time-one',         action: 'dt_menu_step', ts: 1000*3600, },
            { title: 'минуты', icon: 'mdi-clock-time-one-outline', action: 'dt_menu_step', ts: 1000*60, },
          ],
        },
      ],
    },
  }),

  mounted() {
    let el = this.$refs.slider_dt.$el.querySelector('.v-slider');
    el.addEventListener('click',      this.dt_on_mouse_null, {capture: true});
    el.addEventListener('mouseup',    this.dt_on_mouse_null, {capture: true});
    el.addEventListener('mouseleave', this.dt_on_mouse_null, {capture: true});
    el.addEventListener('mousedown',  this.dt_on_mouse_down, {capture: true});
  },

  beforeDestroy() {
    let el = this.$refs.slider_dt.$el.querySelector('.v-slider');
    el.removeEventListener('click',      this.dt_on_mouse_null);
    el.removeEventListener('mouseup',    this.dt_on_mouse_null);
    el.removeEventListener('mouseleave', this.dt_on_mouse_null);
    el.removeEventListener('mousedown',  this.dt_on_mouse_down);
  },


  computed: {
    dt_prop_sel: {
      set: function(lst) {
        let sel_min = lst[0];
        let sel_max = lst[1];
        if ( (sel_min != this.dt.sel_min) || (sel_max != this.dt.sel_max) ) {
          this.dt.sel_max = sel_max;
          this.dt.sel_min = sel_min;
          this.MAP_ACT_REFRESH();
        }
      },
      get: function()    { return [this.dt.sel_min, this.dt.sel_max]; },
    },
    dt_val_min() { return ts_to_screen(this.dt.sel_min, true, true) },
    dt_val_max() { return ts_to_screen(this.dt.sel_max, true, true) },
  },

  methods: {
    // обработчик изменения исходных данных
    dt_items_change(items) {
      // установить мин и макс
      let dt_limit_min = '';
      let dt_limit_max = '';
      items.forEach(function(item){
        item.fc.features.forEach(function(feature){
          let date = feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.DATE];
          if (!date) return;
          if ((date < dt_limit_min) || (dt_limit_min == '')) dt_limit_min=date;
          if ((date > dt_limit_max) || (dt_limit_max == '')) dt_limit_max=date;
        }.bind(this));
      }.bind(this));
      this.dt.limit_min = datesql_to_ts(dt_limit_min);
      this.dt.limit_max = datesql_to_ts(dt_limit_max);

      // скорректирвать выбранный диапазон
      let sel_min = ((this.dt.limit_min <= this.dt.sel_min) && ( this.dt.sel_min <= this.dt.limit_max))?this.dt.sel_min:this.dt.limit_min;
      let sel_max = ((this.dt.limit_min <= this.dt.sel_max) && ( this.dt.sel_max <= this.dt.limit_max))?this.dt.sel_max:this.dt.limit_max;
      this.dt_prop_sel = [sel_min, sel_max];
    },



    // MENU: Показать первый уровень
    dt_menu_show(e) { this.lib_menu_show(e, this.dt, this.$refs.dt_menu); },
    // MENU: Установить выделенный период
    dt_menu_sel(menu_item) { this.dt_prop_sel = this.lib_menu_sel(menu_item, this.dt); },
    // MENU: Установить шаг изменения выделенного периода
    dt_menu_step(menu_item) { this.dt_prop_sel = this.lib_menu_step(menu_item, this.dt); this.dt.sel_step = menu_item.ts; },


    // MOUSE: обработчик блокировать события мыши
    dt_on_mouse_null(e) { this.lib_on_mouse_null(e, this.$refs.slider_dt); },
    // MOUSE: обработчик mousedown
    dt_on_mouse_down(e) { this.lib_on_mouse_down(e, this.$refs.slider_dt, this.dt_sel_move); },


    // SEL: переместить период 0 - влево, 1 - вправо
    dt_sel_move(pos) { this.dt_prop_sel = this.lib_sel_move(pos, this.dt); },
  },

}
