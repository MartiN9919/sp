<template>
  <l-control
    v-if="MAP_GET_RANGE_SHOW"
    v-show="visible"
    position="bottomcenterhorizontal"
    class="leaflet-bar leaflet-control control_range select_off"
  >
    <table>
      <tr>
        <td>
          <v-btn
            class="btn"
            depressed
            plain
            @click="btn_click(0)"
          ><</v-btn>
        </td>

        <td>
          <v-range-slider
            class="slider"
            v-model="prop_sel"
            :min="MAP_GET_RANGE_MIN"
            :max="MAP_GET_RANGE_MAX"

            height="1.5em"
            dense

            thumb-color="green"
            track-fill-color="green"
            track-color="red"

            :hint="hint"
            persistent-hint
          />
        </td>

        <td>
          <v-btn
            class="btn"
            depressed
            plain
            @click="btn_click(1)"
          >></v-btn>
        </td>
      </tr>
    </table>

  </l-control>
</template>



<script>

import {
  mapGetters,
  mapActions,
} from 'vuex';

import {
  LControl,
} from "vue2-leaflet";

import {
  ts_to_screen,
} from '@/plugins/sys';



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
  },

  mounted() {

  },

  computed: {
    ...mapGetters([
      'MAP_GET_RANGE_SHOW',
      'MAP_GET_RANGE_SEL',
      'MAP_GET_RANGE_MIN',
      'MAP_GET_RANGE_MAX',
    ]),

    prop_sel: {
      set: function(lst) { this.MAP_ACT_RANGE_SEL({lst: lst}); },
      get: function()    { return this.MAP_GET_RANGE_SEL;      },
    },

    visible: function() {
      let ts_min = this.MAP_GET_RANGE_MIN;
      let ts_max = this.MAP_GET_RANGE_MAX;
      return (
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

    btn_disabled(pos) {

    },

    btn_click(pos) {
      let limit_min = this.MAP_GET_RANGE_MIN;
      let limit_max = this.MAP_GET_RANGE_MAX;
      let sel       = this.MAP_GET_RANGE_SEL;
      let sel_min   = sel[0];
      let sel_max   = sel[1];
      let sel_delta = sel_max - sel_min;
      if (sel_delta==0) return;

      if (pos==0) {
        if ((sel_min - sel_delta) < limit_min) return;
        sel_min -= sel_delta;
        sel_max -= sel_delta;
      } else {
        if ((sel_max + sel_delta) > limit_max) return;
        sel_min += sel_delta;
        sel_max += sel_delta;
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

  div::v-deep .v-messages {
    text-align: center;
  }

  div::v-deep .v-messages__message {
    text-align: center;
    font-weight: bold;
    color: green;
  }
</style>
