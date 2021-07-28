<template>
  <v-row no-gutters style="flex-wrap: nowrap; height: 100%">
    <v-col cols="auto">
      <tools-menu></tools-menu>
    </v-col>
    <v-col v-if="activeWindow === 'searchPage'" class="search-page">
      <search-tree v-model="searchTreeItems" @findObject="findObject" class="search-tree"></search-tree>
      <found-objects v-if="foundObjects" :objects="foundObjects" class="found-objects"></found-objects>
    </v-col>
    <v-col v-if="activeWindow === 'addPage'">
      <h1>Add Page</h1>
    </v-col>
<!--      <h1 v-if="activeWindow === 'dossierPage'">Dossier Page</h1>-->
  </v-row>
</template>

<script>
import ToolsMenu from "../../WebsiteShell/UI/toolsMenu"
import SearchTree from "./searchTree/searchTree"
import FoundObjects from "./foundObjects/foundObjects"
import router from '@/router'
import { mapActions, mapGetters } from "vuex"

export default {
  name: "graphMenu",
  components: { FoundObjects, SearchTree, ToolsMenu, },
  computed: {
    ...mapGetters(['activeTool', 'searchTreeGraph', 'foundObjects', ]),
    activeWindow: function () {
      return this.activeTool(router.currentRoute.name)
    },
    searchTreeItems: {
      get: function () { return this.searchTreeGraph },
      set: function (value) { this.setRootSearchTreeGraph(value) }
    },
  },
  methods: {
    ...mapActions(['setRootSearchTreeGraph', 'findObjectsOnServer', ]),
    findObject () {
      this.findObjectsOnServer({ searchTree: this.searchTreeItems })
    },
  },
}
</script>

<style scoped>
.search-page {
  display: flex;
  flex-direction: column
}
.search-tree {
  max-height: 30%;
  overflow-y: auto;
  flex-shrink: 0;
  padding-bottom: 8px;
}
.found-objects {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>