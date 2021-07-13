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
  >
    <v-col slot="firstPane" class="column-settings pa-0">
      <treeView
        :treeViewItems="treeView"
        :selectedTreeViewItem="selectedItem"
        @changeSelectedTreeViewItem="setSelectedTreeViewItem"
        class="tree-view overflow-y-auto my-1"
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

      <v-row no-gutters class="overflow-y-auto py-3 px-2">
        <chipAnalytics
          v-for="(analytics, id) in selectedTemplate.activeAnalysts.concat(selectedTemplate.passiveAnalysts)"
          :analytics="analytics"
          :key="id"
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
          <block-header :text-header="'Настройки ' + selectedItem.name" class="pb-3"></block-header>
          <v-tooltip
            v-for="variable in selectedItem.variables" :key="variable.id"
            bottom nudge-bottom="-20" z-index="10001"
            transition="false" color="#00796B" max-width="20%"
          >
            <template v-slot:activator="{ on }">
              <div v-on="on" class="mb-5">
                <settingsAnalytics
                  v-model="variable.value" :variable="variable"
                  :type="variable.type" :title="variable.title"
                ></settingsAnalytics>
              </div>

            </template>
            <p class="text-formatter-for-window-size additional-text text-justify ma-0">
              {{variable.hint ? variable.hint : 'Описание отсутствует'}}
            </p>
          </v-tooltip>

          <div class="text-center pt-2">
            <v-btn
              @click="executeScript(selectedItem)"
              outlined color="#00796B" class="mx-2 mb-2"
            >Выполнить</v-btn>
            <v-btn
              :disabled="selectedTemplate.passiveAnalysts.indexOf(selectedItem) !== -1"
              @click="disabledActiveAnalysts()"
              outlined color="#00796B" class="mx-2 mb-2"
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
import treeView from './treeView'
import chipAnalytics from './chipAnalytics'
import settingsAnalytics from './settingsAnalytics'
import menuTemplate from './menuTemplate'
import blockHeader from './blockHeader'
import CreatorTreeView from './Mixins/CreatorTreeView'
import ExecutorScripts from './Mixins/ExecutorScripts'
import SelectedScriptFormatter from './Mixins/SelectedScriptFormatter'

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
</style>
