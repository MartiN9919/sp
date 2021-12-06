<template>
  <div class="overflow-y-auto h-100">
    <global-settings
      :settings="globalDisplaySettings"
      @changeSettings="changeGlobalSettingState"
    ></global-settings>
    <object-settings :classifiers="getClassifiers" @setClassifier="setClassifier">
      <v-list-item class="px-2">
        <selector-object v-model="idObjectSettings" start-object ></selector-object>
      </v-list-item>
    </object-settings>
    <trigger-settings :triggers="getTriggers" @setTrigger="setTrigger">
      <v-list-item class="px-2">
        <selector-object v-model="idTriggerSettings" start-object :is-get-classifiers="false"></selector-object>
      </v-list-item>
    </trigger-settings>
  </div>
</template>

<script>
import ResponsiveInputForm from "@/components/WebsiteShell/CustomComponents/responsiveInputForm"
import GlobalSettings from "@/components/Graph/GraphMenu/settingsPageComponents/globalSettings"
import ObjectSettings from "@/components/Graph/GraphMenu/settingsPageComponents/objectSettings"
import TriggerSettings from "@/components/Graph/GraphMenu/settingsPageComponents/triggerSettings"
import SelectorObject from "@/components/Graph/GraphMenu/createPageComponents/selectorObject"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "settingsPage",
  components: {SelectorObject, TriggerSettings, ObjectSettings, GlobalSettings, ResponsiveInputForm},
  data: () => ({
    idObjectSettings: null,
    idTriggerSettings: null,
  }),
  computed: {
    ...mapGetters(['globalDisplaySettings', 'baseClassifiers', 'objectTriggers', 'classifiersSettings']),
    getClassifiers: function () {
      let classifiers = []
      for (let baseClassifier of this.baseClassifiers(this.idObjectSettings))
        classifiers.push(Object.assign({
          status: !this.classifiersSettings.includes(baseClassifier.id)
        }, baseClassifier))
      return classifiers
    },
    getTriggers: function() { return this.objectTriggers(this.idTriggerSettings) },
  },
  methods: {
    ...mapActions(['changeGlobalSettingState', 'setTriggerState', 'setClassifiersSettings']),
    setTrigger(event) {
      this.setTriggerState(event)
    },
    setClassifier(classifierId) {
      this.setClassifiersSettings(classifierId)
    }
  },
}
</script>