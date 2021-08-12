<template>
  <ResSplitPane
    ref="EditorSplit"
    style="height:auto; overflow: auto; position: inherit; "
    split-to="columns"
    units="percents"
    :allow-resize="true"
    :min-size="20"
    :max-size="60"
    :resizerBorderThickness="1"
    :resizerThickness="1"
    :size="split_visible ? split_pos : 0"
    v-on:update:size="split_pos = $event"
  >
    <v-col class="pa-0" slot="firstPane">
      <slot name="firstPane"></slot>
    </v-col>
    <v-col class="pa-0" slot="secondPane">
      <slot name="secondPane"></slot>
    </v-col>
  </ResSplitPane>
</template>

<script>
// import { mapActions, mapGetters } from 'vuex'
import router from '@/router'
import ResSplitPane  from 'vue-resize-split-pane'

export default {
  name: 'EditorSplit',
  props: {
    keySave: { type: String, default() { return '' } },
  },
  components: { ResSplitPane, },
  data: () => ({
    split_key: undefined,
    split_pos: 30,
  }),
  mounted () {
    this.split_key = router.currentRoute.name + '_editor_splitter_' + this.keySave+'_pos'
    if (localStorage[this.split_key]) {
      this.split_pos = parseInt(localStorage[this.split_key])
    }
    this.$refs.EditorSplit.$children[1].$el.classList.add('shadow-effect')
  },
  watch: {
    split_pos (newSize) {
      localStorage[this.split_key] = newSize
    },
  },
  computed: {
    //...mapGetters(['navigationDrawerStatus']),

    split_visible: {
      get: function () {
        return true //this.navigationDrawerStatus(router.currentRoute.name)
      },
      set: function (val) {
        //if (val !== this.navigationDrawerStatus(router.currentRoute.name)) { this.changeNavigationDrawerStatus() }
      }
    }
  },
  methods: {
  //  ...mapActions(['changeNavigationDrawerStatus']),
  },
}

</script>

<style scoped>

  /* полоса прокрутки tree */
  /* div::v-deep div.Pane.column:first-of-type { overflow: auto!important; } */

  /* исправить перекрытие сепаратора второй панелью */
  /* div::v-deep span.Resizer.columnsres { height: auto!important; } */

</style>