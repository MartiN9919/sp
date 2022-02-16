<template>
  <div class="py-1">
    <geometry-param v-if="isGeometry" :value="getValue" :title="title">
      {{ getGeometryTextValue }}
    </geometry-param>
    <file-param v-else-if="isFile" :value="getValue" :rec-id="recId" :object-id="objectId" class="text-wrap tile--text">
      {{ getTextValue }}
    </file-param>
    <div v-else class="text-wrap black--text">{{getTextValue}}</div>
    <div style="font-size: 10px; font-style: italic">{{getDate}}</div>
  </div>
</template>

<script>
import GeometryParam from "@/components/WebsiteShell/CustomComponents/Dossier/geometryParam"
import FileParam from "@/components/WebsiteShell/CustomComponents/Dossier/fileParam"

export default {
  name: "dossierValue",
  components: {FileParam, GeometryParam},
  props: {
    value: Object,
    recId: Number,
    objectId: Number,
    title: {
      type: String,
      default: null
    },
    type: Object,
  },
  computed: {
    getValue: function () {
      return this.value.value
    },
    isGeometry: function () {
      return this.type.title === 'geometry'
    },
    isFile: function () {
      return this.type.title === 'file' && this.type.value === 'any'
    },
    getTextValue: function () {
      return this.getValue.length > 255 ? this.getValue.slice(0, 255) + '...' : this.value.value
    },
    getDate: function () {
      return this.value.date
    },
    getGeometryTextValue: function () {
      return this.type.value === 'polygon' ? 'Геометрия' : 'Точка'
    },
  }
}
</script>

<style scoped>

</style>