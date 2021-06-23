<template>
  <v-container class="pa-0">
    <custom-app-bar :work-place="workAreaAboveObjects" v-model="active"></custom-app-bar>
    <v-row v-for="object in workAreaAboveObjects" :key="object.tempId" v-show="object.tempId === active" no-gutters>
      <v-window v-model="window" style="width: 100%">
        <v-window-item value="foundObjects" :transition="false">
          <list-found-objects :object="object"></list-found-objects>
        </v-window-item>
        <v-window-item value="objectConstructor" :transition="false">
          Добавить
        </v-window-item>
        <v-window-item value="searchTree" :transition="false">
          <search-tree-view :object="object" @findObject="findObject"></search-tree-view>
        </v-window-item>
      </v-window>
      <speed-dial-of-tools
        :items="speedDialOfTools"
        @selectTool="setWindowForActiveObject($event)"
      ></speed-dial-of-tools>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import customAppBar from "./customAppBar"
import speedDialOfTools from "../../WebsiteShell/AdditionalTools/speedDialOfTools"
import searchTreeView from "./searchTreeView";
import listFoundObjects from "./listFoundObjects";

export default {
  name: "graphMenu",
  components: { searchTreeView, customAppBar, speedDialOfTools, listFoundObjects, },
  computed: {
    ...mapGetters(['workAreaAboveObjects', 'activeObject', ]),
    window: {
      get: function () { return this.activeObject?.activeWindow },
      set: function (window) { this.setWindowForActiveObject(window) },
    },
    active: {
      get: function () { return this.activeObject?.tempId },
      set: function (id) { this.setActiveObjectId(id) },
    }
  },
  data: () => ({
    speedDialOfTools: [
      { id: 'foundObjects', title: 'Список найденных объектов', icon: 'mdi-format-list-text', color: 'blue' },
      { id: 'objectConstructor', title: 'Добавить новый объектв', icon: 'mdi-plus', color: 'green' },
      { id: 'searchTree', title: 'Найти объект в системе', icon: 'mdi-magnify', color: 'red' },
    ],
  }),
  methods: {
    ...mapActions(['setWindowForActiveObject', 'setActiveObjectId', 'findObjectOnServer', ]),
    findObject () {
      this.findObjectOnServer()
      .then(() => { this.window = 'foundObjects' })

    }
  },
}
</script>

<style scoped>

</style>