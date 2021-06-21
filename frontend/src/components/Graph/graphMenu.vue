<template>
  <v-container class="pa-0">
    <custom-app-bar
      :work-place="workPlace"
      v-model="activeObject"
    ></custom-app-bar>
    <v-row v-for="(object, key) in workPlace" :key="key" v-if="key === activeObject" no-gutters>
      <search-tree-view :active-object="object"></search-tree-view>
      <speed-dial-of-tools></speed-dial-of-tools>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import searchTreeView from "../NavigationDrawer/ConstructorBlocks/BlocksForEnteringValues/searchTreeView";
import customAppBar from "./customAppBar";
import speedDialOfTools from "./speedDialOfTools";

export default {
  name: "graphMenu",
  components: { searchTreeView, customAppBar, speedDialOfTools, },
  computed: {
    ...mapGetters(['workPlace',]),
  },
  data: () => ({
    activeObject: null,
  }),
}
</script>

<style scoped>

</style>