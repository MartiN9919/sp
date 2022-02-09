<template>
  <v-card hover :max-width="maxWidth">
    <table class="table">
      <tr v-for="param in params" :key="param.id" :style="rowStyle">
        <td class="information-column" :class="(!param.values[0].value && !showDate) && 'text-center'">{{param.baseParam.title}}</td>
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
    maxWidth: Number,
    showDate: Boolean,
  },
  computed: {
    rowStyle: function () {
      return {fontSize: `${this.maxWidth / 40}px`}
    },
  }
}
</script>

<style scoped>
table {
  width: max-content;
  max-width: 100%;
  background-color: #f2f2f2;
  border-collapse: collapse;
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
.column-date {
  white-space: nowrap;
}
.content-column {
  width: 100%;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}
</style>