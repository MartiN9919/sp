<template>
  <v-menu
    v-model="status"
    v-bind="$attrs"
    ref="menu"
    :z-index="$attrs['z-index'] || 10001"
    transition="slide-x-reverse-transition"
  >
    <template v-slot:activator="{ on, attrs }">
      <slot name="activator" :on="on" :openMenu="openMenu" :closeMenu="closeMenu" :attrs="attrs"/>
    </template>
    <slot name="body" :openMenu="openMenu" :closeMenu="closeMenu" :status="status"/>
  </v-menu>
</template>

<script>
let menu = null

export default {
  name: "dropDownMenu",
  inheritAttrs: false,
  data: () => ({
    status: false,
  }),
  methods: {
    openMenu() {
      this.status = true
    },
    closeMenu() {
      this.status = false
    }
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