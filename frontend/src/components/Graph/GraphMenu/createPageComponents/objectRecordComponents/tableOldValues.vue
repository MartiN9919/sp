<template>
  <table>
    <tbody class="py-2">
    <tr v-for="item in values">
      <td>
        <span>{{item.value}}</span>
      </td>
      <td class="text-end text-no-wrap pl-3">
        <span>{{item.date}}</span>
      </td>
    </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "tableOldValues",
  props: {
    values: Array,
  }
}
</script>

<style scoped>
table {
  width: 100%;
  color: #757575;
  border-spacing: initial;
}
td {
  height: 0.9em
}
span {
  font-size: 0.8em
}
</style>