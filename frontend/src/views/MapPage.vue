<template>
  <split-panel shadow-effect>
    <template v-slot:firstPane>
      <map-menu></map-menu>
    </template>
    <template v-slot:secondPane>
      <LeafletMain
        @selectObj="selectObj"
      />
    </template>
  </split-panel>
</template>

<script>
import SplitPanel from "../components/WebsiteShell/UI/splitPanel"
import LeafletMain from '../components/Map/Leaflet/LeafletMain'
import MapMenu from "../components/Map/MapMenu/mapMenu"
import { mapActions } from "vuex"

export default {
  name: 'MapPage',
  components: { SplitPanel, MapMenu, LeafletMain, },
  mounted() {
    this.setDefaultValueActiveTool()
  },
  methods: {
    ...mapActions(['setDefaultValueActiveTool', ]),
    selectObj(obj) {
      console.log('Выбран объект:', obj)
    },
  },

}
</script>

<style scoped>

</style>
