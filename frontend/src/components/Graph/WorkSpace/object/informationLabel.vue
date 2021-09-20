<template>
  <v-card hover width="fit-content">
    <table class="table" :style="{padding: sizeNode / 180}">
      <tr v-for="param in classifiers" :key="param.id" v-if="param.values.length" :style="{fontSize: sizeNode/40}">
        <td style="white-space: nowrap">{{param.baseParam.title}}</td>
        <td class="body-row" :style="{minWidth: sizeNode / 2}" v-if="param.values[0].value">{{param.values[0].value}}</td>
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
    allowParams: Array,
    sizeNode: Number,
  },
  computed: {
    classifiers: function () {
      return this.params.filter(param =>this.allowParams.includes(param.baseParam.id))
    }
  },
  watch: {
    classifiers: function () { this.$emit('update') }
  }
}
</script>

<style scoped>
.table {
  width: 100%;
  border-collapse: collapse;
  border-bottom: 1px solid #aaaaaa;
  background-color: #f2f2f2;
}
td {
  padding: 2px 8px;
}
.table tr:nth-child(even){background-color: white;}
.body-row {
  width: fit-content;
}
thead tr {
  background-color: #555555;
  color: white;
}
.v-item-group {
  position: initial;
}
</style>