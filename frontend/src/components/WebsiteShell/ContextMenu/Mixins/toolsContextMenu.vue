<template>

</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: "toolsContextMenu",
  data: () => ({
    contextMenu: {
      event: null,
      position: '',
    },
  }),
  computed: {
    ...mapGetters(['typeContextMenu', ]),
  },
  methods: {
    ...mapActions(['deactivateContextMenu', 'setTypeContextMenu', 'setCoordinatesContextMenu', 'activateContextMenu']),
  },
  watch: {
    contextMenu(value) {
      this.deactivateContextMenu()
      this.setTypeContextMenu(value.typeMenu)
      this.setCoordinatesContextMenu(value.event)
      this.$nextTick(() => {
        this.activateContextMenu()
      })
    },
  },
}
</script>

<style scoped>

</style>