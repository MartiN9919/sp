
import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { myUTC, ts_to_screen, datesql_to_ts } from '@/plugins/sys';

const SEL_STEP_MIN = 60;            // посекундно

export default {
  data: () => ({
    hm: {
      limit_min:   0,               // минимально / максимально допустимое значение, ts
      limit_max:   (60*60*24)|0,
      sel_min:     0,               // выбранное минимальное / максимальное значение, ts
      sel_max:     (60*60*24)|0,
      sel_step:    SEL_STEP_MIN,
      menu_struct: undefined,
      menu_struct_base: [
        {
          title: 'период',
          icon:  'mdi-arrow-expand-horizontal', //'mdi-clock-start',
          menu:  [
            { title: 'все',      icon: 'mdi-calendar-check', action: 'hm_menu_sel', ts: 0, },
            { title: '1 час',    icon: 'mdi-clock-time-one', action: 'hm_menu_sel', ts: 3600, },
            { title: '1 минута', icon: 'mdi-clock-time-one', action: 'hm_menu_sel', ts: 60, },
          ],
        },
        {
          title: 'шаг',
          icon:  'mdi-run',
          menu: [
            { title: 'часы',   icon: 'mdi-clock-time-one',         action: 'hm_menu_step', ts: 3600, },
            { title: 'минуты', icon: 'mdi-clock-time-one-outline', action: 'hm_menu_step', ts: 60, },
          ],
        },
      ],
    },
  }),

  mounted() {
    let el = this.$refs.slider_hm.$el.querySelector('.v-slider');
    el.addEventListener('click',      this.hm_on_mouse_null, {capture: true});
    el.addEventListener('mouseup',    this.hm_on_mouse_null, {capture: true});
    el.addEventListener('mouseleave', this.hm_on_mouse_null, {capture: true});
    el.addEventListener('mousedown',  this.hm_on_mouse_down, {capture: true});
  },

  beforeDestroy() {
    let el = this.$refs.slider_hm.$el.querySelector('.v-slider');
    el.removeEventListener('click',      this.hm_on_mouse_null);
    el.removeEventListener('mouseup',    this.hm_on_mouse_null);
    el.removeEventListener('mouseleave', this.hm_on_mouse_null);
    el.removeEventListener('mousedown',  this.hm_on_mouse_down);
  },


  computed: {
    hm_prop_sel: {
      set: function(lst) {
        let sel_min = lst[0];
        let sel_max = lst[1];
        if ( (sel_min != this.hm.sel_min) || (sel_max != this.hm.sel_max) ) {
          this.hm.sel_max = sel_max;
          this.hm.sel_min = sel_min;
          this.MAP_ACT_REFRESH();
        }
      },
      get: function()    { return [this.hm.sel_min, this.hm.sel_max]; },
    },
    hm_val_min() { return ts_to_screen(this.hm_val_to_ts(this.hm.sel_min), false, true) },
    hm_val_max() { return ts_to_screen(this.hm_val_to_ts(this.hm.sel_max), false, true) },
  },

  methods: {
    // обработчик изменения исходных данных не нужен
    // hm_items_change(items) { },

    // val [0...86400]
    hm_val_to_ts(val) { return val*1000+myUTC },

    // вырезать из ts секунды (для val), 0-начало суток (UTC не используется)
    hm_ts_cut_sec(ts) { return  (((ts-myUTC)/1000) % (60*60*24))|0; },



    // MENU: Показать первый уровень
    hm_menu_show(e) { this.lib_menu_show(e, this.hm, this.$refs.hm_menu); },
    // MENU: Установить выделенный период
    hm_menu_sel(menu_item) { this.hm_prop_sel = this.lib_menu_sel(menu_item, this.hm); },
    // MENU: Установить шаг изменения выделенного периода
    hm_menu_step(menu_item) { this.hm_prop_sel = this.lib_menu_step(menu_item, this.hm); this.hm.sel_step = menu_item.ts; },



    // MOUSE: обработчик блокировать события мыши
    hm_on_mouse_null(e) { this.lib_on_mouse_null(e, this.$refs.slider_hm); },
    // MOUSE: обработчик mousedown
    hm_on_mouse_down(e) { this.lib_on_mouse_down(e, this.$refs.slider_hm, this.hm_sel_move); },




    //
    // SEL
    //

    // SEL: переместить период 0 - влево, 1 - вправо
    hm_sel_move(pos) {
      let sel_min   = this.hm.sel_min;
      let sel_max   = this.hm.sel_max;
      let sel_delta = sel_max - sel_min;
      if (sel_delta==0) return;

      // влево
      if (pos==0) {
        if ((sel_min - sel_delta) < this.hm.limit_min) {
          sel_min = this.hm.limit_min;
          sel_max = this.hm.limit_min+sel_delta;
        } else {
          sel_min -= sel_delta;
          sel_max -= sel_delta;
        }
      // вправо
      } else {
        if ((sel_max + sel_delta) > this.hm.limit_max) {
          sel_min = this.hm.limit_max-sel_delta;
          sel_max = this.hm.limit_max;
        } else {
          sel_min += sel_delta;
          sel_max += sel_delta;
        }
      }

      this.hm_prop_sel = [sel_min, sel_max];
    },

  },

}
