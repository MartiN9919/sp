<template>
  <ResSplitPane
      ref="ResSplitPane"
      split-to="columns"
      :allow-resize="true"
      :resizerBorderThickness="5"
      :resizerThickness="1"
      :size="size"
      v-on:update:size="sizeColumn.value = $event"
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
    parentName: {
      type: String,
      default: null
    }
  },
  data: () => ({
    sizeColumn: null,
    parent: null
  }),
  computed: {
    ...mapGetters(['navigationDrawerStatus']),
    size: function () { return this.navigationDrawerStatus(router.currentRoute.name) ? this.sizeColumn?.value : 0 }
  },
  methods: {
    setThresholdValues() {
      if(this.sizeColumn.value > this.parent.clientWidth) {
        this.sizeColumn.value = this.parent.clientWidth - 10
      }
    }
  },
  mounted() {
    this.parent = this.parentName ? document.getElementById(this.parentName) : document.body
    this.sizeColumn = new UserSetting(
        `size-${router.currentRoute.name}${this.settingName}`,
        this.parent.clientWidth / 3
    )
    if (this.shadowEffect)
      this.$refs.ResSplitPane.$children[0].$el.className += ' split-shadow-effect'
    this.setThresholdValues()
    window.addEventListener(`resize`, this.setThresholdValues, false);
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