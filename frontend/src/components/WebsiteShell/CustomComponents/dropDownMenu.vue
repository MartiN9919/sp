<template>
  <v-menu
    v-model="status"
    v-bind="$attrs"
    ref="menu"
    :z-index="$attrs['z-index'] || 10001"
    transition="slide-x-reverse-transition"
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
    this.closeMenu = this.$refs.menu.save
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