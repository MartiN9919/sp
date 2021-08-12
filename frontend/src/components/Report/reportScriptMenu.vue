<template>
  <split-panel>
    <template v-slot:firstPane>
      <treeView
        :treeViewItems="treeView"
        :selectedTreeViewItem="selectedItem"
        @changeSelectedTreeViewItem="changeSelectedTreeViewItem(transformSelectedScript($event))"
        class="overflow-y-auto tree-view"
      ></treeView>
    </template>

    <template v-slot:secondPane>
      <block-header :text-header="textHeaderSettings"></block-header>
      <v-divider></v-divider>
      <v-scroll-y-transition mode="out-in">
        <div v-if="'id' in selectedItem" :key="selectedItem.id" class="pa-4 py-1">
          <responsive-input-form
            v-for="(variable, key) in selectedItem.variables" :key="key"
            :variable="variable"
          ></responsive-input-form>

          <div class="text-center">
            <v-btn
              @click="executeScript(selectedItem)"
              color="teal"
              outlined
            >Выполнить скрипт</v-btn>
          </div>
        </div>
      </v-scroll-y-transition>
    </template>
  </split-panel>
</template>

<script>
import { mapActions } from 'vuex'
import treeView from '../Map/MapMenu/scriptsPage/treeView'
import ResponsiveInputForm from '../WebsiteShell/UI/responsiveInputForm'
import blockHeader from '../Map/MapMenu/scriptsPage/blockHeader'
import CreatorTreeView from '../Map/MapMenu/Mixins/CreatorTreeView'
import ExecutorScripts from '../Map/MapMenu/Mixins/ExecutorScripts'
import SelectedScriptFormatter from '../Map/MapMenu/Mixins/SelectedScriptFormatter'
import SplitPanel from "../WebsiteShell/UI/splitPanel"

export default {
  name: 'reportScriptMenu',
  mixins: [CreatorTreeView, ExecutorScripts, SelectedScriptFormatter],
  components: {SplitPanel, treeView, ResponsiveInputForm, blockHeader, },
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
