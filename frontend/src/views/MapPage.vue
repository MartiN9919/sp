<template>
  <split-panel shadow-effect>
    <template v-slot:firstPane>
      <map-script-menu/>
    </template>
    <template v-slot:secondPane>
      <LeafletMain/>
    </template>
  </split-panel>
</template>

<script>
import SplitPanel from "@/components/WebsiteShell/CustomComponents/splitPanel"
import LeafletMain from '@/components/Map/Leaflet/LeafletMain'
const MapScriptMenu = () => import("@/components/Map/MapMenu/scriptsPage/mapScriptMenu")

export default {
  name: 'Map',
  components: {SplitPanel, LeafletMain, MapScriptMenu},
}
</script>
