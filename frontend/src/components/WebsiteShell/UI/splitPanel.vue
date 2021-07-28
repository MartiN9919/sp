<template>
  <ResSplitPane
      split-to="columns"
      :allow-resize="true"
      :min-size="15"
      :max-size="85"
      :resizerBorderThickness="1"
      :resizerThickness="1"
      :size="drawer ? sizeNavigation : 0"
      v-on:update:size="sizeNavigation = $event"
      units="percents">
    <v-col class="pa-0" slot="firstPane">
      <slot name="firstPane"></slot>
    </v-col>
    <v-col class="pa-0" slot="secondPane">
      <slot name="secondPane"></slot>
    </v-col>
  </ResSplitPane>
</template>

<script>
import ResSplitPane from 'vue-resize-split-pane'
import NavigationDrawer from "../Mixins/NavigationDrawer"

export default {
  name: "splitPanel",
  components: { ResSplitPane, },
  mixins: [NavigationDrawer, ],
}
</script>

<style scoped>

</style>