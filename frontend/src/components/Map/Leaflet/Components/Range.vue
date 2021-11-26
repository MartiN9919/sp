<template>
  <div>
    <l-control
      v-show="visible"
      position="bottomcenterhorizontal"
      class="leaflet-bar leaflet-control control_range select_off"
    >
      <table @contextmenu.stop="dt_menu_show">
        <tr>
          <td class="layer-parent">

            <!-- МАРКЕРЫ -->
            <canvas
              ref="mark_dt"
              class="layer-child"
              :style="{top: mark.top+'px', left: mark.left+'px', width: mark.width+'px', height: mark.height+'px'}"
              :width="mark.width"
              :height="mark.height"
            />

            <!-- ИНФОРМАТОР -->
            <p
              ref="inf_dt"
              class="layer-child inf zz"
              :style="{top: inf.top+'px', left: inf.left+'px', width: inf.width+'px', height: inf.height+'px'}"
              :width="inf.width"
              :height="inf.height"
            >{{dt_val_min}} - {{dt_val_max}}</p>

            <!-- СТАТИСТИКА -->
            <p
              ref="stat_dt"
              class="layer-child stat"
              :style="{top: stat.top+'px', left: stat.left+'px', width: stat.width+'px', height: stat.height+'px'}"
              :width="stat.width"
              :height="stat.height"
            >{{stat.label_dt}}</p>

            <!-- СЛАЙДЕР -->
            <v-range-slider
              ref="slider_dt"
              class="slider"
              v-model="dt_prop_sel"
              :min="dt.limit_min"
              :max="dt.limit_max"
              :step="dt.sel_step"

              dense

              thumb-size="8"
              :thumb-color="color_sel"

              :track-fill-color="color_sel"
              track-color="red"

              @contextmenu.stop="dt_menu_show"
            >
              <template v-slot:append>
                <v-icon
                  @click.stop="dt_menu_show"
                  size="24"
                >mdi-menu</v-icon>
              </template>
            </v-range-slider>
          </td>
        </tr>
        <tr class="divider"/>
        <tr>
          <td class="layer-parent">

            <!-- МАРКЕРЫ -->
            <canvas
              ref="mark_hm"
              class="layer-child"
              :style="{top: mark.top+'px', left: mark.left+'px', width: mark.width+'px', height: mark.height+'px'}"
              :width="mark.width"
              :height="mark.height"
            />

            <!-- ИНФОРМАТОР -->
            <p
              ref="inf_hm"
              class="layer-child inf"
              :style="{top: inf.top+'px', left: inf.left+'px', width: inf.width+'px', height: inf.height+'px'}"
              :width="inf.width"
              :height="inf.height"
            >{{hm_val_min}} - {{hm_val_max}}</p>

            <!-- СТАТИСТИКА -->
            <p
              ref="stat_dt"
              class="layer-child stat zz"
              :style="{top: stat.top+'px', left: stat.left+'px', width: stat.width+'px', height: stat.height+'px'}"
              :width="stat.width"
              :height="stat.height"
            >{{stat.label_hm}}</p>

            <!-- СЛАЙДЕР -->
            <v-range-slider
              ref="slider_hm"
              class="slider"
              v-model="hm_prop_sel"
              :min="hm.limit_min"
              :max="hm.limit_max"
              :step="hm.sel_step"

              dense

              thumb-size="8"
              :thumb-color="color_sel"

              :track-fill-color="color_sel"
              track-color="red"
            >
              <template v-slot:append>
                <v-icon
                  @click.stop="hm_menu_show"
                  size="24"
                >mdi-menu</v-icon>
              </template>
            </v-range-slider>
          </td>
        </tr>
      </table>
    </l-control>
    <contextMenuNested
      ref="dt_menu"
      :form="form"
      :items="dt.menu_struct"
    />
    <contextMenuNested
      ref="hm_menu"
      :form="form"
      :items="hm.menu_struct"
    />
  </div>
</template>


<script>
// компонент недопустимо отключать v-if
// только скрывать v-show
// работает с данными на шине
// hm всегда устанавливает диапазон 0...75600 (количество секунд в сутках)

import { mapGetters, mapActions } from 'vuex';
import { LControl }      from 'vue2-leaflet';
import { MAP_ITEM }      from '@/components/Map/Leaflet/Lib/Const';
import { datesql_to_ts, datesql_is_time } from '@/plugins/sys';
import contextMenuNested from '@/components/WebsiteShell/UIMainComponents/contextMenuNested';
import MixLib            from '@/components/Map/Leaflet/Components/RangeLib';
import MixDt             from '@/components/Map/Leaflet/Components/RangeDt';
import MixHm             from '@/components/Map/Leaflet/Components/RangeHm';

