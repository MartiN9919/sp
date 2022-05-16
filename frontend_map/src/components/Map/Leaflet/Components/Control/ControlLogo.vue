<template>
  <l-control
    v-if="MAP_GET_LOGO"
    class="map-logo select-off"
    :position="'bottomleft'"
  >
    <v-icon medium>mdi-diamond-stone</v-icon>САПФИР
  </l-control>
</template>



<script>

import {
  mapGetters,
} from 'vuex';

import {
  LControl,
} from "vue2-leaflet";

export default {
  name: 'ControlLogo',

  components: {
    LControl,
  },

  computed: {
    ...mapGetters([
      'MAP_GET_LOGO',
    ]),
  },

}
</script>



<style scoped lang="scss">

  .map-logo {
    font-size: 1.6em;
    font-weight: bolder;
    color: #aaa;
    opacity: 0.8;
    text-shadow: #555;
  }

</style>
