<template>
  <v-container class="overflow-y-auto pa-0">
    <global-settings
      :settings="globalDisplaySettings"
      @changeSettings="changeGlobalSettingState"
    ></global-settings>
    <object-settings :classifiers="getClassifiers">
      <v-list-item class="px-2">
        <selector-object v-model="idObjectSettings" start-object></selector-object>
      </v-list-item>
    </object-settings>
    <trigger-settings :triggers="getTriggers" @setTrigger="setTrigger">
      <v-list-item class="px-2">
        <selector-object v-model="idTriggerSettings" start-object></selector-object>
      </v-list-item>
    </trigger-settings>
  </v-container>
</template>

<script>
import ResponsiveInputForm from "../../WebsiteShell/UI/responsiveInputForm"
import GlobalSettings from "./settingsPageComponents/globalSettings"
import ObjectSettings from "./settingsPageComponents/objectSettings"
import TriggerSettings from "./settingsPageComponents/triggerSettings"
import SelectorObject from "./createPageComponents/selectorObject"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "settingsPage",
  components: {SelectorObject, TriggerSettings, ObjectSettings, GlobalSettings, ResponsiveInputForm},
  data: () => ({
    idObjectSettings: null,
    idTriggerSettings: null,
  }),
  computed: {
    ...mapGetters(['globalDisplaySettings', 'baseClassifiers', 'objectTriggers']),
    getClassifiers: function () { return this.baseClassifiers(this.idObjectSettings) },
    getTriggers: function() { return this.objectTriggers(this.idTriggerSettings) },
  },
  methods: {
    ...mapActions(['changeGlobalSettingState', 'getBaseTriggers', 'setTriggerState']),
    setTrigger(event) {
      this.setTriggerState(event)
    }
  },
  mounted() {
    this.getBaseTriggers()
  }
}
</script>