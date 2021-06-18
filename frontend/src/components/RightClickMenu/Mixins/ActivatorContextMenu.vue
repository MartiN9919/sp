<template>

</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: "ActivatorContextMenu",
  computed: {
    ...mapGetters(['bodyRightClickMenu', ]),
    showContextMenu: function () {
      for (const [key, value] of Object.entries(this.contextMenus)) {
        if (this.bodyRightClickMenu === value) return true
      }
      return false
    }
  },
  methods: {
    ...mapActions(['activateRightClickMenu', ]),
    activateMenu (menu, e) {
      this.activateRightClickMenu({ event: e, body: menu})
    },
  },
}
</script>

<style scoped>

</style>