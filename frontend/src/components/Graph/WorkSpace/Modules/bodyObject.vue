<template>
  <v-avatar :size="bodySize" class="cursor-pointer">
    <v-img v-if="getPhoto" :src="getPhoto"/>
    <v-icon v-else :size="bodySize">{{node.entity.base.icon}}</v-icon>
  </v-avatar>
</template>

<script>
import {getFileLink} from "@/plugins/axiosSettings"

export default {
  name: "bodyObject",
  props: {
    node: Object,
  },
  computed: {
    bodySize: function () { return `${this.node.size / 3}px` },
    getPhoto: function () {
      if(this.node.entity.photo)
        return getFileLink(this.node.ids.object_id, this.node.ids.rec_id, this.node.entity.photo)
      else return null
    },
  },
}
</script>

<style scoped>
.v-icon {
  transition: none;
}
</style>