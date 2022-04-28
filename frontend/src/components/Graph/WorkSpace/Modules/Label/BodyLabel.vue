<template>
  <v-card hover :max-width="size" oncontextmenu="return false">
    <table class="table">
      <row
        v-for="param in params"
        :key="param.id"
        :param="param"
        :show-date="showDate"
        :style="rowStyle"
      />
    </table>
  </v-card>
</template>

<script>
import Row from "@/components/Graph/WorkSpace/Modules/Label/RowLabel"

export default {
  name: "BodyLabel",
  components: {Row},
  props: {
    size: Number,
    params: Array,
    showDate: Boolean,
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