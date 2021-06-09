<template>
  <ResSplitPane
    split-to="columns"
    :allow-resize="true"
    :min-size="15" :max-size="85"
    :size="drawer ? sizeNavigation : 0"
    v-on:update:size="sizeNavigation = $event"
    :resizerBorderThickness="1" :resizerThickness="1"
    resizer-border-thickness="" units="percents">
    <v-col class="pa-0" slot="firstPane">
      <h1>Hello world!</h1>
    </v-col>
    <v-col class="pa-0" slot="secondPane">
      <h1>Hello world!</h1>
    </v-col>
  </ResSplitPane>
</template>

<script>
import ResSplitPane from "vue-resize-split-pane";
import NavigationDrawer from "../components/NavigationDrawer/Mixins/NavigationDrawer";

export default {
  name: 'GraphPage',
  components: { ResSplitPane },
  mixins: [NavigationDrawer],
}
</script>

<style >

</style>
