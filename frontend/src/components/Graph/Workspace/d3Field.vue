<template>
  <v-container fluid class="pa-0">
    <svg class="svg-demo" @contextmenu="contextMenu = { event: $event, typeMenu: 'workSpace' }">
      <circle
        r="60" cy="97" cx="497" stroke-width="2" stroke="#E4AF4C" fill="#F4D37D"
        @contextmenu.stop="contextMenu = { event: $event, typeMenu: 'circle' }"/>
    </svg>
    <context-menu v-if="['workSpace', 'circle'].includes(typeContextMenu)">
      <graph-work-space_cm @selectObject="confirmFillingSelectors" v-if="typeContextMenu === 'workSpace'"/>
      <v-card v-if="typeContextMenu === 'circle'">
        <v-card-title class="justify-center pa-0">
          Пустое меню
        </v-card-title>
      </v-card>
    </context-menu>
  </v-container>
</template>

<script>
import { mapActions } from "vuex";
import contextMenu from "../../ContextMenu/contextMenu";
import graphWorkSpace_cm from "../../ContextMenu/BodysContextMenu/graphWorkSpace_cm";
import toolsContextMenu from "../../ContextMenu/Mixins/toolsContextMenu";

export default {
  name: "d3Field",
  components: { contextMenu, graphWorkSpace_cm, },
  mixins: [ toolsContextMenu, ],
  props: { drawer: Boolean, },
  methods: {
    ...mapActions(['addListObjects', 'activateObject', 'changeNavigationDrawerStatus',]),
    confirmFillingSelectors(object) {
      this.activateObject({params: {object_id: object.id}})
        .then(() => { if (!this.drawer) this.changeNavigationDrawerStatus() })
      this.deactivateContextMenu()
    },
  },

}
</script>

<style scoped>
.svg-demo {
  background-color: #ffffff;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1600 900'%3E%3Cdefs%3E%3ClinearGradient id='a' x1='0' x2='0' y1='1' y2='0'%3E%3Cstop offset='0' stop-color='%230FF'/%3E%3Cstop offset='1' stop-color='%23CF6'/%3E%3C/linearGradient%3E%3ClinearGradient id='b' x1='0' x2='0' y1='0' y2='1'%3E%3Cstop offset='0' stop-color='%23F00'/%3E%3Cstop offset='1' stop-color='%23FC0'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cg fill='%23FFF' fill-opacity='0' stroke-miterlimit='10'%3E%3Cg stroke='url(%23a)' stroke-width='2'%3E%3Cpath transform='translate(0 0)' d='M1409 581 1450.35 511 1490 581z'/%3E%3Ccircle stroke-width='4' transform='rotate(0 800 450)' cx='500' cy='100' r='40'/%3E%3Cpath transform='translate(0 0)' d='M400.86 735.5h-83.73c0-23.12 18.74-41.87 41.87-41.87S400.86 712.38 400.86 735.5z'/%3E%3C/g%3E%3Cg stroke='url(%23b)' stroke-width='4'%3E%3Cpath transform='translate(0 0)' d='M149.8 345.2 118.4 389.8 149.8 434.4 181.2 389.8z'/%3E%3Crect stroke-width='8' transform='rotate(0 1089 759)' x='1039' y='709' width='100' height='100'/%3E%3Cpath transform='rotate(0 1400 132)' d='M1426.8 132.4 1405.7 168.8 1363.7 168.8 1342.7 132.4 1363.7 96 1405.7 96z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  background-attachment: fixed;
  background-size: cover;
  height: 100%;
  width: 100%;
}
</style>