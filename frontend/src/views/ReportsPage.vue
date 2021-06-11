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
    resizer-border-thickness=""
    units="percents">
    <v-col class="pa-0" slot="firstPane">
      <reportScriptMenu></reportScriptMenu>
    </v-col>
    <v-col class="pa-0 select_off" slot="secondPane">
      <reportsList :drawer="drawer"></reportsList>
    </v-col>
  </ResSplitPane>
</template>

<script>
import reportScriptMenu from '../components/Report/reportScriptMenu'
import reportsList from '../components/Report/reportsList'
import ResSplitPane from "vue-resize-split-pane";
import NavigationDrawer from "../components/NavigationDrawer/Mixins/NavigationDrawer";

export default {
  name: 'ReportsPage',
  components: { reportScriptMenu, reportsList, ResSplitPane },
  mixins: [NavigationDrawer],
}
</script>

<style>

</style>
