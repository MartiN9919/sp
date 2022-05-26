<template>
  <split-panel id="report-menu-splitter" parent-name="report-splitter" setting-name="Menu">
    <template v-slot:firstPane>
      <v-text-field v-model="search" placeholder="Поиск по скриптам" solo hide-details dense class="px-2 pt-2"/>
      <treeView
        :items="treeView"
        :selected="selectedItem"
        @change="changeSelectedTreeViewItem(transformSelectedScript($event))"
        class="overflow-y-auto tree-view"
      ></treeView>
    </template>

    <template v-slot:secondPane>
      <v-scroll-y-transition mode="out-in">
        <div
            v-if="selectedItem.hasOwnProperty('id')"
            :key="selectedItem.refresh"
            class="px-2 pb-1 overflow-y-auto h-100"
        >
          <custom-tooltip
              v-for="(v, key) in selectedItem.variables"
              :key="selectedItem.id + key"
              :description="v.hint"
              :value="v.value"
              :type="v.type"
              is-description
              nudge-right="20"
              right
          >
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
        </div>
      </v-scroll-y-transition>
    </template>
  </split-panel>
</template>

<script>
import { mapActions } from 'vuex'
import treeView from '../Map/MapMenu/scriptsPage/treeView'
import ResponsiveInputForm from '@/components/WebsiteShell/CustomComponents/responsiveInputForm'
import CreatorTreeView from '@/components/Map/MapMenu/Mixins/CreatorTreeView'
import ExecutorScripts from '@/components/Map/MapMenu/Mixins/ExecutorScripts'
import SelectedScriptFormatter from '@/components/Map/MapMenu/Mixins/SelectedScriptFormatter'
import SplitPanel from "@/components/WebsiteShell/CustomComponents/splitPanel"
import CustomTooltip from "@/components/WebsiteShell/CustomComponents/Tooltip/customTooltip"

export default {
  name: 'reportScriptMenu',
  mixins: [CreatorTreeView, ExecutorScripts, SelectedScriptFormatter],
  components: {SplitPanel, treeView, ResponsiveInputForm, CustomTooltip},
  methods: mapActions(['changeSelectedTreeViewItem']),
}
</script>

<style scoped>
  .tree-view {
    height: calc(100% - 46px);
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
