<template>
  <split-panel shadow-effect>
    <template v-slot:firstPane>
      <reportScriptMenu></reportScriptMenu>
    </template>
    <template v-slot:secondPane>
      <reportsList></reportsList>
    </template>
  </split-panel>
</template>

<script>
import reportScriptMenu from '../components/Report/reportScriptMenu'
import reportsList from '../components/Report/reportsList'
import SplitPanel from "../components/WebsiteShell/UI/splitPanel";

export default {
  name: 'Reports',
  components: { SplitPanel, reportScriptMenu, reportsList},
}
</script>

<style>

</style>
