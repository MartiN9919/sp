<template>
  <split-panel shadow-effect>
    <template v-slot:firstPane>
      <v-row no-gutters class="graph-menu">
        <tools-menu></tools-menu>
        <component :is="changeComponent()" class="page"></component>
      </v-row>
    </template>
    <template v-slot:secondPane>
      <graph-area></graph-area>
    </template>
  </split-panel>
</template>

<script>
import SplitPanel from "../components/WebsiteShell/UI/splitPanel"
import graphArea from '../components/Graph/WorkSpace/graphArea'
import toolsMenu from "../components/WebsiteShell/UI/toolsMenu"
import searchPage from "../components/Graph/GraphMenu/searchPage"
import createPage from "../components/Graph/GraphMenu/createPage"
import dossierPage from "../components/Graph/GraphMenu/dossierPage"
import createRelationPage from "../components/Graph/GraphMenu/createRelationPage"
import settingsPage from "../components/Graph/GraphMenu/settingsPage"
import {mapActions, mapGetters} from "vuex"
import router from '@/router'

export default {
  name: 'GraphPage',
  components: {SplitPanel, graphArea, toolsMenu, searchPage, createPage, dossierPage, createRelationPage, settingsPage},
  computed: {
    ...mapGetters(['activeTool']),
    activeWindow: function () {
      return this.activeTool(router.currentRoute.name)
    },
  },
  methods: {
    ...mapActions(['setDefaultValueActiveTool', 'getBaseObjects', 'setRootSearchTreeItem', 'getBaseTriggers', "getBaseRelations"]),
    changeComponent() {
      if (this.activeWindow === 'searchPage')
        return 'searchPage'
      if (this.activeWindow === 'createPage')
        return 'createPage'
      if (this.activeWindow === 'dossierPage')
        return 'dossierPage'
      if (this.activeWindow === 'createRelationPage')
        return 'createRelationPage'
      if (this.activeWindow === 'settingsPage')
        return 'settingsPage'
    },
  },
  mounted() {
    this.getBaseObjects({})
    .then(() => {
      this.setDefaultValueActiveTool()
      this.setRootSearchTreeItem({})
    })
    this.getBaseTriggers()
    this.getBaseRelations()
  },
}
</script>

<style>
.graph-menu {
  flex-wrap: nowrap;
  height: 100%;
}

.page {
  max-width: calc(100% - 56px)
}
</style>
