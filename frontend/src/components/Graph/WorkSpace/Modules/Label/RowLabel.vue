<template>
  <tr>
    <td class="information-column">{{title}}</td>
    <td :class="valueClass">{{value}}</td>
    <td v-if="showDate" class="column-date text-end">{{date}}</td>
  </tr>
</template>

<script>
export default {
  name: "RowLabel",
  props: {
    param: Object,
    showDate: Boolean,
  },
  computed: {
    valueClass: function () {
      return ['content-column', !this.showDate ? 'text-end' : 'text-center']
    },
    title: function () {
      return this.param.baseParam.title
    },
    value: function () {
      return this.param.values[0].value
    },
    date: function () {
      return this.param.values[0].date
    },
  }
}
</script>

<style scoped>
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