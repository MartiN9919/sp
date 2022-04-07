<template>
  <v-list dense>
    <item-global-settings
      v-for="(setting, key) in globalDisplaySettings"
      :key="key"
      v-model="setting.state.value"
      :title="setting.title"
      :sub-title="setting.subTitle"
    />
  </v-list>
</template>

<script>
import ItemGlobalSettings from "@/components/Graph/GraphMenu/Settings/Global/ItemGlobalSettings"
import {mapGetters} from "vuex"

export default {
  name: "ListGlobalSettings",
  components: {ItemGlobalSettings},
  computed: mapGetters(['globalDisplaySettings'])
}
</script>

<style scoped>

</style>