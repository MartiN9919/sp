
import { myUTC } from '@/plugins/sys';
import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';

export default {
  methods: {

    // MARK: обновить
    lib_mark_refresh(data, mark, fun_converter) {
      if (mark == undefined) return;
      let ctx = mark.getContext('2d');

      let self        = this;
      let limit_delta = data.limit_max  - data.limit_min;
      let logic_width = this.mark.width - this.mark.margin_x - this.mark.margin_x;
      ctx.beginPath();
      try {
        ctx.clearRect(0, 0, this.mark.width, this.mark.height);
        ctx.strokeStyle   = this.mark.strokeStyle;
        ctx.lineWidth     = this.mark.lineWidth;
        ctx.shadowColor   = this.mark.shadowColor;
        ctx.shadowBlur    = this.mark.shadowBlur;

        let items = this.SCRIPT_GET;
        items.forEach(function(item){
          item.fc.features.forEach(function(feature){
            let date = feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.DATE];
            if (!date) return;
            let x = self.mark.margin_x + ((fun_converter(date)-data.limit_min)*logic_width/limit_delta)|0;
            ctx.moveTo(x, self.mark.lineHeightStart);
            ctx.lineTo(x, self.mark.lineHeightEnd);
          });
        });
      } finally {
        if (ctx != undefined) { ctx.stroke(); ctx.closePath(); }
      }
    },



    //
    // MENU
    //

    // MENU: Показать первый уровень
    lib_menu_show(e, data, menu) {
      let limit_delta  = data.limit_max - data.limit_min;
      let sel_delta    = data.sel_max   - data.sel_min;
      data.menu_struct = JSON.parse(JSON.stringify(data.menu_struct_base));

      // меню периодов
      data.menu_struct[1].menu.forEach((item, ind) => {
        // пометить:
        // предлагаемый период равен текущему шагу
        if (item.ts == data.sel_step) { data.menu_struct[1].menu[ind].subtitle = 'Шаг'; }
        // недоступно:
        // предлагаемый период меньше текущего шага и больше 0 или
        // предлагаемый период равен текущему периоду
        if (
          ((item.ts < data.sel_step) && (item.ts > 0)) ||
          (((item.ts==0)?limit_delta:item.ts) == sel_delta)
        ) { data.menu_struct[1].menu[ind].disabled = true; }
      });

      // меню шагов
      data.menu_struct[2].menu.forEach((item, ind) => {
        // недоступно:
        // предлагаемый шаг равен текущему шагу
        if (item.ts == data.sel_step) { data.menu_struct[2].menu[ind].disabled = true; }
      });

      // прервать обработку click-события и показать меню
      e.preventDefault();
      e.stopPropagation();
      menu.show_root(e.clientX, e.clientY);
    },


    // MENU: Сбросить настройки
    lib_menu_reset() {
      this.dt.sel_step = this.dt_sel_step_min_default();
      this.dt_prop_sel = [this.dt.limit_min, this.dt.limit_max];
      this.hm.sel_step = this.hm_sel_step_min_default();
      this.hm_prop_sel = [this.hm.limit_min, this.hm.limit_max];
    },


    // MENU: Установить выделенный период
    lib_menu_sel(menu_item, data) {
      let sel_min   = data.sel_min;
      let sel_max   = data.sel_max;
      let sel_delta = menu_item.ts;

      if (sel_delta == 0) {                                     // период: вся шкала
        sel_min = data.limit_min;
        sel_max = data.limit_max;
      } else if ((sel_max - sel_delta) >= data.limit_min) {     // период: влево от sel_max полностью
        sel_min = sel_max-sel_delta;

      } else {                                                  // период: влево от sel_max частично
        sel_min = data.limit_min;
        sel_max = Math.min(sel_min+sel_delta, data.limit_max);
      }

      return [sel_min, sel_max];
    },



    // MENU: Установить шаг изменения выделенного периода
    lib_menu_step(menu_item, data) {
      let sel_min = data.sel_min;
      let sel_max = data.sel_max;
      sel_min -= (sel_min-myUTC) % menu_item.ts;
      sel_max -= (sel_max-myUTC) % menu_item.ts;
      return [sel_min, sel_max];
    },


    //
    // MOUSE
    //

    // MOUSE: обработчик блокировать события мыши
    lib_on_mouse_null(e, slider) {
      let thumb = slider.$el.querySelectorAll('.v-slider__thumb-container');
      thumb[0].blur();
      thumb[1].blur();

      e.preventDefault();
      e.stopPropagation();
    },


    // MOUSE: обработчик mousedown
    lib_on_mouse_down(e, slider, fun_sel_move) {
      let el     = slider.$el;
      let parent = el.querySelector   ('.v-slider__track-container');
      let thumb  = el.querySelectorAll('.v-slider__thumb-container');
      thumb[0].blur();
      thumb[1].blur();

      let bounds = parent.getBoundingClientRect();
      let x = e.clientX - bounds.left; // let y = e.clientY - bounds.top;

      const size = 7;
      if (x < (thumb[0].offsetLeft - size)) { e.preventDefault(); e.stopPropagation(); fun_sel_move(0); return; } // левее   периода
      if (x > (thumb[1].offsetLeft + size)) { e.preventDefault(); e.stopPropagation(); fun_sel_move(1); return; } // правее  периода

      // e.preventDefault(); e.stopPropagation(); - нельзя блокировать
    },




    //
    // SEL
    //

    // SEL: переместить период 0 - влево, 1 - вправо
    lib_sel_move(pos, data) {
      let sel_min   = data.sel_min;
      let sel_max   = data.sel_max;
      let sel_delta = sel_max - sel_min;
      if (sel_delta==0) return;

      // влево
      if (pos==0) {
        if ((sel_min - sel_delta) < data.limit_min) {
          sel_min = data.limit_min;
          sel_max = data.limit_min+sel_delta;
        } else {
          sel_min -= sel_delta;
          sel_max -= sel_delta;
        }
      // вправо
      } else {
        if ((sel_max + sel_delta) > data.limit_max) {
          sel_min = data.limit_max-sel_delta;
          sel_max = data.limit_max;
        } else {
          sel_min += sel_delta;
          sel_max += sel_delta;
        }
      }

      return [sel_min, sel_max];
    },


  },
}
