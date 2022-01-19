<template>
  <body-block-settings :icon="icon" :title="title" :sub-title="subTitle">
    <slot></slot>
    <v-card v-for="trigger of triggers" :key="trigger.id" class="ma-2">
      <v-list class="pt-0">
        <v-list-item @click="activateTrigger(trigger)" dense v-ripple="{ class: 'teal--text' }">
          <v-list-item-content>
            <v-list-item-title>{{trigger.title}}</v-list-item-title>
            <v-list-item-subtitle>{{trigger.subTitle}}</v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-action class="flex-row">
            <v-switch v-model="trigger.state" disabled color="teal"></v-switch>
          </v-list-item-action>
        </v-list-item>
        <v-divider v-if="trigger.variables.length" class="pb-2"></v-divider>
        <v-form :ref="'form' + trigger.id" onSubmit="return false;">
          <v-list-item v-for="param in trigger.variables" :key="param.name">
            <responsive-input-form
              v-model="param.value"
              @changeInputString="deactivateTrigger(trigger, false)"
              :input-type="param.type"
              :label="param.title"
              :list-rules="param.necessary ? ['notEmpty'] : []"
            ></responsive-input-form>
          </v-list-item>
        </v-form>
      </v-list>
    </v-card>
    <v-card v-if="!triggers.length" flat class="ma-2">
      <v-card-title class="justify-center py-0" style="white-space: normal">У данного объекта триггеры отсутствуют</v-card-title>
    </v-card>
  </body-block-settings>
</template>

<script>
import BodyBlockSettings from "@/components/Graph/GraphMenu/settingsPageComponents/bodyBlockSettings"
import SelectorObject from "@/components/Graph/GraphMenu/createPageComponents/selectorObject"
import ResponsiveInputForm from "@/components/WebsiteShell/CustomComponents/responsiveInputForm"

export default {
  name: "triggerSettings",
  components: {SelectorObject, ResponsiveInputForm, BodyBlockSettings},
  props: {
    triggers: Array,
  },
  data: () => ({
    icon: 'mdi-flag-outline',
    title: 'Настройки триггеров',
    subTitle: 'Настройка отслеживаемых свойств',
    selectObject: null,
  }),
  methods: {
    deactivateTrigger(trigger) {
      this.$emit('setTrigger', {triggerId: trigger.id, value: false})
    },
    activateTrigger(trigger) {
      if (this.$refs['form' + trigger.id][0].validate())
        this.$emit('setTrigger', {triggerId: trigger.id, value: !trigger.state})
    }
  }
}
</script>

<style scoped>

</style>