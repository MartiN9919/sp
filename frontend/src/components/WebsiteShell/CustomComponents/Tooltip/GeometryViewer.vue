<template>
  <LeafletViewer v-if="fc" :fc="fc" :controls="false" class="geometry-viewer"/>
</template>

<script>
import LeafletViewer from "@/components/Map/Leaflet/LeafletViewer";
import {fc_normalize} from "@/components/Map/Leaflet/Lib/LibFc";

export default {
  name: "GeometryViewer",
  components: {LeafletViewer},
  props: {
    value: [String, Object]
  },
  computed: {
    fc: function () {
      return fc_normalize(this.value) || JSON.parse(this.value)
    }
  }
}
</script>

<style scoped>
.geometry-viewer {
  width: 15vh !important;
  height: 15vh !important;
  margin-left: auto;
  margin-right: auto;
}
</style>