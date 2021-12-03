<template>
  <split-panel shadow-effect>
    <template v-slot:firstPane>
      <tools-menu>
        <component :is="changeComponent()"/>
      </tools-menu>
    </template>
    <template v-slot:secondPane>
      <LeafletMain/>
    </template>
  </split-panel>
</template>

<script>
import SplitPanel from "@/components/WebsiteShell/CustomComponents/splitPanel"
import LeafletMain from '@/components/Map/Leaflet/LeafletMain'
import toolsMenu from "@/components/WebsiteShell/CustomComponents/toolsMenu"
const MapScriptMenu = () => import("@/components/Map/MapMenu/scriptsPage/mapScriptMenu")
const MapDossier = () => import("@/components/Map/MapMenu/dossierPage/dossierPage")
import { mapGetters, mapActions } from "vuex"
import router from "@/router"

export default {
  name: 'Map',
  components: {SplitPanel, toolsMenu, LeafletMain, MapScriptMenu, MapDossier},
  computed: mapGetters(['activeTool', 'SCRIPT_GET_ITEM_SEL']),
  methods: {
    ...mapActions(['setNavigationDrawerStatus', 'setActiveTool']),
    changeComponent() {
      switch (this.activeTool(router.currentRoute.name)) {
        case 'scriptsPage':
          return 'MapScriptMenu'
        case 'dossierPage':
          return 'MapDossier'
        default:
          return 'MapScriptMenu'
      }
    }
  },
  watch: {
    SCRIPT_GET_ITEM_SEL: function (value) {
      if(JSON.parse(value).length) {
        this.setNavigationDrawerStatus(true)
        this.setActiveTool('dossierPage')
      }
    }
  },
}
</script>
