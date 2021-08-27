<template>

</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "tableOldValues",
  props: {
    values: Array,
  },
  computed: {
    ...mapGetters(['editableObjects', 'editableRelation']),
  },
  methods: {
    textColorStyle(item) {
      for(let param of this.editableObjects[0].params) {
        if (!param.values.find(value => value.value === item.value && value.date === item.date))
          return 'red--text'
      }
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