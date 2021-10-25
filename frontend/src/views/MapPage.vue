<template>
  <split-panel shadow-effect>
    <template v-slot:firstPane>
      <map-menu></map-menu>
    </template>
    <template v-slot:secondPane>
      <LeafletMain/>
    </template>
  </split-panel>
</template>

<script>
import SplitPanel from "../components/WebsiteShell/UI/splitPanel"
import LeafletMain from '../components/Map/Leaflet/LeafletMain'
import MapMenu from "../components/Map/MapMenu/mapMenu"
import { mapGetters, mapActions } from "vuex"

export default {
  name: 'MapPage',
  components: { SplitPanel, MapMenu, LeafletMain, },

  mounted() {
    this.setDefaultValueActiveTool()
  },

  watch: {
    SCRIPT_GET_ITEM_SEL: function(obj) {
      console.log('Выбраны объекты:', obj)
    },
  },

  computed: {
    ...mapGetters([
      'SCRIPT_GET_ITEM_SEL',
    ]),
  },

  methods: {
    ...mapActions(['setDefaultValueActiveTool', ]),
  },

}
</script>

<style scoped>

</style>
