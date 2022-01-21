<template>
  <a :href="getDownloadLink()">
    <slot/>
  </a>
</template>

<script>
import {getDownloadFileLink} from "@/plugins/axiosSettings"

export default {
  name: "fileParam",
  props: {
    objectId: Number,
    recId: Number,
    value: String,
  },
  methods: {
    getDownloadLink() {
      return getDownloadFileLink(this.objectId, this.recId, this.value)
    },
  }
}
</script>

<style scoped>

</style>