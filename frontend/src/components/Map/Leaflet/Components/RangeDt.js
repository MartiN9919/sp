export default {
  mounted() {
    let el = this.$refs.slider_dt.$el.querySelector('.v-slider');
    el.addEventListener('click',      this.on_mouse_reset_dt,      {capture: true});
    el.addEventListener('mouseup',    this.on_mouse_reset_dt,      {capture: true});
    el.addEventListener('mouseleave', this.on_mouse_reset_dt,      {capture: true});
    el.addEventListener('mousedown',  this.on_mousedown_slider_dt, {capture: true});
  },

  beforeDestroy() {
    let el = this.$refs.slider_dt.$el.querySelector('.v-slider');
    el.removeEventListener('click',      this.on_mouse_reset_dt);
    el.removeEventListener('mouseup',    this.on_mouse_reset_dt);
    el.removeEventListener('mouseleave', this.on_mouse_reset_dt);
    el.removeEventListener('mousedown',  this.on_mousedown_slider_dt);
  },


  methods: {
    // MENU: Показать первый уровень
    on_menu_dt_show(e) {
      const self    = this;
      let sel_delta = this.dt.sel_max - this.dt.sel_min;

      e.preventDefault();
      e.stopPropagation();
      this.dt.menu_struct = JSON.parse(JSON.stringify(this.dt.menu_struct_base));
      // текущий выбор периода недоступен
      this.dt.menu_struct[0].menu.forEach((item, ind) => {
        if (                                                                                   // доступность
          (self.dt.sel_step == item.ts) &&                                                     // шаг шкалы равен периоду и
          (sel_delta == ((item.ts==0)?(self.dt.limit_max-self.dt.limit_min):self.dt.sel_step)) // выбран только один шаг шкалы (для ВСЕ выбрано все)
        ) { self.dt.menu_struct[0].menu[ind].disabled = true; }
        if (self.dt.step  == item.ts) {                                                        // текущий выбор: шаг шкалы равен периоду
          self.dt.menu_struct[0].menu[ind].subtitle = 'Выбрано';
        }
      });
      this.$refs.menu.show_root(e.clientX, e.clientY);
    },

    // MENU: Установить период
    async on_period_dt(menu_item) {
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

      await this.set_range_dt_sel(sel_min, sel_max, sel_delta);
    },

    // MENU: Округлить период
    async on_round_dt(menu_item) {
      let sel_min   = this.dt.sel_min;
      let sel_max   = this.dt.sel_max;

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

      await this.set_range_dt_sel(sel_min, sel_max);
  },




  },

}
