<template>
  <ResSplitPane
    style="height:auto; overflow: auto; position: inherit; "
    split-to="columns"
    units="percents"
    :allow-resize="true"
    :min-size="20"
    :max-size="50"
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
import router from '@/router'
import { mapActions, mapGetters } from 'vuex'
import ResSplitPane  from 'vue-resize-split-pane'

export default {
  name: 'EditorSplit',
  components: { ResSplitPane, },
  data: () => ({
    split_storage_name: undefined,
    split_pos: 30,
  }),
  mounted () {
    this.split_storage_name = router.currentRoute.name + '_editor_splitter_pos'
    if (localStorage[this.split_storage_name]) {
      this.split_pos = parseInt(localStorage[this.split_storage_name])
    }
    //document.getElementsByClassName('column')[0].classList.add('shadow-effect')
  },
  watch: {
    split_pos (newSize) {
      localStorage[this.split_storage_name] = newSize
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
  div::v-deep div.Pane.column:first-of-type { overflow: auto!important; }

  /* исправить перекрытие сепаратора второй панелью */
  div::v-deep span.Resizer.columnsres { height: auto!important; }

</style>