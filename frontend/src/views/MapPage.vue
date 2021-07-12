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
      <map-script-menu></map-script-menu>
    </v-col>
    <v-col class="pa-0" slot="secondPane">
      <LeafletMain></LeafletMain>
    </v-col>
  </ResSplitPane>
</template>

<script>
import LeafletMain from '../components/Map/Leaflet/LeafletMain'
import mapScriptMenu from '../components/Map/MapMenu/mapScriptMenu'
import ResSplitPane from 'vue-resize-split-pane'
import NavigationDrawer from '../components/WebsiteShell/Mixins/NavigationDrawer'

export default {
  name: 'MapPage',
  components: { LeafletMain, mapScriptMenu, ResSplitPane },
  mixins: [NavigationDrawer]
}
</script>

<style scoped>

</style>
