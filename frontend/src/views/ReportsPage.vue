<template>
  <split-panel shadow-effect>
    <template v-slot:firstPane>
      <report-script-menu id="report-splitter"/>
    </template>
    <template v-slot:secondPane>
      <reports-list/>
    </template>
  </split-panel>
</template>

<script>
import SplitPanel from "@/components/WebsiteShell/CustomComponents/splitPanel"
import reportsList from '@/components/Report/reportsList'
const reportScriptMenu = () => import('@/components/Report/reportScriptMenu')

export default {
  name: 'Report',
  components: { SplitPanel, reportScriptMenu, reportsList},
}
</script>
