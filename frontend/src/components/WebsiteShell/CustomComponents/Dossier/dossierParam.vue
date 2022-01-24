<template>
  <tr>
    <td class="text-h6">{{param.baseParam.title}}</td>
    <td class="text-end">
      <geometry-param v-if="isGeometry" :value="getValue" :title="title">
        <div class="text-wrap tile--text">
          {{ getGeometryTextValue }}
        </div>
      </geometry-param>
      <file-param v-else-if="isFile" :value="getValue" :rec-id="recId" :object-id="objectId">
        <div class="text-wrap tile--text">
          {{ getTextValue }}
        </div>
      </file-param>
      <div v-else class="text-wrap black--text">{{getTextValue}}</div>
      <div style="font-size: 10px; font-style: italic">{{getDate}}</div>
    </td>
  </tr>
</template>

<script>
import GeometryParam from "@/components/WebsiteShell/CustomComponents/Dossier/geometryParam"
import FileParam from "@/components/WebsiteShell/CustomComponents/Dossier/fileParam"

export default {
  name: "dossierParam",
  components: {FileParam, GeometryParam},
  props: {
    param: Object,
    recId: Number,
    objectId: Number,
    title: {
      type: String,
      default: null
    }
  },
  computed: {
    getValue: function () {
      return this.param.values[0].value
    },
    isGeometry: function () {
      return this.getClassifierType === 'geometry' || this.getClassifierType === 'geometry_point'
    },
    isFile: function () {
      return this.getClassifierType === 'file_any'
    },
    getTextValue: function () {
      return this.getValue.length > 255 ? this.getValue.slice(0, 255) + '...' : this.param.values[0].value
    },
    getDate: function () {
      return this.param.values[0].date
    },
    getGeometryTextValue: function () {
      return this.getClassifierType === 'geometry' ? 'Геометрия' : 'Точка'
    },
    getClassifierType: function () {
      return this.param.baseParam.type.title
    },
  },
}
</script>

<style scoped>
td {
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  padding: 6px 0;
}
</style>