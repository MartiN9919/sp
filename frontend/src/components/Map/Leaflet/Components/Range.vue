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
            <v-range-slider
              ref="slider"
              class="slider"
              v-model="prop_sel"
              :min="MAP_GET_RANGE_MIN"
              :max="MAP_GET_RANGE_MAX"

              height="1.5em"
              dense

              thumb-size="8"
              thumb-color="green"

              track-fill-color="green"
              track-color="red"

              :hint="hint"
              persistent-hint
            >
              <template v-slot:append>
                <v-icon
                  @click.stop="on_menu_show"
                  size="20"
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
    menu_struct: undefined,
    menu_struct_base: [
      {
        title: 'установить период',
        icon:  'mdi-arrow-expand-horizontal', //'mdi-clock-start',
        menu:  [
          { title: 'все',      icon: 'mdi-calendar-check', action: 'on_period_dt', ts: 0, },
          { divider: true },
          { title: '30 суток', icon: 'mdi-calendar-month', action: 'on_period_dt', ts: 2592000, },
          { title: '1 неделя', icon: 'mdi-calendar-range', action: 'on_period_dt', ts: 604800, },
          { title: '1 сутки',  icon: 'mdi-calendar-today', action: 'on_period_dt', ts: 86400, },
          { title: '1 час',    icon: 'mdi-clock-time-one', action: 'on_period_dt', ts: 3600, },
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
    let el = this.$refs.slider.$el.querySelector('.v-slider');
    el.addEventListener('click',      this.on_mouse_reset,      {capture: true});
    el.addEventListener('mouseup',    this.on_mouse_reset,      {capture: true});
    el.addEventListener('mouseleave', this.on_mouse_reset,      {capture: true});
    el.addEventListener('mousedown',  this.on_mousedown_slider, {capture: true});
  },
  beforeDestroy() {
    let el = this.$refs.slider.$el.querySelector('.v-slider');
    el.removeEventListener('click',      this.on_mouse_reset);
    el.removeEventListener('mouseup',    this.on_mouse_reset);
    el.removeEventListener('mouseleave', this.on_mouse_reset);
    el.removeEventListener('mousedown',  this.on_mousedown_slider);
  },

  computed: {
    ...mapGetters([
      'MAP_GET_RANGE_SHOW',
      'MAP_GET_RANGE_SEL',
      'MAP_GET_RANGE_MIN',
      'MAP_GET_RANGE_MAX',
    ]),

    form: vm => vm,

    prop_sel: {
      set: function(lst) { this.MAP_ACT_RANGE_SEL({lst: lst}); },
      get: function()    { return this.MAP_GET_RANGE_SEL;      },
    },

    visible: function() {
      let ts_min = this.MAP_GET_RANGE_MIN;
      let ts_max = this.MAP_GET_RANGE_MAX;
      return (
        this.MAP_GET_RANGE_SHOW &&
        (ts_min > 0) &&
        (ts_max > 0) &&
        (ts_min != ts_max)
      );
    },
    hint() {
      let t_min = ts_to_screen(this.prop_sel[0]);
      let t_max = ts_to_screen(this.prop_sel[1]);
      return t_min+" - "+t_max;
    },
  },

  methods: {
    ...mapActions([
      'MAP_ACT_RANGE_SEL',
    ]),

    // вызывается извне
    filter(fc) {
      if (this.MAP_GET_RANGE_SHOW) {
        let range_ts  = this.MAP_GET_RANGE_SEL;
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
    on_menu_show(e) {
      e.preventDefault();
      e.stopPropagation();
      this.menu_struct = JSON.parse(JSON.stringify(this.menu_struct_base)); // основа - глубокая копия
      //this.menu_struct.splice(4, 1);
      this.$refs.menu.show_root(e.clientX, e.clientY);
    },

    // MENU: Установить период
    on_period_dt(menu_item) {
      let limit_min = this.MAP_GET_RANGE_MIN;
      let limit_max = this.MAP_GET_RANGE_MAX;
      let sel       = this.MAP_GET_RANGE_SEL;
      let sel_min   = sel[0];
      let sel_max   = sel[1];
      let sel_delta = menu_item.ts*1000;


      if (sel_delta == 0) {
        sel_min = limit_min;
        sel_max = limit_max;
      } else if ((sel_max - sel_delta) >= limit_min) {
        sel_min = sel_max-sel_delta;              // период влево от sel_max полностью

      } else {                                    // период влево от sel_max частично
        sel_min = limit_min;
        sel_max = Math.min(sel_min+sel_delta, limit_max);
      }

      this.MAP_ACT_RANGE_SEL({lst: [sel_min, sel_max]});
    },

    // MENU: Округлить период
    on_round_dt(menu_item) {
      let limit_min = this.MAP_GET_RANGE_MIN;
      let limit_max = this.MAP_GET_RANGE_MAX;
      let sel       = this.MAP_GET_RANGE_SEL;
      let sel_min   = sel[0];
      let sel_max   = sel[1];

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

      this.MAP_ACT_RANGE_SEL({lst: [sel_min, sel_max]});
  },


    // MOUSE
    on_mousedown_slider(e) {
      let el     = this.$refs.slider.$el;
      let parent = el.querySelector('.v-slider__track-container');
      let thumb  = el.querySelectorAll('.v-slider__thumb-container');
      thumb[0].blur();
      thumb[1].blur();

      let bounds = parent.getBoundingClientRect();
      let x = e.clientX - bounds.left; // let y = e.clientY - bounds.top;

      const size = 7;
      if (x < (thumb[0].offsetLeft - size)) { e.preventDefault(); e.stopPropagation(); this.on_click_btn(0); return; } // левее  периода
      if (x > (thumb[1].offsetLeft + size)) { e.preventDefault(); e.stopPropagation(); this.on_click_btn(1); return; } // правее  периода

      //e.preventDefault(); e.stopPropagation();
    },
    on_mouse_reset(e) {
      let thumb = this.$refs.slider.$el.querySelectorAll('.v-slider__thumb-container');
      thumb[0].blur();
      thumb[1].blur();

      e.preventDefault();
      e.stopPropagation();
    },
    on_click_btn(pos) {
      let limit_min = this.MAP_GET_RANGE_MIN;
      let limit_max = this.MAP_GET_RANGE_MAX;
      let sel       = this.MAP_GET_RANGE_SEL;
      let sel_min   = sel[0];
      let sel_max   = sel[1];
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

      this.MAP_ACT_RANGE_SEL({lst: [sel_min, sel_max]});
    },
  },
}

</script>



<style scoped lang="scss">
  .control_range {
    border: 2px solid rgba(0,0,0,0.2);
    background-color: white;
    opacity: .7;
  }

  div::v-deep .btn {
    height: 3em!important;
    min-width: 1.5em!important;
    max-width: 1.5em!important;
    padding: 0;
    margin: 0;
    font-weight: bold;
  }

  div::v-deep .slider {
    min-width: 25em;
    height: 2.4em;
    padding: 0;
    margin: 0 0 .4em 0;
  }


  div::v-deep .v-slider {
    cursor: pointer;
  }

  /* высота полоски */
  div::v-deep .v-slider__track-container {
    height: 2px;
  }

  /* формат подсказки */
  div::v-deep .v-messages {
    text-align: center;
  }
  div::v-deep .v-messages__message {
    text-align: center;
    font-weight: bold;
    color: green;
  }

</style>
