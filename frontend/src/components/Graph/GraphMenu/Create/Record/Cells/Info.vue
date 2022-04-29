<template>
  <td class="text-break col-info">
    <a tabindex="-1" v-if="isFile" :href="downloadLink">{{ value }}</a>
    <geometry-param v-else-if="isGeometry" :value="value" :title="title">
      {{ geometryTextValue }}
    </geometry-param>
    <span v-else>{{ value ? value : 'Создана' }}</span>
  </td>
</template>

<script>
import GeometryParam from "@/components/WebsiteShell/CustomComponents/Dossier/geometryParam";
import {getDownloadFileLink} from '@/plugins/axiosSettings'

export default {
  name: "Info",
  components: {GeometryParam},
  props: {
    value: String,
    title: String,
    typeRecord: Object,
    settings: Object
  },
  computed: {
    geometryTextValue: function () {
      return this.typeRecord.value === 'polygon' ? 'Геометрия' : 'Точка'
    },
    isFile: function () {
      return this.typeRecord.title === 'file'
    },
    isGeometry: function () {
      return this.typeRecord.title === 'geometry'
    },
    downloadLink: function () {
      return getDownloadFileLink(this.settings.objectId, this.settings.recId, this.value)
    },
  }
}
</script>

<style scoped>
.col-info {
  min-width: 5em;
}
</style>