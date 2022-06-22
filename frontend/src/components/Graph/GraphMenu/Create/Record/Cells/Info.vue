<template>
  <td class="text-break col-info">
    <info-param :value="value" :title="title" :date="date" :base="base" :rec-id="recId"/>
  </td>
</template>

<script>
import InfoParam from "@/components/WebsiteShell/CustomComponents/Dossier/infoParam"

export default {
  name: "Info",
  components: {InfoParam},
  props: {
    value: String,
    title: String,
    date: String,
    recId: Number,
    base: Object,
    type: Object,
  },
}
</script>

<style scoped>
.col-info {
  min-width: 5em;
}
</style>