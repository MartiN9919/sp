<template>
  <v-card hover :max-width="sizeNode" :min-width="sizeNode">
    <table class="table">
      <tr v-for="param in params" :key="param.id" :style="rowStyle">
        <td class="information-column">{{param.baseParam.title}}</td>
        <td v-if="param.values[0].value" class="content-column text-center" :class="!showDate && 'text-end'">{{param.values[0].value}}</td>
        <td v-if="showDate" class="column-date text-end">{{param.values[0].date}}</td>
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
    rowStyle: function () {
      return {fontSize: `${this.sizeNode / 40}px`}
    },
  }
}
</script>

<style scoped>
.table {
  width: 100%;
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
  width: auto;
}
.column-date {
  white-space: nowrap;
}
.content-column {
  width: 100%;
}
</style>