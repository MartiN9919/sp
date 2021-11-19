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
              <div>{{dt_val_min}}</div><div>-</div><div>{{dt_val_max}}</div>
            </div>
          </td>
          <td>
            <v-range-slider
              ref="slider_dt"
              class="slider"
              v-model="dt_prop_sel"
              :min="dt.limit_min"
              :max="dt.limit_max"
              :step="dt.sel_step"

              dense

              thumb-size="8"
              thumb-color="green"

              track-fill-color="green"
              track-color="red"
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
        <tr>
          <td>
            <div class="range-info">
              <div>{{hm_val_min}}</div><div>-</div><div>{{hm_val_max}}</div>
            </div>
          </td>
          <td>
            <v-range-slider
              ref="slider_hm"
              class="slider"
              v-model="dt_prop_sel"
              :min="dt.limit_min"
              :max="dt.limit_max"
              :step="dt.sel_step"

              dense

              thumb-size="8"
              thumb-color="green"

              track-fill-color="green"
              track-color="red"
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
      </table>
    </l-control>
    <contextMenuNested
      ref="menu"
      :form="form"
      :items="dt.menu_struct"
    />
  </div>
</template>


<script>
// компонент недопустимо отключать v-if
// только скрывать v-show
// работает с данными на шине

import { mapGetters, mapActions } from 'vuex';
import { LControl }      from 'vue2-leaflet';
import { MAP_ITEM }      from '@/components/Map/Leaflet/Lib/Const';
import { datesql_to_ts } from '@/plugins/sys';
import contextMenuNested from '@/components/WebsiteShell/ContextMenu/contextMenuNested';
import MixDt             from '@/components/Map/Leaflet/Components/RangeDt';
import MixHm             from '@/components/Map/Leaflet/Components/RangeHm';

export default {
  name: 'Range',
  mixins: [ MixDt, MixHm, ],
  components: { LControl, contextMenuNested, },
  watch: {
    SCRIPT_GET: {
      deep: true,
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
          let item_date;
          let self = this;
          let features = fc.features.filter(function(feature) {
            if (!feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.DATE]) return true;
            item_date = datesql_to_ts(feature.properties[MAP_ITEM.FC.FEATURES.PROPERTIES.DATE]);
            return ((item_date >= self.dt.sel_min) && (item_date <= self.dt.sel_max));
          });
          fc.features = features;
        }
      }
      return fc;
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
