<template>
  <v-badge overlap color="rgba(0, 0, 0, 0)" class="badge">
    <template v-slot:badge>
      <trigger-information :active-triggers="triggers" :size="triggerSize"></trigger-information>
    </template>
    <v-avatar :size="bodySize" class="cursor-pointer" oncontextmenu="return false">
      <v-img v-if="getPhoto" :src="getPhoto"/>
      <v-icon v-else :size="bodySize">{{node.entity.base.icon}}</v-icon>
    </v-avatar>
    </v-badge>
</template>

<script>
import TriggerInformation from "@/components/WebsiteShell/CustomComponents/triggerInformation"
import {getFileLink} from "@/plugins/axiosSettings"

export default {
  name: "bodyObject",
  components: {TriggerInformation},
  props: {
    node: Object,
    showTriggers: Boolean
  },
  computed: {
    bodySize: function () { return `${this.node.size / 3}px` },
    triggerSize: function () { return `${this.node.size / 18}px` },
    triggers: function () { return this.showTriggers ? this.node.entity.triggers : []},
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
.badge {
  border-radius: 50%;
}
</style>