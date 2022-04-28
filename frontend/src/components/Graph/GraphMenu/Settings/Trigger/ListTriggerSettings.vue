<template>
  <object-selector-settings v-model="id" class="pb-1">
    <item-trigger-settings v-for="trigger of triggers" :key="trigger.id" :trigger="trigger"/>
  </object-selector-settings>
</template>

<script>
import ObjectSelectorSettings from "@/components/Graph/GraphMenu/Settings/Modules/ObjectSelectorSettings"
import ItemTriggerSettings from "@/components/Graph/GraphMenu/Settings/Trigger/ItemTriggerSettings"
import {mapGetters} from "vuex";

export default {
  name: "ListTriggerSettings",
  components: {ItemTriggerSettings, ObjectSelectorSettings},
  data: () => ({
    id: null
  }),
  computed: {
    ...mapGetters(['objectTriggers']),
    triggers: function() {
      return this.objectTriggers(this.id)
    },
  }
}
</script>

<style scoped>

</style>