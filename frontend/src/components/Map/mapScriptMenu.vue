<template>
  <ResSplitPane
    split-to="columns"
    :allow-resize="true"
    :min-size="15"
    :max-size="85"
    :size="sizeMenuColumn"
    :resizerBorderThickness="1"
    :resizerThickness="1"
    v-on:update:size="sizeMenuColumn = $event"
    units="percents"
    oncontextmenu="return false"
  >
    <v-col slot="firstPane" class="column-settings pa-0">
      <treeView
        :treeViewItems="treeView"
        :selectedTreeViewItem="selectedItem"
        @changeSelectedTreeViewItem="setSelectedTreeViewItem"
        class="tree-view overflow-y-auto"
      ></treeView>
    </v-col>

    <v-col slot="secondPane" class="column-settings overflow-hidden pa-0">
      <block-header :text-header="'Выбранные скрипты'"></block-header>
      <v-divider></v-divider>
      <menuTemplate
        :templates="templatesList"
        :selectedTemplate="selectedTemplate"
        @getTemplate="getSelectedTemplate({ params: { template_id: $event } })"
        @changeTitle="changeSelectedTemplateTitle"
        @deleteTemplate="deleteSelectedTemplate"
        @saveTemplate="saveTemplate"
        @createNewTemplate="createTemplate"
      ></menuTemplate>

      <v-divider
          v-if="selectedTemplate.activeAnalysts.length || selectedTemplate.passiveAnalysts.length"
      ></v-divider>

      <v-row no-gutters class="overflow-y-auto pa-3">
        <chipAnalytics
          v-for="analytics in selectedTemplate.activeAnalysts.concat(selectedTemplate.passiveAnalysts)"
          :analytics="analytics"
          :selectedTreeViewItem="selectedItem"
          @returnSelectAnalytics="setCurrentAnalytics"
          @changeColor="changeColorActiveAnalysts"
          @deleteActiveAnalytics="deleteAnalytics"
        ></chipAnalytics>
      </v-row>

      <v-divider
        v-if="selectedTemplate.activeAnalysts.length || selectedTemplate.passiveAnalysts.length && 'id' in selectedItem"
      ></v-divider>

      <v-scroll-y-transition mode="out-in">
        <div v-if="'id' in selectedItem" :key="selectedItem.id" class="pa-4 py-1">
          <block-header :text-header="'Настройки ' + selectedItem.name"></block-header>
          <settingsAnalytics
            v-for="variable in selectedItem.variables"
            :variable="variable"
          ></settingsAnalytics>

          <div class="text-center">
            <v-btn
              @click="executeScript(selectedItem)"
              outlined
              color="teal"
              class="mx-2 mb-2"
            >Выполнить</v-btn>
            <v-btn
              :disabled="selectedTemplate.passiveAnalysts.indexOf(selectedItem) !== -1"
              @click="disabledActiveAnalysts()"
              outlined
              color="teal"
              class="mx-2 mb-2"
            >Отключить</v-btn>
          </div>
        </div>
      </v-scroll-y-transition>
    </v-col>
  </ResSplitPane>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import ResSplitPane from 'vue-resize-split-pane'
import treeView from '../NavigationDrawer/ConstructorBlocks/treeView'
import chipAnalytics from '../NavigationDrawer/ConstructorBlocks/chipAnalytics'
import settingsAnalytics from '../NavigationDrawer/ConstructorBlocks/settingsAnalytics'
import menuTemplate from '../NavigationDrawer/ConstructorBlocks/menuTemplate'
import blockHeader from '../NavigationDrawer/ConstructorBlocks/blockHeader'
import CreatorTreeView from '../NavigationDrawer/Mixins/CreatorTreeView'
import ExecutorScripts from '../NavigationDrawer/Mixins/ExecutorScripts'
import SelectedScriptFormatter from '../NavigationDrawer/Mixins/SelectedScriptFormatter'

