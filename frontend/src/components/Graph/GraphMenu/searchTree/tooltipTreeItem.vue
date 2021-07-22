<template>
  <table style="width:100%">
    <tr>
      <th>Связь</th>
      <td colspan="2">{{ labelRelation(item) }}</td>
    </tr>
    <tr>
      <th rowspan="3">Период</th>
    </tr>
    <tr>
      <th>Дата начала</th>
      <th>Дата конца</th>
    </tr>
    <tr>
      <td>{{ item.rel.date_time_start }}</td>
      <td>{{ item.rel.date_time_end }}</td>
    </tr>
    <tr>
      <th>Поиск по актуальным значениям</th>
      <td colspan="2">
        <v-icon v-if="item.actual" color="green">mdi-check</v-icon>
        <v-icon v-else color="red">mdi-close</v-icon>
      </td>
    </tr>
  </table>
</template>

<script>
export default {
  name: "tooltipTreeItem",
  props: {
    item: Object,
  },
  methods: {
    labelRelation (item) {
      let relation = this.$store.getters.relationObject(item.rel.id)
      let relationTitle = relation ? relation.title: 'Не выбрана'
      let relationValueTitle = ''
      if (relation?.list) {
        let relationValue = relation.list.find(i => i.id === item.rel.value)
        if (relationValue) relationValueTitle = '(' + relationValue.value + ')'
      }
      return relationTitle + relationValueTitle
    },
  }
}
</script>

<style scoped>
table {
  border-collapse: collapse;
  table-layout: fixed;
  font-size: 0.80em;
  color: white;
  width: 100%;
}

th {
  text-align: center;
}
td, th {
  border: 1px solid white;
  padding: 2px 5px;
  white-space: pre-wrap;
}
</style>