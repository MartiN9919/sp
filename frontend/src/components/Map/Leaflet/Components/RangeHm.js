
import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { myUTC, ts_to_screen, datesql_to_ts } from '@/plugins/sys';

export default {
  data: () => ({
    hm: {
      limit_min:   0,              // минимально / максимально допустимое значение, ts
      limit_max:   0,
      sel_min:     0,              // выбранное минимальное / максимальное значение, ts
      sel_max:     0,
      sel_step:    0,
      menu_struct: undefined,
      menu_struct_base: [
        {
          title: 'период 2',
          icon:  'mdi-arrow-expand-horizontal', //'mdi-clock-start',
          menu:  [
            { title: 'все',      icon: 'mdi-calendar-check', action: 'hm_menu_period', ts: 0, },
            //{ divider: true },
            { title: '30 суток', icon: 'mdi-calendar-month', action: 'hm_menu_period', ts: 1000*2592000, },
            { title: '1 неделя', icon: 'mdi-calendar-range', action: 'hm_menu_period', ts: 1000*604800, },
            { title: '1 сутки',  icon: 'mdi-calendar-today', action: 'hm_menu_period', ts: 1000*86400, },
            { title: '1 час',    icon: 'mdi-clock-time-one', action: 'hm_menu_period', ts: 1000*3600, },
          ],
        },
        {
          title: 'округлить до',
          icon:  'mdi-content-cut',
          menu: [
            { title: 'суток', icon: 'mdi-calendar-blank', action: 'hm_menu_round', round: 'day', },
            { title: 'часов', icon: 'mdi-clock',          action: 'hm_menu_round', round: 'hour', },
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
      set: function(lst) { this.hm_sel_set(lst[0], lst[1]); },
      get: function()    { return [this.hm.sel_min, this.hm.sel_max]; },
    },
    hm_val_min() { return ts_to_screen(this.hm_prop_sel[0]) },
    hm_val_max() { return ts_to_screen(this.hm_prop_sel[1]) },
  },

  methods: {
    // обработчик изменения исходных данных
    hm_items_change(items) {
      // установить мин и макс
      let hm_limit_min = '';
      let hm_limit_max = '';
      items.forEach(function(item){
        item.fc.features.forEach(function(feature){
          let date = feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.DATE];
          if (!date) return;
          if ((date < hm_limit_min) || (hm_limit_min == '')) hm_limit_min=date;
          if ((date > hm_limit_max) || (hm_limit_max == '')) hm_limit_max=date;
        }.bind(this));
      }.bind(this));
      this.hm.limit_min = datesql_to_ts(hm_limit_min);
      this.hm.limit_max = datesql_to_ts(hm_limit_max);

      // скорректирвать выбранный диапазон
      let sel_min = ((this.hm.limit_min <= this.hm.sel_min) && ( this.hm.sel_min <= this.hm.limit_max))?this.hm.sel_min:this.hm.limit_min;
      let sel_max = ((this.hm.limit_min <= this.hm.sel_max) && ( this.hm.sel_max <= this.hm.limit_max))?this.hm.sel_max:this.hm.limit_max;
      this.hm_sel_set(sel_min, sel_max);
    },



    //
    // MOUSE
    //

    // MENU: Показать первый уровень
    hm_menu_show(e) {
      const self    = this;
      let sel_delta = this.hm.sel_max - this.hm.sel_min;

      e.preventDefault();
      e.stopPropagation();
      this.hm.menu_struct = JSON.parse(JSON.stringify(this.hm.menu_struct_base));
      // текущий выбор периода недоступен
      this.hm.menu_struct[0].menu.forEach((item, ind) => {
        if (                                                                                   // доступность
          (self.hm.sel_step == item.ts) &&                                                     // шаг шкалы равен периоду и
          (sel_delta == ((item.ts==0)?(self.hm.limit_max-self.hm.limit_min):self.hm.sel_step)) // выбран только один шаг шкалы (для ВСЕ выбрано все)
        ) { self.hm.menu_struct[0].menu[ind].disabled = true; }
        if (self.hm.step  == item.ts) {                                                        // текущий выбор: шаг шкалы равен периоду
          self.hm.menu_struct[0].menu[ind].subtitle = 'Выбрано';
        }
      });
      this.$refs.menu.show_root(e.clientX, e.clientY);
    },

    // MENU: Установить период
    hm_menu_period(menu_item) {
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

      this.hm_sel_set(sel_min, sel_max, sel_delta);
    },

    // MENU: Округлить период
    hm_menu_round(menu_item) {
      let sel_min   = this.hm.sel_min;
      let sel_max   = this.hm.sel_max;

      sel_min -= myUTC;
      sel_max -= myUTC;
      switch (menu_item.round) {
        case 'day':                               // округлить до суток
          sel_min -= sel_min % (24 * 60 * 60 * 1000);
          sel_max -= sel_max % (24 * 60 * 60 * 1000);
          break;
        case 'hour':                              // округлить до часов
          sel_min -= sel_min % (60 * 60 * 1000);
          sel_max -= sel_max % (60 * 60 * 1000);
          break;
      }
      sel_min += myUTC;
      sel_max += myUTC;

      this.hm_sel_set(sel_min, sel_max);
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

      this.hm_sel_set(sel_min, sel_max);
    },

    // SEL: установить период корректно
    async hm_sel_set(sel_min, sel_max, sel_step_new=undefined) {
      if (
        (sel_min == this.hm.sel_min) &&
        (sel_max == this.hm.sel_max) &&
        (sel_step_new == undefined)
      ) return;

      let step_temp = (sel_step_new != undefined) ? sel_step_new : this.hm.sel_step;
      this.hm.sel_step = 0;
      this.hm.sel_min  = sel_min;
      this.hm.sel_max  = sel_max;
      this.hm.sel_step = step_temp;
      await this.MAP_ACT_REFRESH();
    }

  },

}
