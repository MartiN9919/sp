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
const SearchObjectPage = () => import("@/components/Graph/GraphMenu/Search/SearchObjectPage")
const SearchRelationPage = () => import("@/components/Graph/GraphMenu/Search/SearchRelationPage")
const CreateObjectPage = () => import("@/components/Graph/GraphMenu/Create/CreateObjectPage")
const CreateRelationPage = () => import("@/components/Graph/GraphMenu/Create/CreateRelationPage")
const SettingsPage = () => import("@/components/Graph/GraphMenu/Settings/SettingsPage")
const TimeLinePage = () => import("@/components/Graph/GraphMenu/Timeline/TimeLinePage")
import SplitPanel from "@/components/WebsiteShell/CustomComponents/splitPanel"
import graphArea from '@/components/Graph/WorkSpace/graphArea'
import toolsMenu from "@/components/WebsiteShell/CustomComponents/toolsMenu"
import {mapActions, mapGetters} from "vuex"
import router from '@/router'

export default {
  name: 'Graph',
  components: {
    SplitPanel,
    graphArea,
    toolsMenu,
    SearchObjectPage,
    SearchRelationPage,
    CreateObjectPage,
    CreateRelationPage,
    SettingsPage,
    TimeLinePage
  },
  computed: mapGetters(['activeTool']),
  methods: {
    ...mapActions(['setRootSearchTreeItem']),
    changeComponent() {
      switch (this.activeTool(router.currentRoute.name)) {
        case 'SearchObjectPage':
          return 'SearchObjectPage'
        case 'SearchRelationPage':
          return 'SearchRelationPage'
        case 'CreateObjectPage':
          return 'CreateObjectPage'
        case 'CreateRelationPage':
          return 'CreateRelationPage'
        case 'SettingsPage':
          return 'SettingsPage'
        case 'TimeLinePage':
          return 'TimeLinePage'
        default:
          return 'SearchObjectPage'
      }
    }
  },
  mounted() {
    this.setRootSearchTreeItem({})
  }
}
</script>
