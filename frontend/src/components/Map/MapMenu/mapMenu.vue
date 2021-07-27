<template>
  <v-row no-gutters style="flex-wrap: nowrap; height: 100%">
    <v-col cols="auto">
      <tools-menu></tools-menu>
    </v-col>
    <v-col class="overflow-y-auto">
      <map-script-menu v-if="activeWindow === 'scriptsPage'"></map-script-menu>
      <h1 v-if="activeWindow === 'dossierPage'">Dossier Page</h1>
    </v-col>
  </v-row>
</template>

<script>
import ToolsMenu from "../../WebsiteShell/UI/toolsMenu"
import MapScriptMenu from "./scriptsPage/mapScriptMenu"
import router from '@/router'
import {mapGetters} from "vuex"

export default {
  name: "mapMenu",
  components: {MapScriptMenu, ToolsMenu, },
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