<template>
  <custom-tooltip right>
    <template v-slot:activator="{ on }">
      <i v-show="showTriggers.length" v-on="on" :class="tooltipClass" :style="tooltipStyle"></i>
    </template>
    <template v-slot:body>
      <div v-for="trigger in showTriggers" class="px-2">{{trigger.title}}</div>
    </template>
  </custom-tooltip>
</template>

<script>
import CustomTooltip from "@/components/WebsiteShell/CustomComponents/Tooltip/customTooltip"
import {mapGetters} from "vuex"

export default {
  name: "triggerInformation",
  components: {CustomTooltip},
  props: {
    activeTriggers: Array,
    size: {
      type: String,
      default: '24px',
    }
  },
  computed: {
    ...mapGetters(['triggers']),
    showTriggers: function () { return this.triggers.filter(trigger => this.activeTriggers.includes(trigger.id)) },
    tooltipStyle: function () { return {fontSize: this.size, color: 'red'} },
    tooltipClass: function () { return "mdi mdi-alert-outline" },
  }
}
</script>

<style scoped>

</style>