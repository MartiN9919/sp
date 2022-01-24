<template>
  <v-avatar :size="bodySize" class="cursor-pointer">
    <v-img v-if="getPhoto" :src="getPhoto"/>
    <v-icon v-else :size="bodySize">{{object.object.object.icon}}</v-icon>
  </v-avatar>
</template>

<script>
import {getFileLink} from "@/plugins/axiosSettings"

export default {
  name: "bodyObject",
  props: {
    object: Object,
  },
  computed: {
    bodySize: function () { return `${this.object.size / 3}px` },
    getPhoto: function () {
      if(this.object.object.photo)
        return getFileLink(this.object.object.object.id, this.object.object.recId, this.object.object.photo)
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