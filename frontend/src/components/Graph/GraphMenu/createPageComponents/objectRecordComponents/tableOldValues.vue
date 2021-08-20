<template>
  <table>
    <tbody class="py-2">
    <tr v-for="item in values">
      <td>
        <span :class="textColorStyle(item)">{{item.value}}</span>
      </td>
      <td class="text-end text-no-wrap pl-3">
        <span :class="textColorStyle(item)">{{item.date}}</span>
      </td>
    </tr>
    </tbody>
  </table>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "tableOldValues",
  props: {
    values: Array,
  },
  computed: {
    ...mapGetters(['editableObjects']),
  },
  methods: {
    textColorStyle(item) {
      if(!this.editableObjects[0].params.find(
          param => param.values.find(
              value => value.value === item.value && value.date === item.date
          )
      ))
        return 'conflict-span'
    }
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
.conflict-span {
  color: #FF0000
}
</style>