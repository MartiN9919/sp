<template>
  <v-row no-gutters style="flex-wrap: nowrap; height: 100%">
    <v-col cols="auto">
      <tools-menu/>
    </v-col>
    <v-col class="overflow-y-auto">
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
