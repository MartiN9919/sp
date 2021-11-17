<template>
  <split-panel>
    <template v-slot:firstPane>
      <treeView
        :items="treeView"
        :selected="selectedItem"
        @change="setSelectedItem"
        class="tree-view"
      ></treeView>
    </template>

    <template v-slot:secondPane>
      <div class="second-column">
        <menuTemplate
          :templates="templatesList"
          :selectedTemplate="selectedTemplate"
          @getTemplate="getSelectedTemplate({ params: { template_id: $event } })"
          @changeTitle="changeSelectedTemplateTitle"
          @deleteTemplate="deleteSelectedTemplate"
          @saveTemplate="saveTemplate"
          @createNewTemplate="createTemplate"
          class="px-2 pt-2"
        ></menuTemplate>
        <v-row no-gutters class="overflow-y-auto pa-1 chip-analytics">
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
        <v-divider v-if="'id' in selectedItem"></v-divider>

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
                :disabled="selectedTemplate.passiveAnalysts.includes(selectedItem)"
                @click="disabledActiveAnalysts()"
                outlined color="#00796B"
              >Отключить</v-btn>
              <v-spacer></v-spacer>
              <v-btn
                @click="executeScript(selectedItem)"
                outlined color="#00796B"
              >Выполнить</v-btn>
            </div>
          </v-form>
        </v-scroll-y-transition>
      </div>
    </template>
  </split-panel>
</template>

<script>
import treeView from './treeView'
import chipAnalytics from './chipAnalytics'
import ResponsiveInputForm from '../../../WebsiteShell/UI/responsiveInputForm'
import menuTemplate from './menuTemplate'
import blockHeader from './blockHeader'
import CreatorTreeView from '../Mixins/CreatorTreeView'
import ExecutorScripts from '../Mixins/ExecutorScripts'
import SelectedScriptFormatter from '../Mixins/SelectedScriptFormatter'
import CustomTooltip from "../../../WebsiteShell/UI/customTooltip"
import SplitPanel from "../../../WebsiteShell/UI/splitPanel"
import { mapActions, mapGetters } from 'vuex'
import { MAP_CONST } from '@/components/Map/Leaflet/Lib/Const';

export default {
  name: 'mapScriptMenu',
  mixins: [CreatorTreeView, ExecutorScripts, SelectedScriptFormatter],
  components: {SplitPanel, CustomTooltip, treeView, chipAnalytics, ResponsiveInputForm, menuTemplate, blockHeader},
  computed: mapGetters(['templatesList', 'selectedTemplate']),
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
    setSelectedItem (script) {
      /**
       * transformSelectedScript - функция миксина [Mixins.SelectedScriptFormatter]
       * @type {Object} {id: *, name: *, variables: {title: *, value: *}}
       */
      const transformedScript = this.transformSelectedScript(script)
      /** Добавление цвета "пассивной" аналитики */
      transformedScript.color = MAP_CONST.COLOR.SCRIPT_OFF
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
      this.selectedItem.color = MAP_CONST.COLOR.SCRIPT_OFF
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
      for (const script of scriptForRequest.activeAnalysts) { delete script.fc }
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
  height: 100%;
  overflow-y: auto;
}
.chip-analytics {
  flex: auto;
}
.second-column {
  max-height: 100%;
  display: flex;
  flex-direction: column;
}
</style>
