<template>
  <split-panel split-shadow-effect>
    <template v-slot:firstPane>
      <report-script-menu/>
    </template>
    <template v-slot:secondPane>
      <reports-list/>
    </template>
  </split-panel>
</template>

<script>
import SplitPanel from "@/components/WebsiteShell/CustomComponents/splitPanel"
import reportsList from '@/components/Report/reportsList'
import reportScriptMenu from '@/components/Report/reportScriptMenu'

export default {
  name: 'Reports',
  components: { SplitPanel, reportScriptMenu, reportsList},
}
</script>
