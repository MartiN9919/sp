<template>
  <v-row no-gutters style="flex-wrap: nowrap; height: 100%">
    <v-col cols="auto">
      <tools-menu
        v-model="activeTool"
        :toolsMenu="toolsMapMenu"
      ></tools-menu>
    </v-col>
    <v-col class="overflow-y-auto">
      <map-script-menu v-if="activeTool === 'scriptsPage'"></map-script-menu>
      <h1 v-if="activeTool === 'dossierPage'">Dossier Page</h1>
    </v-col>
  </v-row>
</template>

<script>
import ToolsMenu from "../../Graph/GraphMenu/toolsMenu";
import {mapActions, mapGetters} from "vuex";
import MapScriptMenu from "./scriptsPage/mapScriptMenu";

export default {
  name: "mapMenu",
  components: {MapScriptMenu, ToolsMenu, },
  data: () => ({
  }),
  computed: {
    ...mapGetters(['activeToolMap', 'toolsMapMenu']),
    activeTool: {
      get: function () { return this.activeToolMap },
      set: function (value) { this.setActiveToolMap(value) }
    }
  },
  methods: {
    ...mapActions(['setActiveToolMap', ]),
  },
}
</script>

<style scoped>

</style>