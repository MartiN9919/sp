
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
          title: 'установить период',
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



    //
    // MOUSE
    //

    // MENU: Показать первый уровень
    hm_menu_show(e) {
      const self    = this;
      let limit_delta = this.hm.limit_max - this.hm.limit_min;
      let sel_delta   = this.hm.sel_max   - this.hm.sel_min;

      e.preventDefault();
      e.stopPropagation();
      this.hm.menu_struct = JSON.parse(JSON.stringify(this.hm.menu_struct_base));

      // меню периодов
      this.hm.menu_struct[0].menu.forEach((item, ind) => {
        // пометить:
        // предлагаемый период равен текущему шагу
        if (item.ts == self.hm.sel_step) { self.hm.menu_struct[0].menu[ind].subtitle = 'Шаг'; }
        // недоступно:
        // предлагаемый период меньше текущего шага и больше 0 или
        // предлагаемый период равен текущему периоду
        if (
          ((item.ts < self.hm.sel_step) && (item.ts > 0)) ||
          (((item.ts==0)?limit_delta:item.ts) == sel_delta)
        ) { self.hm.menu_struct[0].menu[ind].disabled = true; }
      });

      // меню шагов
      this.hm.menu_struct[1].menu.forEach((item, ind) => {
        // недоступно:
        // предлагаемый шаг равен текущему шагу
        if (item.ts == self.hm.sel_step) { self.hm.menu_struct[1].menu[ind].disabled = true; }
      });

      this.$refs.hm_menu.show_root(e.clientX, e.clientY);
    },

    // MENU: Установить выделенный период
    hm_menu_sel(menu_item) {
      let sel_min   = this.hm.sel_min;
      let sel_max   = this.hm.sel_max;
      let sel_delta = menu_item.ts;

      if (sel_delta == 0) {                                     // период: вся шкала
        sel_min = this.hm.limit_min;
        sel_max = this.hm.limit_max;
      } else if ((sel_max - sel_delta) >= this.hm.limit_min) {  // период: влево от sel_max полностью
        sel_min = sel_max-sel_delta;

      } else {                                                  // период: влево от sel_max частично
        sel_min = this.hm.limit_min;
        sel_max = Math.min(sel_min+sel_delta, this.hm.limit_max);
      }

      this.hm_prop_sel = [sel_min, sel_max];
    },

    // MENU: Установить шаг изменения выделенного периода
    hm_menu_step(menu_item) {
      let sel_min   = this.hm.sel_min;
      let sel_max   = this.hm.sel_max;
      sel_min -= (sel_min-myUTC) % menu_item.ts;
      sel_max -= (sel_max-myUTC) % menu_item.ts;
      this.hm_prop_sel = [sel_min, sel_max];
      this.hm.sel_step = menu_item.ts;
    },





    //
    // MOUSE
    //

    // MOUSE: обработчик блокировать события мыши
    hm_on_mouse_null(e) {
      let thumb = this.$refs.slider_hm.$el.querySelectorAll('.v-slider__thumb-container');
      thumb[0].blur();
      thumb[1].blur();

      e.preventDefault();
      e.stopPropagation();
    },

    // MOUSE: обработчик mousedown
    hm_on_mouse_down(e) {
      let el     = this.$refs.slider_hm.$el;
      let parent = el.querySelector('.v-slider__track-container');
      let thumb  = el.querySelectorAll('.v-slider__thumb-container');
      thumb[0].blur();
      thumb[1].blur();

      let bounds = parent.getBoundingClientRect();
      let x = e.clientX - bounds.left; // let y = e.clientY - bounds.top;

      const size = 7;
      if (x < (thumb[0].offsetLeft - size)) { e.preventDefault(); e.stopPropagation(); this.hm_sel_move(0); return; } // левее   периода
      if (x > (thumb[1].offsetLeft + size)) { e.preventDefault(); e.stopPropagation(); this.hm_sel_move(1); return; } // правее  периода

      // e.preventDefault(); e.stopPropagation(); - нельзя блокировать
    },




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
