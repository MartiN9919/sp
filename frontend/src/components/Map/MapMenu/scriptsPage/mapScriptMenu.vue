<template>
  <split-panel id="map-menu-splitter" parent-name="map-splitter" setting-name="Menu">
    <template v-slot:firstPane>
      <v-text-field v-model="search" placeholder="Поиск по скриптам" solo hide-details dense class="px-2 pt-2"/>
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
          @get="getSelectedTemplate"
          @create="createTemplate"
          @put="putTemplate"
          @save="saveTemplate"
          @remove="deleteSelectedTemplate"
          @changeTitle="changeSelectedTemplateTitle"
          class="px-2 pt-2"
        ></menuTemplate>

        <div class="d-flex flex-column overflow-y-hidden h-100">
          <v-row no-gutters class="pa-1 overflow-y-auto">
            <chipAnalytics
              v-for="(analytics, key) in analysts"
              :analytics="analytics"
              :key="analytics.refresh + key"
              :active="selectedTemplate.activeAnalysts.includes(analytics)"
              :selectedTreeViewItem="selectedItem"
              @disabled="disabledAnalysts"
              @activate="executeScript"
              @select="setCurrentAnalytics"
              @changeColor="changeColorActiveAnalysts"
              @delete="deleteAnalytics"
            ></chipAnalytics>
          </v-row>
          <v-divider v-if="'id' in selectedItem"></v-divider>

          <v-scroll-y-transition mode="out-in">
            <v-form
                ref="form"
                v-if="'id' in selectedItem"
                :key="selectedItem.refresh"
                class="px-2 py-1 overflow-y-auto"
                onSubmit="return false;"
            >
              <custom-tooltip
                  v-for="(v, key) in selectedItem.variables"
                  :key="selectedItem.id + key"
                  :body-text="v.hint"
                  bottom
              >
                <template v-slot:activator="{ on }">
                  <div v-on="on" class="pt-1">
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
            </v-form>
          </v-scroll-y-transition>
        </div>
      </div>
    </template>
  </split-panel>
</template>

<script>
import treeView from '@/components/Map/MapMenu/scriptsPage/treeView'
import chipAnalytics from '@/components/Map/MapMenu/scriptsPage/chipAnalytics'
import menuTemplate from '@/components/Map/MapMenu/scriptsPage/menuTemplate'
import CreatorTreeView from '@/components/Map/MapMenu/Mixins/CreatorTreeView'
import ExecutorScripts from '@/components/Map/MapMenu/Mixins/ExecutorScripts'
import SelectedScriptFormatter from '@/components/Map/MapMenu/Mixins/SelectedScriptFormatter'
import ResponsiveInputForm from '@/components/WebsiteShell/CustomComponents/responsiveInputForm'
import CustomTooltip from "@/components/WebsiteShell/CustomComponents/customTooltip"
import SplitPanel from "@/components/WebsiteShell/CustomComponents/splitPanel"
import { MAP_CONST } from '@/components/Map/Leaflet/Lib/Const'
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'mapScriptMenu',
  mixins: [CreatorTreeView, ExecutorScripts, SelectedScriptFormatter],
  components: {SplitPanel, CustomTooltip, treeView, chipAnalytics, ResponsiveInputForm, menuTemplate},
  computed: {
    ...mapGetters(['templatesList', 'selectedTemplate']),
    /**
     * Список всех скриптов (Активные и деактивированные)
     * @returns []
     */
    analysts: function () {
      return this.selectedTemplate.activeAnalysts.concat(this.selectedTemplate.passiveAnalysts)
    }
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

    /** Деактивация аналитики (удаление имеющихся результатов выполнения скрипта) */
    disabledAnalysts (analytics) {
      /** Удаление аналитики из списка активных аналитик шаблона */
      this.removeAnalytics(analytics)
      /** Добавление цвета "пассивной" аналитики */
      analytics.color = MAP_CONST.COLOR.SCRIPT_OFF
      /** Удаление имеющихся результатов выполнения скрипта */
      delete analytics.result
      /** Занесение аналитики на шину в переменную selectedTemplate.passiveAnalysts */
      this.addPassiveAnalysts(analytics)
    },

    /** Подготовка шаблона к сохранению/изменению */
    templatePreparation (title) {
      /** Присваивание заголовка шаблону */
      this.changeSelectedTemplateTitle(title)
      /** Удаление имеющихся результатов из активных аналитик шаблона */
      this.selectedTemplate.activeAnalysts.forEach(script => delete script.fc)
    },

    /** Сохранение шаблона без имеющихся результатов */
    saveTemplate (title) {
      this.templatePreparation(title)
      /** Сохранение шаблона */
      this.saveSelectedTemplate({selectedTemplate: this.selectedTemplate, config: {}})
    },

    /** Изменение шаблона без имеющихся результатов */
    putTemplate (title) {
      this.templatePreparation(title)
      /** Изменение шаблона */
      this.putSelectedTemplate({selectedTemplate: this.selectedTemplate, config: {}})
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
  height: calc(100% - 46px);
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
