<template>
  <div class="overflow-y-auto h-100">
    <setting-block
      v-for="(setting, key) in listSettings"
      :key="key"
      :icon="setting.icon"
      :title="setting.title"
      :sub-title="setting.subTitle"
    >
      <component :is="setting.component"/>
    </setting-block>
<!--    <trigger-settings :triggers="getTriggers" @setTrigger="setTrigger">-->
<!--      <v-list-item class="px-2">-->
<!--        <selector-object v-model="idTriggerSettings" start-object/>-->
<!--      </v-list-item>-->
<!--    </trigger-settings>-->
  </div>
</template>

<script>
import SettingBlock from "@/components/Graph/GraphMenu/Settings/Modules/SettingBlock"
import ListGlobalSettings from "@/components/Graph/GraphMenu/Settings/Global/ListGlobalSettings"
import ListClassifierSettings from "@/components/Graph/GraphMenu/Settings/Classifier/ListClassifierSettings"
import ListTriggerSettings from "@/components/Graph/GraphMenu/Settings/Trigger/ListTriggerSettings"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "SettingsPage",
  components: {SettingBlock, ListTriggerSettings, ListClassifierSettings, ListGlobalSettings},
  data: () => ({
    listSettings: [
      {
        icon: 'mdi-graph-outline',
        title: 'Общие настройки графа',
        subTitle: 'Настройка отображения связей и объектов на графе',
        component: ListGlobalSettings,
      },
      {
        icon: 'mdi-text-box-outline',
        title: 'Настройки объектов',
        subTitle: 'Настройка отображения классификаторов объекта',
        component: ListClassifierSettings,
      },
      {
        icon: 'mdi-flag-outline',
        title: 'Настройки триггеров',
        subTitle: 'Настройка отслеживаемых свойств',
        component: ListTriggerSettings,
      }
    ],
  }),
  computed: {
    ...mapGetters(['objectTriggers']),
    getTriggers: function() { return this.objectTriggers(this.idTriggerSettings) },
  },
  methods: {
    ...mapActions(['setTriggerState']),
    setTrigger(event) {
      this.setTriggerState(event)
    }
  },
}
</script>