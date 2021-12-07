<template>
  <ResSplitPane
    ref="EditorSplit"
    split-to="columns"
    units="percents"
    class="split-panel"
    :allow-resize="true"
    :min-size="20"
    :max-size="60"
    :resizerBorderThickness="1"
    :resizerThickness="1"
    :size="pos.value"
    v-on:update:size="pos.value = $event"
  >
    <v-col class="pa-0 split-column" slot="firstPane">
      <slot name="firstPane"></slot>
    </v-col>
    <v-col class="pa-0 split-column" slot="secondPane">
      <slot name="secondPane"></slot>
    </v-col>
  </ResSplitPane>
</template>

<script>
import router from '@/router'
import UserSetting from "@/store/addition"
import ResSplitPane  from 'vue-resize-split-pane'

export default {
  name: 'EditorSplit',
  components: { ResSplitPane, },
  data: () => ({
    pos : new UserSetting('EditorSplit_pos', 40),
  }),
  mounted () {
    this.$refs.EditorSplit.$children[1].$el.classList.add('split-shadow-effect')
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
  /* полоса прокрутки tree */
  /* div::v-deep div.Pane.column:first-of-type { overflow: auto!important; } */

  /* исправить перекрытие сепаратора второй панелью */
  /* div::v-deep span.Resizer.columnsres { height: auto!important; } */

</style>