export default {
  name: 'Range',
  mixins: [ MixLib, MixDt, MixHm, ],
  components: { LControl, contextMenuNested, },
  data: () => ({
    color_sel:         'green',

    mark: {                     // маркеры на canvas
      margin_x:        3,       // вычисляемые отступы слева и справа
      top:             3,
      left:            16,
      width:           541,     // реальная ширина, width-margin_x-margin_x = логическая ширина
      height:          15,

      strokeStyle:     "#aaa",  // маркер: цвет
      lineWidth:       2,       // маркер: ширина
      lineHeightStart: 1,       // маркер: Y1
      lineHeightEnd:   8,       // маркер: Y2
      shadowColor:     "#999",  // тень: цвет
      shadowBlur:      4,       // тень: размытие
    },

    inf: {                      // информатор
      //info_dt:        '55 из 100 (100%)',
      //info_hm:        '12 из 1000 (100%)',
      top:             30,
      left:            18,
      width:           536,     // реальная ширина, 307-7-7=293 - логическая ширина
      height:          15,
    },

    stat: {                     // статистика
      label_dt:        '55 из 100 (100%)',
      label_hm:        '12 из 1000 (100%)',
      top:             30,
      left:            18,
      width:           536,     // реальная ширина, 307-7-7=293 - логическая ширина
      height:          15,

      count_all:       0,
      count_sel_all:   0,
      count_sel_dt:    0,
      count_sel_hm:    0,
      percent_sel_all: 0,
      percent_sel_dt:  0,
      percent_sel_hm:  0,
    },
  }),

  mounted: function() {
  },

  watch: {
    SCRIPT_GET: {
      deep: true,
      immediate: true,
      handler: function(items) {
        this.dt_items_change(items);
        this.hm_items_change(items);
      },
    }
  },

  computed: {
    ...mapGetters([
      'SCRIPT_GET',
      'MAP_GET_RANGE',
    ]),

    form: vm => vm,

    visible: function() {
      return (
        this.MAP_GET_RANGE &&
        (this.dt.limit_min > 0) &&
        (this.dt.limit_max > 0) &&
        (this.dt.limit_min != this.dt.limit_max)
      );
    },
  },

  methods: {
    ...mapActions([ 'MAP_ACT_REFRESH', ]),

    // отфильтровать fc, вызывается извне
    filter(fc) {
      if (this.MAP_GET_RANGE) {
        if ((this.dt.sel_min>0) && (this.dt.sel_max>0)) {
          let self = this;
          let features  = fc.features.filter(function(feature) {
            let fc_date = feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.DATE];
            if (!fc_date) return true;
            let item_date = datesql_to_ts(fc_date);
            let is_time   = datesql_is_time(fc_date);                        // если время не указано, его не учитываем
            let item_time = (is_time) ? self.hm_ts_cut_sec(item_date) : 0;   // в секундах

            return (
              (item_date >= self.dt.sel_min) &&
              (item_date <= self.dt.sel_max) &&
              (
                (is_time == false) ||
                (
                  (is_time == true) &&
                  (item_time >= self.hm.sel_min) &&
                  (item_time <= self.hm.sel_max)
                )
              )
            );
          });
          fc.features = features;
        }
      }
      return fc;
    },


    set_hint() {
      let self = this;
      this.stat.count_all       = 0;
      this.stat.count_sel_all   = 0;
      this.stat.count_sel_dt    = 0;
      this.stat.count_sel_hm    = 0;
      this.stat.percent_sel_all = 0;
      this.stat.percent_sel_dt  = 0;
      this.stat.percent_sel_hm  = 0;

      this.SCRIPT_GET.forEach(function(item){
        item.fc.features.forEach(function(feature){
          self.stat.count_all++;
          let date = feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.DATE];
          if (!date) return;
          date = datesql_to_ts(date);
          if ((date >= self.dt.sel_min) && (date <= self.dt.sel_max)) { self.stat.count_sel_dt++; }
       });
      });
      //console.log(self.stat.count_all, self.stat.count_sel_dt)
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

  /* наложение друг на друга */
  div::v-deep .layer-parent  { position: relative; }
  div::v-deep .layer-child   { position: absolute; }

  /* слайдер */
  div::v-deep .slider        { width: 600px; padding: 0 5px 5px 10px; margin: 5px 0; }
  div::v-deep .v-slider      { cursor: pointer; }
  div::v-deep .v-input__slot { margin: 0 !important; }
  div::v-deep .v-messages    { display: none; }
  div::v-deep .v-slider__track-container                  { height: 1px; }        /* высота полоски */
  div::v-deep .v-slider__track-container>div:nth-child(2) { height: 2px; }
  div::v-deep .divider       { height: 1px; }                                     /* разделитель между слайдерами */

  /* информатор */
  div::v-deep .inf           { text-align: center; font-size: 0.7em; font-weight: bold; color: #444; } /* класс info нельзя, т.к. уже есть */

  /* статистика */
  div::v-deep .stat          { text-align: right; font-size: 0.7em; color: #444; }
</style>
