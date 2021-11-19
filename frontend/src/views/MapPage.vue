<template>
  <split-panel shadow-effect>
    <template v-slot:firstPane>
      <v-row no-gutters class="graph-menu">
        <tools-menu></tools-menu>
        <component :is="changeComponent()" :style="stylesComponent"></component>
      </v-row>
    </template>
    <template v-slot:secondPane>
      <LeafletMain/>
    </template>
  </split-panel>
</template>

<script>
import SplitPanel from "../components/WebsiteShell/UI/splitPanel"
import LeafletMain from '../components/Map/Leaflet/LeafletMain'
import toolsMenu from "../components/WebsiteShell/UI/toolsMenu"
const MapScriptMenu = () => import("../components/Map/MapMenu/scriptsPage/mapScriptMenu")
const MapDossier = () => import("../components/Map/MapMenu/dossierPage/dossierPage")
import { mapGetters, mapActions } from "vuex"
import router from "@/router"

export default {
  name: 'Map',
  components: {SplitPanel, toolsMenu, LeafletMain, MapScriptMenu, MapDossier},
  computed: {
    ...mapGetters(['activeTool', 'SCRIPT_GET_ITEM_SEL']),
    stylesComponent: function () {
      return { 'width': `calc(100% - ${this.$CONST.APP.TOOL_MENU.WIDTH}px)`}
    },
    activeWindow: function () {
      return this.activeTool(router.currentRoute.name)
    }
  },

  mounted() {
    this.setDefaultValueActiveTool()
  },

  methods: {
    ...mapActions(['setDefaultValueActiveTool', 'setNavigationDrawerStatus', 'setActiveTool']),
    changeComponent() {
      if (this.activeWindow === 'scriptsPage')
        return 'MapScriptMenu'
      if (this.activeWindow === 'dossierPage')
        return 'MapDossier'
    }
  },
  watch: {
    SCRIPT_GET_ITEM_SEL: function (value) {
      if(JSON.parse(value).length) {
        this.setNavigationDrawerStatus(true)
        this.setActiveTool('dossierPage')
      }
    }
  }
}
</script>

<style scoped>
.graph-menu {
  flex-wrap: nowrap;
  height: 100%;
}
</style>
