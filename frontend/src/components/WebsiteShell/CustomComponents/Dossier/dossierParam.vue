<template>
  <tr>
    <td class="text-h6">{{param.baseParam.title}}</td>
    <td class="text-end">
      <custom-tooltip
          v-for="(value, index) in values"
          :key="index"
          :value="value.value"
          :type="getParamType"
          nudge-right="20"
          right
      >
        <template v-slot:activator="{ on }">
          <div v-on="on">
            <dossier-value
              :value="value"
              :rec-id="recId"
              :object-id="objectId"
              :title="title"
              :type="getParamType"
              :document="value.doc"
            />
          </div>
        </template>
      </custom-tooltip>
      <span v-if="paramsLength > 1" @click="showOldValues = !showOldValues" class="old-values">
        {{ showOldValues ? 'Скрыть' :'Старые значения' }}
      </span>
    </td>
  </tr>
</template>

<script>
import GeometryParam from "@/components/WebsiteShell/CustomComponents/Dossier/geometryParam"
import FileParam from "@/components/WebsiteShell/CustomComponents/Dossier/fileParam"
import DossierValue from "@/components/WebsiteShell/CustomComponents/Dossier/dossierValue";
import CustomTooltip from "@/components/WebsiteShell/CustomComponents/Tooltip/customTooltip";

export default {
  name: "dossierParam",
  components: {CustomTooltip, DossierValue, FileParam, GeometryParam},
  props: {
    param: Object,
    recId: Number,
    objectId: Number,
    title: {
      type: String,
      default: null
    }
  },
  data: () => ({
    showOldValues: false,
  }),
  computed: {
    paramsLength: function () {
      return this.param.values.length
    },
    values: function () {
      return this.param.values.slice(0, this.showOldValues ? this.paramsLength : 1)
    },
    getParamType: function () {
      return this.param.baseParam.type
    },
  },
}
</script>

<style scoped>
td {
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  padding: 6px 8px;
}
.old-values {
  font-size: 12px;
  color: green;
  cursor: pointer;
}
</style>