<template>
  <l-control
    v-if="MAP_GET_NOTIFY"
    v-show="visible"
    position="topcenterhorizontal"
    class="leaflet-bar leaflet-control control_notify select-off"
  >
    <v-card
      v-for="(message_item, message_ind) in messages"
      :key="message_ind"
      class="item"
    >
      {{ message_item }}
    </v-card>
  </l-control>
</template>



<script>

import { mapGetters, } from 'vuex';
import { LControl, } from "vue2-leaflet";


export default {
  name: 'Notify',
  components: {
    LControl,
  },
  data: () => ({
    messages: [],
  }),

  computed: {
    ...mapGetters([
      'MAP_GET_NOTIFY',
    ]),

    visible() { return (this.messages.length > 0) },
  },

  methods: {
    notify_add(message) {
      if (message.length > 0) {
        this.messages.unshift(message)
        this.messages.splice(5)
      }
    },
    notify_set(message) {
      if (message.length > 0) { this.messages=[message] }
      else                    { this.messages=[] }
    },
    notify_del(message) {
      this.messages=[]
    },
  },

}

</script>



<style scoped lang="scss">
  .control_notify {
    border: 2px solid rgba(0,0,0,0.2);
    background-color: white;
    opacity: .7;
  }

  div::v-deep.control_notify .item {
    height: 30px !important;
    line-height: 30px !important;
    text-align: center;
    padding: 0 8px;
  }
</style>
