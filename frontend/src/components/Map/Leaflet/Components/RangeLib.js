
import { myUTC } from '@/plugins/sys';

export default {
    methods: {

    //
    // MENU
    //

    // MENU: Показать первый уровень
    lib_menu_show(e, data, menu) {
      let limit_delta  = data.limit_max - data.limit_min;
      let sel_delta    = data.sel_max   - data.sel_min;
      data.menu_struct = JSON.parse(JSON.stringify(data.menu_struct_base));

      // меню периодов
      data.menu_struct[0].menu.forEach((item, ind) => {
        // пометить:
        // предлагаемый период равен текущему шагу
        if (item.ts == data.sel_step) { data.menu_struct[0].menu[ind].subtitle = 'Шаг'; }
        // недоступно:
        // предлагаемый период меньше текущего шага и больше 0 или
        // предлагаемый период равен текущему периоду
        if (
          ((item.ts < data.sel_step) && (item.ts > 0)) ||
          (((item.ts==0)?limit_delta:item.ts) == sel_delta)
        ) { data.menu_struct[0].menu[ind].disabled = true; }
      });

      // меню шагов
      data.menu_struct[1].menu.forEach((item, ind) => {
        // недоступно:
        // предлагаемый шаг равен текущему шагу
        if (item.ts == data.sel_step) { data.menu_struct[1].menu[ind].disabled = true; }
      });

      // прервать обработку click-события и показать меню
      e.preventDefault();
      e.stopPropagation();
      menu.show_root(e.clientX, e.clientY);
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
      let sel_min   = data.sel_min;
      let sel_max   = data.sel_max;
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
