<template>
  <v-menu
    :close-on-content-click="false"
    max-height="50%" min-width="20%" max-width="20%"
    offset-x offset-y z-index="10001"
    transition="slide-x-reverse-transition"
    v-model="showMenu"
    :position-x="coordinatesContextMenu.x"
    :position-y="coordinatesContextMenu.y"
    absolute
  >
    <slot></slot>
  </v-menu>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "rightClickMenu",
  computed: {
    ...mapGetters(['isStateContextMenu', 'coordinatesContextMenu', ]),
    showMenu: {
      get: function () { return this.isStateContextMenu },
      set: function (value) { this.deactivateContextMenu() }
    }
  },
  methods: {
    ...mapActions(['deactivateContextMenu', ]),
  },
  destroyed() {
    this.deactivateContextMenu()
  }
}
</script>

<style scoped>

</style>