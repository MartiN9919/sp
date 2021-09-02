<template>
  <v-menu
    v-model="status"
    v-bind="$attrs"
    ref="menuBoolean"
    transition="slide-x-reverse-transition"
    offset-x
    offset-y
    bottom
    fixed
    z-index="10001"
  >
    <template v-slot:activator="{ on, attrs }">
      <slot name="activator" :on="on"></slot>
    </template>
    <slot name="body" :closeMenu="closeMenu" :status="status"></slot>
  </v-menu>
</template>

<script>
let menu = null

export default {
  name: "dropDownMenu",
  inheritAttrs: false,
  data: () => ({
    closeMenu: null,
    status: false,
  }),
  mounted() {
    this.closeMenu = this.$refs.menuBoolean.save
  },
  watch: {
    menuModal: function (value) {
      if (value) {
        if (menu && menu !== this)
          menu.menuModal = false
        menu = this
      }
    }
  }
}
</script>

<style scoped>

</style>