<template>
  <modal v-if="showModal" @close="showModal = false">
    <h3 slot="header">custom header</h3>
  </modal>
</template>



<script>

import {
  mapGetters,
} from 'vuex';

import {
  LControl,
} from "vue2-leaflet";

export default {
  name: 'Leaflet.Editor',

  components: {

  },

  data() {
    return {
      showModal: true,
    }
  },

  computed: {
    ...mapGetters([
      'MAP_GET_LOGO',
    ]),
  },

}
</script>



<style scoped lang="scss">

</style>