export default {
  name: 'mapScriptMenu',
  mixins: [CreatorTreeView, ExecutorScripts, SelectedScriptFormatter],
  components: { treeView, chipAnalytics, settingsAnalytics, menuTemplate, ResSplitPane, blockHeader },
  computed: {
    ...mapGetters(['templatesList', 'selectedTemplate'])
  },
  methods: {
    ...mapActions([
      'addPassiveAnalysts', 'changeSelectedTreeViewItem', 'changeSelectedTemplateTitle', 'changeColorActiveAnalysts',
      'removeAnalytics', 'createNewTemplate', 'getTemplatesList', 'deleteSelectedTemplate', 'saveSelectedTemplate',
      'putSelectedTemplate', 'getSelectedTemplate'
    ]),

    /**
     * Обработка выбора скрипта в дереве скриптов [ConstructorBlocks.treeView]
     * @param {Object} script - Глубокая копия выбранного пользователем скрипта
     */
    setSelectedTreeViewItem (script) {
      /**
       * transformSelectedScript - функция миксина [Mixins.SelectedScriptFormatter]
       * @type {Object} {id: *, name: *, variables: {title: *, value: *}}
       */
      const transformedScript = this.transformSelectedScript(script)
      /** Добавление цвета "пассивной" аналитики */
      transformedScript.color = '#696969FF'
      /** Занесение преобразованной копии скрипта на шину в переменную selectedTreeViewItemMap */
      this.changeSelectedTreeViewItem(transformedScript)
      /** Занесение преобразованной копии скрипта на шину в переменную selectedTemplate.passiveAnalysts */
      this.addPassiveAnalysts(transformedScript)
    },

    /**
     * Обработка выбора аналитики из списка активных или пассивных аналитик шаблона [ConstructorBlocks.chipAnalytics]
     * @param {Object} analytics - Выбранная аналитика
     */
    setCurrentAnalytics (analytics) {
      /** Проверка активации аналитики */
      if (this.selectedItem !== analytics)
      /** Если аналитика не активна, то добавление ее на шину в переменную selectedTreeViewItemMap */
      { this.changeSelectedTreeViewItem(analytics) }
      /** Деактивация аналитики (очистка selectedTreeViewItemMap на шине) */
      else this.changeSelectedTreeViewItem()
    },

    /**
     * Удаление аналитики из списка активных или пассивных аналитик шаблона [ConstructorBlocks.chipAnalytics]
     * @param {Object} analytics - Выбранная аналитика
     */
    deleteAnalytics (analytics) {
      /** Удаление аналитики из списка активных или пассивных аналитик шаблона */
      this.removeAnalytics(analytics)
      /** Деактивация аналитики (очистка selectedTreeViewItemMap на шине) при необходимости */
      this.changeSelectedTreeViewItem()
    },

    /** Деактивация активной аналитики (удаление имеющися результатов выполнения скрипта) */
    disabledActiveAnalysts () {
      /** Удаление аналитики из списка активных аналитик шаблона */
      this.removeAnalytics(this.selectedItem)
      /** Добавление цвета "пассивной" аналитики */
      this.selectedItem.color = '#696969FF'
      /** Удаление имеющися результатов выполнения скрипта */
      delete this.selectedItem.result
      /** Занесение аналитки на шину в переменную selectedTemplate.passiveAnalysts */
      this.addPassiveAnalysts(this.selectedItem)
    },

    /** Сохранение или пересохранение шаблона без имеющихся результатов */
    saveTemplate () {
      /** Создание глубокой копии шаблона */
      const scriptForRequest = JSON.parse(JSON.stringify(this.selectedTemplate))
      /** Удаление имеющихся результатов из активных аналитик шаблона */
      for (const script of scriptForRequest.activeAnalysts) { delete script.result }
      /** Проверка на сохранение, либо пересохранение шаблона */
      if ('id' in scriptForRequest)
        this.putSelectedTemplate({ selectedTemplate: scriptForRequest, config: {} })
      else this.saveSelectedTemplate({ selectedTemplate: scriptForRequest, config: {} })
    },

    /** Создание нового шаблона */
    createTemplate () {
      /** Деактивация аналитики (очистка selectedTreeViewItemMap на шине) при необходимости */
      this.changeSelectedTreeViewItem()
      /** Создание нового "скелета" для шаблона */
      this.createNewTemplate()
    }
  },
  created () {
    /** Получение списка имеющихся шаблонов при создании объекта */
    this.getTemplatesList({})
    /** Также отрабатывает функция getTreeViewItemsFromServer миксина [Mixins.CreatorTreeView] */
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
  ::-webkit-scrollbar {
    width: 10px;
  }
  ::-webkit-scrollbar-track {
    background: #FFFFFF;
  }
  ::-webkit-scrollbar-thumb {
    background : rgba(0, 0, 0, .1);
  }
</style>
