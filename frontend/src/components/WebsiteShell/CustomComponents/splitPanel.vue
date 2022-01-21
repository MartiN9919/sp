<template>
  <ResSplitPane
      ref="ResSplitPane"
      split-to="columns"
      :allow-resize="true"
      :min-size="15"
      :max-size="85"
      :resizerBorderThickness="1"
      :resizerThickness="1"
      :size="size"
      v-on:update:size="sizeColumn.value = $event"
      units="percents"
      class="split-panel"
  >
    <v-col :id="$router.currentRoute.name + '1'" class="pa-0 split-column" slot="firstPane">
      <slot name="firstPane"></slot>
    </v-col>
    <v-col :id="$router.currentRoute.name + '2'" class="pa-0 split-column" slot="secondPane">
      <slot name="secondPane"></slot>
    </v-col>
  </ResSplitPane>
</template>

<script>
import router from '@/router'
import {mapGetters} from "vuex"
import ResSplitPane from 'vue-resize-split-pane'
import UserSetting from "@/store/addition";

export default {
  name: "splitPanel",
  components: {ResSplitPane},
  props: {
    shadowEffect: {
      type: Boolean,
      default: false,
    },
    settingName: {
      type: String,
      default: ''
    },
  },
  data: () => ({
    sizeColumn: null,
  }),
  computed: {
    ...mapGetters(['navigationDrawerStatus']),
    size: function () { return this.navigationDrawerStatus(router.currentRoute.name) ? this.sizeColumn?.value : 0 }
  },
  mounted() {
    this.sizeColumn = new UserSetting(`size-${router.currentRoute.name}${this.settingName}`, 30)
    if (this.shadowEffect)
      this.$refs.ResSplitPane.$children[0].$el.className += ' split-shadow-effect'
  },
}
</script>

<style scoped>
.split-panel {
  position: static;
}
.split-column {
  height: 100%;
}
</style>