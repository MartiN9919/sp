<template>
  <div>
    <l-control
      v-show="visible"
      position="bottomcenterhorizontal"
      class="leaflet-bar leaflet-control control_range select_off"
    >
      <table>
        <tr>
          <td>
            <div class="range-info">
              <div>{{val_dt_from}}</div><div>-</div><div>{{val_dt_to}}</div>
            </div>
          </td>
          <td>
            <v-range-slider
              ref="slider_dt"
              class="slider"
              v-model="prop_dt_sel"
              :min="MAP_GET_RANGE_DT_LIMIT_MIN"
              :max="MAP_GET_RANGE_DT_LIMIT_MAX"
              :step="step"

              dense

              thumb-size="8"
              thumb-color="green"

              track-fill-color="green"
              track-color="red"
            >
              <template v-slot:append>
                <v-icon
                  @click.stop="on_menu_dt_show"
                  size="24"
                >mdi-menu</v-icon>
              </template>
            </v-range-slider>
          </td>
        </tr>
        <tr>
          <td>
            <div class="range-info">
              <div>{{val_hm_from}}</div><div>-</div><div>{{val_hm_to}}</div>
            </div>
          </td>
          <td>
            <v-range-slider
              ref="slider_hm"
              class="slider"
              v-model="prop_dt_sel"
              :min="MAP_GET_RANGE_DT_LIMIT_MIN"
              :max="MAP_GET_RANGE_DT_LIMIT_MAX"
              :step="step"

              dense

              thumb-size="8"
              thumb-color="green"

              track-fill-color="green"
              track-color="red"
            >
              <template v-slot:append>
                <v-icon
                  @click.stop="on_menu_dt_show"
                  size="24"
                >mdi-menu</v-icon>
              </template>
            </v-range-slider>
          </td>
        </tr>
      </table>
    </l-control>
    <contextMenuNested
      ref="menu"
      :form="form"
      :items="menu_struct"
    />
  </div>
</template>


<script>
              // :hint="hint"
              // persistent-hint


// компонент недопустимо отключать v-if
// только скрывать v-show
// работает с данными на шине


import { mapGetters, mapActions } from 'vuex';
import { LControl } from "vue2-leaflet";
import { MAP_ITEM }  from '@/components/Map/Leaflet/Lib/Const';
import { myUTC, datesql_to_ts, ts_to_screen } from '@/plugins/sys';
import contextMenuNested from '@/components/WebsiteShell/ContextMenu/contextMenuNested';


const props = {
  options: {
    type: Object,
    default() { return {}; },
  },
};

