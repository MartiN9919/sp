<template>
  <l-control
    position="topcenterhorizontal"
    class="control_range select_off"
  >
    <v-card>
      66661 sdf gsd fgsd fg sd fg sdf g sd fg sdf g sdf g sdf g sdf g sdf g sdf g sdf g sdf gs d
      {{ messages }}
    </v-card>
  </l-control>
</template>



<script>

import { LControl, } from "vue2-leaflet";


export default {
  name: 'Notify',
  components: {
    LControl,
  },
  data: () => ({
    messages: [],
  }),

  mounted() {

  },

  computed: {

    // prop_sel: {
    //   set: function(lst) { this.MAP_ACT_RANGE_SEL({lst: lst}); },
    //   get: function()    { return this.MAP_GET_RANGE_SEL;      },
    // },

    visible: function() {},
    hint() { },
  },

  methods: {
    notify_add(message) {
      this.messages.push(message)
    },
    notify_set(message) {
      this.messages=[message]
    },
  },

}

</script>



<style lang="scss">
  .control_range {
    border: 2px solid rgba(0,0,0,0.2);
    background-color: white;
    opacity: .7;
  }

  .control_range .btn {
    height: 3em!important;
    min-width: 1.5em!important;
    max-width: 1.5em!important;
    padding: 0;
    margin: 0;
    font-weight: bold;
  }

  .control_range .slider {
    min-width: 16em;
    height: 2.4em;
    padding: 0;
    margin: 0 0 .4em 0;
  }

  .control_range .v-messages {
    text-align: center;
  }
</style>
