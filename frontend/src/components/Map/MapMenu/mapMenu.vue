<template>
  <v-row no-gutters style="flex-wrap: nowrap; height: 100%">
    <v-col style="max-width: 56px">
      <tools-menu></tools-menu>
    </v-col>
    <v-col style="max-width: calc(100% - 56px)">
      <map-script-menu v-if="activeWindow === 'scriptsPage'"/>
      <map-dossier v-if="activeWindow === 'dossierPage'"/>
    </v-col>
  </v-row>
</template>

<script>
import ToolsMenu from "../../WebsiteShell/UI/toolsMenu"
import MapScriptMenu from "./scriptsPage/mapScriptMenu"
import router from '@/router'
import {mapGetters} from "vuex"
import MapDossier from "./dossierPage/dossierPage";

export default {
  name: "mapMenu",
  components: {MapScriptMenu, ToolsMenu, MapDossier, },
  data: () => ({
  }),
  computed: {
    ...mapGetters(['activeTool', ]),
    activeWindow: function () {
      return this.activeTool(router.currentRoute.name)
    }
  },
}
</script>

<style scoped>

</style>
