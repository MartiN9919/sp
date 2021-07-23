<template>
  <v-menu
    v-model="showMenu"
    :position-x="coordinatesContextMenu.x"
    :position-y="coordinatesContextMenu.y"
    offset-overflow right
    :close-on-content-click="false"
    max-height="50%" min-width="25em" max-width="25em" z-index="10001" transition="slide-x-reverse-transition"
  >
    <slot></slot>
  </v-menu>
</template>

<script>
import { mapActions, mapGetters } from "vuex"

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