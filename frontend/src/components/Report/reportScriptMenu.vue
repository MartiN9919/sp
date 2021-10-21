<template>
  <split-panel>
    <template v-slot:firstPane>
      <treeView
        :items="treeView"
        :selected="selectedItem"
        @change="changeSelectedTreeViewItem(transformSelectedScript($event))"
        class="overflow-y-auto tree-view"
      ></treeView>
    </template>

    <template v-slot:secondPane>
      <block-header :text-header="textHeaderSettings"></block-header>
      <v-divider></v-divider>
      <v-scroll-y-transition mode="out-in">
          <v-form ref="form" v-if="'id' in selectedItem" class="px-2">
            <custom-tooltip v-for="v in selectedItem.variables" :key="v.id" :body-text="v.hint" bottom>
              <template v-slot:activator="{ on }">
                <div v-on="on" class="pt-2">
                  <responsive-input-form
                    v-model="v.value"
                    :input-type="v.type"
                    :label="v.title"
                    :list-rules="v.necessary ? ['notEmpty'] : []"
                    clearable
                  ></responsive-input-form>
                </div>
              </template>
            </custom-tooltip>
            <div class="py-2 d-flex flex-nowrap flex-row justify-center">
              <v-btn
                @click="executeScript(selectedItem)"
                outlined color="#00796B"
              >Выполнить
              </v-btn>
            </div>
          </v-form>
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
import CustomTooltip from "../WebsiteShell/UI/customTooltip"

export default {
  name: 'reportScriptMenu',
  mixins: [CreatorTreeView, ExecutorScripts, SelectedScriptFormatter],
  components: {SplitPanel, treeView, ResponsiveInputForm, blockHeader, CustomTooltip, },
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
