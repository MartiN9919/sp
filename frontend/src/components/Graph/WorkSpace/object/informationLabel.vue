<template>
  <v-card hover width="fit-content">
    <table class="table" :style="tableStyle">
      <tr v-for="param in params" :key="param.id" :style="rowStyle">
        <td class="information-column">{{param.baseParam.title}}</td>
        <td :style="valueColStyle">{{param.values[0].value}}</td>
        <td v-if="showDate" class="information-column">{{param.values[0].date}}</td>
      </tr>
    </table>
  </v-card>
</template>


<script>

export default {
  name: "tooltip",
  props: {
    params: Array,
    sizeNode: Number,
    showDate: Boolean,
  },
  computed: {
    tableStyle: function () {
      return {padding: `${this.sizeNode / 180}px`}
    },
    rowStyle: function () {
      return {fontSize: `${this.sizeNode / 40}px`}
    },
    valueColStyle: function () {
      return {maxWidth: `${this.sizeNode / 2}px`}
    }
  }
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