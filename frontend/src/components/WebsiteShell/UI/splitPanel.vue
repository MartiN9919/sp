<template>
  <ResSplitPane
      ref="ResSplitPane"
      split-to="columns"
      :allow-resize="true"
      :min-size="15"
      :max-size="85"
      :resizerBorderThickness="1"
      :resizerThickness="1"
      :size="drawer ? sizeColumn : 0"
      v-on:update:size="sizeColumn = $event"
      units="percents"
      class="split-panel"
  >
    <v-col :id="name + '1'" class="pa-0 splitColumn" slot="firstPane">
      <slot name="firstPane"></slot>
    </v-col>
    <v-col :id="name + '2'" class="pa-0 splitColumn" slot="secondPane">
      <slot name="secondPane"></slot>
    </v-col>
  </ResSplitPane>
</template>

<script>
import router from '@/router'
import ResSplitPane from 'vue-resize-split-pane'
import NavigationDrawer from "../Mixins/NavigationDrawer"

export default {
  name: "splitPanel",
  components: { ResSplitPane, },
  mixins: [ NavigationDrawer, ],
  props: {
    shadowEffect: {
      type: Boolean,
      default: false,
    }
  },
  data: () => ({
    sizeColumn: 30,
    name: null
  }),
  mounted() {
    this.name = this.$refs.ResSplitPane.$parent.$parent.$options.name
    if (localStorage['size' + router.currentRoute.name + this.name]) {
      this.sizeColumn = parseInt(localStorage['size' + router.currentRoute.name + this.name])
    }
    if (this.shadowEffect)
      this.$refs.ResSplitPane.$children[0].$el.className += ' shadow-effect'
  },
  watch: {
    sizeColumn (newSizeColumn) {
      localStorage['size' + router.currentRoute.name + this.name] = newSizeColumn
    }
  },
}
</script>

<style scoped>
.split-panel {
  position: static;
}
.splitColumn {
  height: 100%;
}
</style>