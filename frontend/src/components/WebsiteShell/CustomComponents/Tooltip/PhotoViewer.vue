<template>
  <v-img :src="file" width="250" max-width="auto"/>
</template>

<script>
import {getFileLink} from "@/plugins/axiosSettings";

export default {
  name: "PhotoViewer",
  props: {
    objectId: Number,
    recId: Number,
    value: String
  },
  computed: {
    file: function () {
      return getFileLink(this.objectId, this.recId, this.value)
    },
  }
}
</script>

<style scoped>

</style>