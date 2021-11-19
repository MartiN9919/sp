<template>
  <split-panel shadow-effect>
    <template v-slot:firstPane>
      <tools-menu>
        <component :is="changeComponent()"/>
      </tools-menu>
    </template>
    <template v-slot:secondPane>
      <graph-area/>
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
  name: 'Graph',
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
  computed: mapGetters(['activeTool']),
  methods: {
    ...mapActions(['setRootSearchTreeItem']),
    changeComponent() {
      switch (this.activeTool(router.currentRoute.name)) {
        case 'searchPage':
          return 'searchPage'
        case 'searchRelationPage':
          return 'searchRelationPage'
        case 'createObjectPage':
          return 'createObjectPage'
        case 'createRelationPage':
          return 'createRelationPage'
        case 'settingsPage':
          return 'settingsPage'
        default:
          return 'searchPage'
      }
    }
  },
  mounted() {
    this.setRootSearchTreeItem({})
  }
}
</script>

<style>

</style>
