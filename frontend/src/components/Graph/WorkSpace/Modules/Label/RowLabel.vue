<template>
  <tr>
    <td>
      <span>{{title}}</span><br>
      <span v-if="showDoc && doc" class="teal--text" style="font-size: 0.8em">{{doc}}</span>
    </td>
    <td :class="valueClass" class="column-data">{{value}}</td>
    <td v-if="showDate" class="column-date text-end">{{date}}</td>
  </tr>
</template>

<script>
export default {
  name: "RowLabel",
  props: {
    param: Object,
    showDate: Boolean,
    showDoc: Boolean
  },
  computed: {
    valueClass: function () {
      return [!this.showDate ? 'text-end' : 'text-center']
    },
    title: function () {
      return this.param.baseParam.title
    },
    value: function () {
      if(this.param.baseParam.type.title === 'geometry') {
        if(this.param.baseParam.type.value === 'polygon') {
          return 'Полигон'
        } else if (this.param.baseParam.type.value === 'point') {
          return 'Точка'
        }
      } else {
        if (this.param.values[0].value.length > 255) {
          return this.param.values[0].value.slice(0, 255) + '...'
        } else {
          return this.param.values[0].value
        }
      }
    },
    date: function () {
      return this.param.values[0].date
    },
    doc: function () {
      return this.param.values[0].doc?.title
    }
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
.column-data {
  word-break: break-all;
}
</style>