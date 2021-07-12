<template>
  <ResSplitPane
    split-to="columns"
    :allow-resize="true"
    :min-size="35"
    :max-size="65"
    :size="sizeMenuColumn"
    :resizerBorderThickness="1"
    :resizerThickness="1"
    v-on:update:size="sizeMenuColumn = $event"
    units="percents">
    <v-col slot="firstPane" class="pa-0 column-settings">
      <treeView
        :treeViewItems="treeView"
        :selectedTreeViewItem="selectedItem"
        @changeSelectedTreeViewItem="changeSelectedTreeViewItem(transformSelectedScript($event))"
        class="overflow-y-auto tree-view"
      ></treeView>
    </v-col>

    <v-col slot="secondPane" class="pa-0 column-settings overflow-hidden">
      <block-header :text-header="textHeaderSettings"></block-header>
      <v-divider></v-divider>
      <v-scroll-y-transition mode="out-in">
        <div v-if="'id' in selectedItem" :key="selectedItem.id" class="pa-4 py-1">
          <settingsAnalytics
            v-for="variable in selectedItem.variables"
            :variable="variable"
          ></settingsAnalytics>

          <div class="text-center">
            <v-btn
              @click="executeScript(selectedItem)"
              color="teal"
              outlined
            >Выполнить скрипт</v-btn>
          </div>
        </div>
      </v-scroll-y-transition>
    </v-col>
  </ResSplitPane>
</template>

<script>
import { mapActions } from 'vuex'
import treeView from '../Map/MapMenu/treeView'
import settingsAnalytics from '../Map/MapMenu/settingsAnalytics'
import blockHeader from '../Map/MapMenu/blockHeader'
import CreatorTreeView from '../Map/MapMenu/Mixins/CreatorTreeView'
import ExecutorScripts from '../Map/MapMenu/Mixins/ExecutorScripts'
import SelectedScriptFormatter from '../Map/MapMenu/Mixins/SelectedScriptFormatter'
import ResSplitPane from 'vue-resize-split-pane'

export default {
  name: 'reportScriptMenu',
  mixins: [CreatorTreeView, ExecutorScripts, SelectedScriptFormatter],
  components: { treeView, settingsAnalytics, blockHeader, ResSplitPane },
  methods: {
    ...mapActions(['changeSelectedTreeViewItem'])
  },
  computed: {
    textHeaderSettings () {
      return 'id' in this.selectedItem ? 'Настройки ' + this.selectedItem.name : 'Выберете скрипт'
    }
  }
}
</script>

<style scoped>
  .tree-view {
    max-height: 95%;
  }
  .column-settings {
    max-height:100%;
    display: flex;
    flex-direction: column;
  }
  .navigation-drawer {
    will-change: auto; /*will-change поставить auto, чтобы не было дрожания объектов*/
    width: 50% !important;
  }
  ::-webkit-scrollbar {
    width: 10px;
  }
  ::-webkit-scrollbar-track {
    background: #FFFFFF;
  }
  ::-webkit-scrollbar-thumb {
    background : rgba(0, 0, 0, .1);
    border-radius : 4px;
  }
</style>
