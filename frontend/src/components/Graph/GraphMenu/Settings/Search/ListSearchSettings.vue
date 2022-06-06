<template>
  <v-list dense>
    <item-search-settings
      v-for="(setting, key) in globalDisplaySettings"
      :key="key"
      v-model="setting.state.value"
      :title="setting.title"
      :sub-title="setting.subTitle"
    />
  </v-list>
</template>

<script>
import ItemSearchSettings from "@/components/Graph/GraphMenu/Settings/Search/ItemSearchSettings"
import {mapGetters} from "vuex"

export default {
  name: "ListSearchSettings",
  components: {ItemSearchSettings},
  computed: mapGetters(['globalDisplaySettings'])
}
</script>

<style scoped>

</style>