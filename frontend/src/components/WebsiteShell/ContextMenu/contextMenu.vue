<template>
  <v-menu
    v-model="showMenu" :close-on-content-click="false"
    max-height="50%" min-width="25em" max-width="25em"
    absolute offset-x offset-y z-index="10001"
    transition="slide-x-reverse-transition"
    :position-x="coordinatesContextMenu.x"
    :position-y="coordinatesContextMenu.y"
  ><slot></slot></v-menu>
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