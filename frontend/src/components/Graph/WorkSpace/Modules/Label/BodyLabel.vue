<template>
  <v-card hover :max-width="size" oncontextmenu="return false">
    <table class="table">
      <row-label
        v-for="param in params"
        :key="param.id"
        :param="param"
        :show-date="showDate"
        :show-doc="showDoc"
        :style="rowStyle"
      />
    </table>
  </v-card>
</template>

<script>
import RowLabel from "@/components/Graph/WorkSpace/Modules/Label/RowLabel"

export default {
  name: "BodyLabel",
  components: {RowLabel},
  props: {
    size: Number,
    params: Array,
    showDate: Boolean,
    showDoc: Boolean
  },
  computed: {
    rowStyle: function () {
      return {fontSize: `${this.size / 40}px`}
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
</style>