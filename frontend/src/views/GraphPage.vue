<template>
  <ResSplitPane
    v-on:update:size="sizeNavigation = $event"
    split-to="columns" :allow-resize="true" units="percents"
    :min-size="15" :max-size="85" :size="drawer ? sizeNavigation : 0"
    :resizerBorderThickness="1" :resizerThickness="1" resizer-border-thickness="">
    <graph-menu slot="firstPane"></graph-menu>
    <work-place slot="secondPane" :drawer="drawer"></work-place>
  </ResSplitPane>
</template>

<script>
import workPlace from '../components/Graph/Graph/workPlace'
import graphMenu from '../components/Graph/GraphMenu/graphMenu'
import NavigationDrawer from '../components/WebsiteShell/Mixins/NavigationDrawer'
import ResSplitPane from 'vue-resize-split-pane'

export default {
  name: 'GraphPage',
  mixins: [ NavigationDrawer, ],
  components: { ResSplitPane, workPlace, graphMenu,},
  created() { this.$store.dispatch('getListOfPrimaryObjects') },
}
</script>

<style >

</style>
