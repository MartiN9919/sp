<template>
  <split-panel shadow-effect>
    <template v-slot:firstPane>
      <v-row no-gutters class="graph-menu">
        <tools-menu></tools-menu>
        <component :is="changeComponent()" :style="stylesComponent"></component>
      </v-row>
    </template>
    <template v-slot:secondPane>
      <graph-area></graph-area>
    </template>
  </split-panel>
</template>

<script>
const searchPage = () => import("../components/Graph/GraphMenu/searchPage")
const searchRelationPage = () => import("../components/Graph/GraphMenu/searchRelationPage")
const createObjectPage = () => import("../components/Graph/GraphMenu/createObjectPage")
const createRelationPage = () => import("../components/Graph/GraphMenu/createRelationPage")
const settingsPage = () => import("../components/Graph/GraphMenu/settingsPage")
import SplitPanel from "../components/WebsiteShell/UI/splitPanel"
import graphArea from '../components/Graph/WorkSpace/graphArea'
import toolsMenu from "../components/WebsiteShell/UI/toolsMenu"
import {mapActions, mapGetters} from "vuex"
import router from '@/router'

export default {
  name: 'GraphPage',
  components: {
    SplitPanel,
    graphArea,
    toolsMenu,
    searchPage,
    searchRelationPage,
    createObjectPage,
    createRelationPage,
    settingsPage
  },
  computed: {
    ...mapGetters(['activeTool']),
    stylesComponent: function () {
      return { 'max-width': `calc(100% - ${this.$CONST.APP.TOOL_MENU.WIDTH}px)`}
    },
    activeWindow: function () {
      return this.activeTool(router.currentRoute.name)
    }
  },
  methods: {
    ...mapActions([
      'setDefaultValueActiveTool',
      'getBaseObjects',
      'setRootSearchTreeItem',
      'getBaseTriggers',
      'getBaseRelations',
      'getBaseClassifiers'
    ]),
    changeComponent() {
      if (this.activeWindow === 'searchPage')
        return 'searchPage'
      if (this.activeWindow === 'searchRelationPage')
        return 'searchRelationPage'
      if (this.activeWindow === 'createObjectPage')
        return 'createObjectPage'
      if (this.activeWindow === 'createRelationPage')
        return 'createRelationPage'
      if (this.activeWindow === 'settingsPage')
        return 'settingsPage'
    }
  },
  mounted() {
    this.getBaseObjects()
      .then(() => {
        this.setDefaultValueActiveTool()
        this.setRootSearchTreeItem({})
      })
    this.getBaseTriggers()
    this.getBaseRelations()
    this.getBaseClassifiers()
  }
}
</script>

<style>
.graph-menu {
  flex-wrap: nowrap;
  height: 100%;
}
</style>
