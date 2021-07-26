<template>
  <ResSplitPane
    split-to="columns"
    :allow-resize="true"
    :min-size="15"
    :max-size="85"
    :resizerBorderThickness="1"
    :resizerThickness="1"
    :size="drawer ? sizeNavigation : 0"
    v-on:update:size="sizeNavigation = $event"
    units="percents">
    <v-col class="pa-0" slot="firstPane">
      <map-menu></map-menu>
    </v-col>
    <v-col class="pa-0" slot="secondPane">
      <LeafletMain></LeafletMain>
    </v-col>
  </ResSplitPane>
</template>

<script>
import LeafletMain from '../components/Map/Leaflet/LeafletMain'
import MapMenu from "../components/Map/MapMenu/mapMenu"
import ResSplitPane from 'vue-resize-split-pane'
import NavigationDrawer from '../components/WebsiteShell/Mixins/NavigationDrawer'
import { mapActions } from "vuex"

export default {
  name: 'MapPage',
  components: { MapMenu, LeafletMain, ResSplitPane },
  mixins: [NavigationDrawer],
  methods: {
    ...mapActions(['setDefaultValueActiveToolMap', ]),
  },
  mounted() {
    this.setDefaultValueActiveToolMap()
  },
}
</script>

<style scoped>

</style>
