
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



    //
    // MOUSE
    //

    // MENU: Показать первый уровень
    dt_menu_show(e) {
      const self      = this;
      let limit_delta = this.dt.limit_max - this.dt.limit_min;
      let sel_delta   = this.dt.sel_max   - this.dt.sel_min;

      e.preventDefault();
      e.stopPropagation();
      this.dt.menu_struct = JSON.parse(JSON.stringify(this.dt.menu_struct_base));

      // меню периодов
      this.dt.menu_struct[0].menu.forEach((item, ind) => {
        // пометить:
        // предлагаемый период равен текущему шагу
        if (item.ts == self.dt.sel_step) { self.dt.menu_struct[0].menu[ind].subtitle = 'Шаг'; }
        // недоступно:
        // предлагаемый период меньше текущего шага и больше 0 или
        // предлагаемый период равен текущему периоду
        if (
          ((item.ts < self.dt.sel_step) && (item.ts > 0)) ||
          (((item.ts==0)?limit_delta:item.ts) == sel_delta)
        ) { self.dt.menu_struct[0].menu[ind].disabled = true; }
      });

      // меню шагов
      this.dt.menu_struct[1].menu.forEach((item, ind) => {
        // недоступно:
        // предлагаемый шаг равен текущему шагу
        if (item.ts == self.dt.sel_step) { self.dt.menu_struct[1].menu[ind].disabled = true; }
      });

      this.$refs.dt_menu.show_root(e.clientX, e.clientY);
    },

    // MENU: Установить выделенный период
    dt_menu_sel(menu_item) {
      let sel_min   = this.dt.sel_min;
      let sel_max   = this.dt.sel_max;
      let sel_delta = menu_item.ts;

      if (sel_delta == 0) {                                     // период: вся шкала
        sel_min = this.dt.limit_min;
        sel_max = this.dt.limit_max;
      } else if ((sel_max - sel_delta) >= this.dt.limit_min) {  // период: влево от sel_max полностью
        sel_min = sel_max-sel_delta;

      } else {                                                  // период: влево от sel_max частично
        sel_min = this.dt.limit_min;
        sel_max = Math.min(sel_min+sel_delta, this.dt.limit_max);
      }

      this.dt_prop_sel = [sel_min, sel_max];
    },

    // MENU: Установить шаг изменения выделенного периода
    dt_menu_step(menu_item) {
      let sel_min   = this.dt.sel_min;
      let sel_max   = this.dt.sel_max;
      sel_min -= (sel_min-myUTC) % menu_item.ts;
      sel_max -= (sel_max-myUTC) % menu_item.ts;
      this.dt_prop_sel = [sel_min, sel_max];
      this.dt.sel_step = menu_item.ts;
    },





    //
    // MOUSE
    //

    // MOUSE: обработчик блокировать события мыши
    dt_on_mouse_null(e) {
      let thumb = this.$refs.slider_dt.$el.querySelectorAll('.v-slider__thumb-container');
      thumb[0].blur();
      thumb[1].blur();

      e.preventDefault();
      e.stopPropagation();
    },

    // MOUSE: обработчик mousedown
    dt_on_mouse_down(e) {
      let el     = this.$refs.slider_dt.$el;
      let parent = el.querySelector('.v-slider__track-container');
      let thumb  = el.querySelectorAll('.v-slider__thumb-container');
      thumb[0].blur();
      thumb[1].blur();

      let bounds = parent.getBoundingClientRect();
      let x = e.clientX - bounds.left; // let y = e.clientY - bounds.top;

      const size = 7;
      if (x < (thumb[0].offsetLeft - size)) { e.preventDefault(); e.stopPropagation(); this.dt_sel_move(0); return; } // левее   периода
      if (x > (thumb[1].offsetLeft + size)) { e.preventDefault(); e.stopPropagation(); this.dt_sel_move(1); return; } // правее  периода

      // e.preventDefault(); e.stopPropagation(); - нельзя блокировать
    },




    //
    // SEL
    //

    // SEL: переместить период 0 - влево, 1 - вправо
    dt_sel_move(pos) {
      let sel_min   = this.dt.sel_min;
      let sel_max   = this.dt.sel_max;
      let sel_delta = sel_max - sel_min;
      if (sel_delta==0) return;

      // влево
      if (pos==0) {
        if ((sel_min - sel_delta) < this.dt.limit_min) {
          sel_min = this.dt.limit_min;
          sel_max = this.dt.limit_min+sel_delta;
        } else {
          sel_min -= sel_delta;
          sel_max -= sel_delta;
        }
      // вправо
      } else {
        if ((sel_max + sel_delta) > this.dt.limit_max) {
          sel_min = this.dt.limit_max-sel_delta;
          sel_max = this.dt.limit_max;
        } else {
          sel_min += sel_delta;
          sel_max += sel_delta;
        }
      }

      this.dt_prop_sel = [sel_min, sel_max];
    },

  },

}
