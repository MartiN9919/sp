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
            @click="on_click_btn(0)"
          >
            <v-icon size="25">mdi-arrow-left-circle</v-icon>
          </v-btn>
        </td>

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
          />
        </td>

        <td>
          <v-btn
            class="btn"
            depressed
            plain
            @click="on_click_btn(1)"
          >
            <v-icon size="25">mdi-arrow-right-circle</v-icon>
          </v-btn>
        </td>
      </tr>
    </table>

  </l-control>
</template>



<script>
//             @click.capture="on_mousedown_slider"
//             @mousedown.capture="on_mousedown_slider"


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
    let el = this.$refs.slider.$el.querySelector('.v-slider');
    el.addEventListener('click',     this.on_mouse_reset,      {capture: true});
    el.addEventListener('mouseup',   this.on_mouse_reset,      {capture: true});
    el.addEventListener('mousedown', this.on_mousedown_slider, {capture: true});
  },

  beforeDestroy() {
    let el = this.$refs.slider.$el.querySelector('.v-slider');
    el.removeEventListener('click',     this.on_mouse_reset);
    el.removeEventListener('mouseup',   this.on_mouse_reset);
    el.removeEventListener('mousedown', this.on_mousedown_slider);
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



    on_mousedown_slider(e) {
      let el     = this.$refs.slider.$el;
      let parent = el.querySelector('.v-slider__track-container');
      let thumb  = el.querySelectorAll('.v-slider__thumb-container');
      thumb[0].blur();
      thumb[1].blur();

      let bounds = parent.getBoundingClientRect();
      let x = e.clientX - bounds.left; // let y = e.clientY - bounds.top;

      const size = 7;
      if (x < (thumb[0].offsetLeft - size)) { e.preventDefault(); e.stopPropagation(); this.on_click_btn(0); return; }
      if (x > (thumb[1].offsetLeft + size)) { e.preventDefault(); e.stopPropagation(); this.on_click_btn(1); return; }

      //e.preventDefault(); e.stopPropagation();
    },
    on_mouse_reset(e) {
      let thumb = this.$refs.slider.$el.querySelectorAll('.v-slider__thumb-container');
      thumb[0].blur();
      thumb[1].blur();

      e.preventDefault();
      e.stopPropagation();
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
