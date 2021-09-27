<template>
  <v-card hover width="fit-content">
    <table class="table" :style="{padding: sizeNode / 180}">
      <tr
        v-if="param.values.length"
        v-for="param in params" :key="param.id"
        :style="{fontSize: sizeNode/40}"
      >
        <td class="information-column">
          {{param.baseParam.title}}
        </td>
        <td v-if="param.values[0].value" :style="{maxWidth: sizeNode / 2}">
          {{param.values[0].value}}
        </td>
        <td v-if="showDate" class="information-column">
          {{param.values[0].date}}
        </td>
      </tr>
    </table>
  </v-card>
</template>


<script>
import CustomTooltip from "@/components/WebsiteShell/UI/customTooltip"

export default {
  name: "tooltip",
  components: {CustomTooltip},
  props: {
    params: Array,
    sizeNode: Number,
    showDate: {
      type: Boolean,
      default: false,
    }
  },
}
</script>

<style scoped>
.table {
  width: max-content;
  border-collapse: collapse;
  background-color: #f2f2f2;
}
td {
  padding: 2px 8px;
}
.table tr:nth-child(even) {
  background-color: white;
}
thead tr {
  background-color: #555555;
  color: white;
}
.v-item-group {
  position: initial;
}
.information-column {
  white-space: nowrap;
}
</style>