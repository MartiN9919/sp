<template>
  <div>
    <v-dialog class="dialog" width="60%" style="z-index: 100001">
      <template v-slot:activator="{ on, attrs }">
        <span v-bind="attrs" v-on="on" class="teal--text">
          <slot/>
        </span>
      </template>
      <v-card>
        <v-card-title v-if="title" class="text-h7">{{ title }}</v-card-title>
        <v-divider/>
        <leaflet-viewer style="height: 70vh;" :fc="JSON.parse(value)" :controls="true"/>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import LeafletViewer from "@/components/Map/Leaflet/LeafletViewer"

export default {
  name: "geometryParam",
  components: {LeafletViewer},
  props: {
    value: String,
    title: {
      type: String,
      default: null,
    },
  }
}
</script>

<style scoped>

</style>