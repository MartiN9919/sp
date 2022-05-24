<template>
  <div>
    <v-dialog class="dialog" width="60%" style="z-index: 100001">
      <template v-slot:activator="{ on: on_dialog, attrs: attrs_dialog }">

        <v-tooltip slot="activator" right open-delay="200" close-delay="400" transition="scroll-x-transition">
          <span slot="activator" class="teal--text">
            <slot/>
          </span>

          <!--
            tooltip content
            позиционирование карты EditorPreview производится ТОЛЬКО на видимом окне
          -->
          <span>
            <EditorPreview
              :id="0"
              :funGetFC="funGetFC"
            />
          </span>

        </v-tooltip>
      </template>

      <!-- dialog content -->
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
import EditorPreview from '@/components/Map/Leaflet/Components/Editor/EditorPreview';
import { fc_normalize, } from '@/components/Map/Leaflet/Lib/LibFc';

export default {
  name: "geometryParam",
  components: {LeafletViewer, EditorPreview,},
  props: {
    value: String,
    title: {
      type: String,
      default: null,
    },
  },
  methods: {
    funGetFC(id, fun) {
      this.$nextTick(() => {
        fun(fc_normalize(JSON.parse(this.value)));
      });
    },
  },
}
</script>

<style scoped>

</style>