export default {
  name: 'Range',
  props,
  components: {
    LControl,
    contextMenuNested,
  },

  data: () => ({
    label_dt: '',
    step: 0,
    menu_struct: undefined,
    menu_struct_base: [
      {
        title: 'период',
        icon:  'mdi-arrow-expand-horizontal', //'mdi-clock-start',
        menu:  [
          { title: 'все',      icon: 'mdi-calendar-check', action: 'on_period_dt', ts: 0, },
          //{ divider: true },
          { title: '30 суток', icon: 'mdi-calendar-month', action: 'on_period_dt', ts: 1000*2592000, },
          { title: '1 неделя', icon: 'mdi-calendar-range', action: 'on_period_dt', ts: 1000*604800, },
          { title: '1 сутки',  icon: 'mdi-calendar-today', action: 'on_period_dt', ts: 1000*86400, },
          { title: '1 час',    icon: 'mdi-clock-time-one', action: 'on_period_dt', ts: 1000*3600, },
        ],
      },
      {
        title: 'округлить до',
        icon:  'mdi-content-cut',
        menu: [
          { title: 'суток', icon: 'mdi-calendar-blank', action: 'on_round_dt', round: 'day', },
          { title: 'часов', icon: 'mdi-clock',          action: 'on_round_dt', round: 'hour', },
        ],
      },
    ],
  }),

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

  computed: {
    ...mapGetters([
      'MAP_GET_RANGE_SHOW',
      'MAP_GET_RANGE_DT_SEL',
      'MAP_GET_RANGE_DT_SEL_MIN',
      'MAP_GET_RANGE_DT_SEL_MAX',
      'MAP_GET_RANGE_DT_LIMIT_MIN',
      'MAP_GET_RANGE_DT_LIMIT_MAX',
    ]),

    form: vm => vm,

    prop_dt_sel: {
      set: function(lst) { this.MAP_ACT_RANGE_DT_SEL({lst: lst}); },
      get: function()    { return this.MAP_GET_RANGE_DT_SEL;   },
    },

    visible: function() {
      let ts_min = this.MAP_GET_RANGE_DT_LIMIT_MIN;
      let ts_max = this.MAP_GET_RANGE_DT_LIMIT_MAX;
      return (
        this.MAP_GET_RANGE_SHOW &&
        (ts_min > 0) &&
        (ts_max > 0) &&
        (ts_min != ts_max)
      );
    },
    val_dt_from() { return ts_to_screen(this.prop_dt_sel[0]) },
    val_dt_to()   { return ts_to_screen(this.prop_dt_sel[1]) },
    val_hm_from() { return ts_to_screen(this.prop_dt_sel[0]) },
    val_hm_to()   { return ts_to_screen(this.prop_dt_sel[1]) },
  },

  methods: {
    ...mapActions([
      'MAP_ACT_RANGE_DT_SEL',
    ]),

    // вызывается извне
    filter(fc) {
      if (this.MAP_GET_RANGE_SHOW) {
        let range_ts  = this.MAP_GET_RANGE_DT_SEL;
        if ((range_ts[0]>0) && (range_ts[1]>0)) {
          let item_date;
          let features = fc.features.filter(function(feature) {
            if (!feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.DATE]) return true;
            item_date = datesql_to_ts(feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.DATE]);
            return ((item_date >= range_ts[0]) && (item_date <= range_ts[1]));
          });
          fc.features = features;
        }
      }
      return fc;
    },


    // MENU: Показать первый уровень
    on_menu_dt_show(e) {
      const self    = this;
      let limit_min = this.MAP_GET_RANGE_DT_LIMIT_MIN;
      let limit_max = this.MAP_GET_RANGE_DT_LIMIT_MAX;
      let sel_min   = this.MAP_GET_RANGE_DT_SEL_MIN;
      let sel_max   = this.MAP_GET_RANGE_DT_SEL_MAX;
      let sel_delta = sel_max - sel_min;

      e.preventDefault();
      e.stopPropagation();
      this.menu_struct = JSON.parse(JSON.stringify(this.menu_struct_base)); // основа - глубокая копия
      // текущий выбор периода недоступен
      this.menu_struct[0].menu.forEach((item, ind) => {
        if (                                                                // доступность
          (self.step  == item.ts) &&                                        // шаг шкалы равен периоду и
          (sel_delta == ((item.ts==0)?(limit_max-limit_min):self.step))     // выбран только один шаг шкалы (для ВСЕ выбрано все)
        ) { self.menu_struct[0].menu[ind].disabled = true; }
        if (self.step  == item.ts) {                                        // текущий выбор: шаг шкалы равен периоду
          self.menu_struct[0].menu[ind].subtitle = 'Выбрано';
        }
      });
      this.$refs.menu.show_root(e.clientX, e.clientY);
    },

    // MENU: Установить период
    async on_period_dt(menu_item) {
      let limit_min = this.MAP_GET_RANGE_DT_LIMIT_MIN;
      let limit_max = this.MAP_GET_RANGE_DT_LIMIT_MAX;
      let sel_min   = this.MAP_GET_RANGE_DT_SEL_MIN;
      let sel_max   = this.MAP_GET_RANGE_DT_SEL_MAX;
      let sel_delta = menu_item.ts;

      if (sel_delta == 0) {                             // период: вся шкала
        sel_min = limit_min;
        sel_max = limit_max;
      } else if ((sel_max - sel_delta) >= limit_min) {  // период: влево от sel_max полностью
        sel_min = sel_max-sel_delta;

      } else {                                          // период: влево от sel_max частично
        sel_min = limit_min;
        sel_max = Math.min(sel_min+sel_delta, limit_max);
      }

      await this.set_range_dt_sel(sel_min, sel_max, sel_delta);
    },

    // MENU: Округлить период
    async on_round_dt(menu_item) {
      let limit_min = this.MAP_GET_RANGE_DT_LIMIT_MIN;
      let limit_max = this.MAP_GET_RANGE_DT_LIMIT_MAX;
      let sel_min   = this.MAP_GET_RANGE_DT_SEL_MIN;
      let sel_max   = this.MAP_GET_RANGE_DT_SEL_MAX;

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


    // MOUSE
    on_mousedown_slider_dt(e) {
      let el     = this.$refs.slider_dt.$el;
      let parent = el.querySelector('.v-slider__track-container');
      let thumb  = el.querySelectorAll('.v-slider__thumb-container');
      thumb[0].blur();
      thumb[1].blur();

      let bounds = parent.getBoundingClientRect();
      let x = e.clientX - bounds.left; // let y = e.clientY - bounds.top;

      const size = 7;
      if (x < (thumb[0].offsetLeft - size)) { e.preventDefault(); e.stopPropagation(); this.on_click_btn_dt(0); return; } // левее  периода
      if (x > (thumb[1].offsetLeft + size)) { e.preventDefault(); e.stopPropagation(); this.on_click_btn_dt(1); return; } // правее  периода

      // e.preventDefault(); e.stopPropagation(); - нельзя блокировать
    },
    on_mouse_reset_dt(e) {
      let thumb = this.$refs.slider_dt.$el.querySelectorAll('.v-slider__thumb-container');
      thumb[0].blur();
      thumb[1].blur();

      e.preventDefault();
      e.stopPropagation();
    },
    async on_click_btn_dt(pos) {
      let limit_min = this.MAP_GET_RANGE_DT_LIMIT_MIN;
      let limit_max = this.MAP_GET_RANGE_DT_LIMIT_MAX;
      let sel_min   = this.MAP_GET_RANGE_DT_SEL_MIN;
      let sel_max   = this.MAP_GET_RANGE_DT_SEL_MAX;
      let sel_delta = sel_max - sel_min;
      if (sel_delta==0) return;

      // влево
      if (pos==0) {
        if ((sel_min - sel_delta) < limit_min) {
          sel_min = limit_min;
          sel_max = limit_min+sel_delta;
        } else {
          sel_min -= sel_delta;
          sel_max -= sel_delta;
        }
      // вправо
      } else {
        if ((sel_max + sel_delta) > limit_max) {
          sel_min = limit_max-sel_delta;
          sel_max = limit_max;
        } else {
          sel_min += sel_delta;
          sel_max += sel_delta;
        }
      }

      await this.set_range_dt_sel(sel_min, sel_max);
    },

    async set_range_dt_sel(sel_min, sel_max, step=undefined) {
      let step_temp = (step != undefined) ? step : this.step;
      this.step = 0;
      await this.MAP_ACT_RANGE_DT_SEL({lst: [sel_min, sel_max]});
      this.step = step_temp;
    }
  },
}

</script>



<style scoped lang="scss">
  .control_range {
    border: 2px solid rgba(0,0,0,0.2);
    background-color: white;
    opacity: .7;
  }

  div::v-deep .slider { width: 22em; padding: 0 .7em 0 0; margin: 0; }
  div::v-deep .v-slider      { cursor: pointer; }
  div::v-deep .v-input__slot { margin: 0 !important; }
  div::v-deep .v-messages    { display: none; }
  div::v-deep .v-slider__track-container { height: 2px; }  /* высота полоски */

  /* информатор */
  div::v-deep .range-info {
    width: 240px;
    text-align: right;
    font-size: .8em;
    font-weight: bold;
    color: green;
  }
  div::v-deep .range-info > div { display: inline-block; }
  div::v-deep .range-info > div:nth-of-type(1) { width: 110px; text-align: right;  }
  div::v-deep .range-info > div:nth-of-type(2) { width: 15px;  text-align: center; }
  div::v-deep .range-info > div:nth-of-type(3) { width: 110px; text-align: left;   }
</style>
