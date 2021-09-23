<template>
  <v-badge overlap color="rgba(0, 0, 0, 0)">
    <template v-slot:badge>
      <trigger-information :active-triggers="triggers" :size="triggerSize"></trigger-information>
    </template>
    <v-hover v-slot="{ hover }">
      <v-avatar :size="bodySize" :class="getClassesObject(hover)">
        <v-img v-if="getPhoto" :src="getPhoto"></v-img>
        <i v-else :class="bodyIconClass" :style="bodyIconStyle"></i>
      </v-avatar>
    </v-hover>
  </v-badge>
</template>

<script>
import TriggerInformation from "@/components/WebsiteShell/UI/triggerInformation"
import {getFileLink} from "@/plugins/axios_settings"

export default {
  name: "bodyObject",
  components: {TriggerInformation},
  props: {
    node: Object,
    showTriggers: Boolean,
    selected: Boolean,
  },
  data: () => ({
    edgeButton: {hover: false, top: 0, left: 0}
  }),
  computed: {
    getPhoto: function () {
      if(this.node.object.photo)
        return getFileLink(this.node.object.object.id, this.node.object.recId, this.node.object.photo)
      else return null
    },
    bodySize: function () { return this.node.size / 3 },
    triggerSize: function () { return this.bodySize / 6 },
    bodyIconStyle: function () { return {fontSize: this.bodySize, color: '#aaaaaa', backgroundColor: 'white'} },
    bodyIconClass: function () { return 'mdi ' + this.node.object.object.icon },
    triggers: function () { return this.showTriggers ? this.node.object.triggers : []}
  },
  methods: {
    getClassesObject(hover) {
      if (hover && this.selected)
        return ['elevation-12', 'body-active']
      if (hover && !this.selected)
        return 'elevation-12'
      if (!hover && this.selected)
        return 'body-active'
      if (!hover && !this.selected)
        return 'elevation-6'
    }
  }
}
</script>

<style scoped>
.body, .body-active {
  background-color: white;
}
.body {
  box-shadow: 0 8px 9px -5px rgba(0, 0, 0, 0.2),
              0 15px 22px 2px rgba(0, 0, 0, 0.14),
              0 6px 28px 5px rgba(0, 0, 0, 0.12);
}
.body-active {
  box-shadow: 0 0 9px 5px rgba(255, 0, 0, 0.2),
              0 0 22px 2px rgba(255, 0, 0, 0.14),
              0 0 28px 5px rgba(255, 0, 0, 0.12) !important;
}
</style>