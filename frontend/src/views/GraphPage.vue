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
      <graph-menu></graph-menu>
    </v-col>
    <v-col class="pa-0" slot="secondPane">
      <d3-field :drawer="drawer"></d3-field>

    </v-col>
  </ResSplitPane>
</template>

<script>
import ResSplitPane from "vue-resize-split-pane";
import NavigationDrawer from "../components/NavigationDrawer/Mixins/NavigationDrawer";
import d3Field from "../components/Graph/d3Field";
import graphMenu from "../components/Graph/graphMenu";

export default {
  name: 'GraphPage',
  components: { ResSplitPane, d3Field, graphMenu,},
  mixins: [NavigationDrawer],
}
</script>

<style >

</style>
