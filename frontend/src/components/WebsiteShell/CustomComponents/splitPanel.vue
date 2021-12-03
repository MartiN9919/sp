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
      v-on:update:size="sizeColumn = $event"
      units="percents"
      class="split-panel"
  >
    <v-col :id="name + '1'" class="pa-0 split-column" slot="firstPane">
      <slot name="firstPane"></slot>
    </v-col>
    <v-col :id="name + '2'" class="pa-0 split-column" slot="secondPane">
      <slot name="secondPane"></slot>
    </v-col>
  </ResSplitPane>
</template>

<script>
import router from '@/router'
import {mapGetters} from "vuex"
import ResSplitPane from 'vue-resize-split-pane'

export default {
  name: "splitPanel",
  components: {ResSplitPane},
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
  computed: {
    ...mapGetters(['navigationDrawerStatus']),
    size: function () { return this.navigationDrawerStatus(router.currentRoute.name) ? this.sizeColumn : 0 }
  },
  mounted() {
    this.name = this.$refs.ResSplitPane.$parent.$parent.$options.name
    if (localStorage['size' + router.currentRoute.name + this.name])
      this.sizeColumn = parseInt(localStorage['size' + router.currentRoute.name + this.name])
    if (this.shadowEffect)
      this.$refs.ResSplitPane.$children[0].$el.className += ' split-shadow-effect'
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
.split-column {
  height: 100%;
}
</style>