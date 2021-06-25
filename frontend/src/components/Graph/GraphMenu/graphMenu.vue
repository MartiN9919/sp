<template>
  <div class="pa-0">
    <custom-app-bar :work-place="workAreaAboveObjects" v-model="active"></custom-app-bar>
    <div v-for="object in workAreaAboveObjects" :key="object.tempId" v-show="object.tempId === active">
      <v-window v-model="window" style="width: 100%; height: 100%">
        <v-window-item value="searchTree" :transition="false">
          <res-split-pane
              split-to="rows" :allow-resize="true"
              :min-size="10" :max-size="90" :size="90"
              class="ma-0" units="percents" :resizerThickness="1"
              :resizerBorderThickness="1" resizer-border-thickness="">
            <div slot="firstPane" class="ma-3" style="width: 100%;">
              <search-tree-view :object="object" @findObject="findObject"></search-tree-view>
            </div>
            <div slot="secondPane" class="ma-3"  style="width: 100%">
              <list-found-objects :object="object"></list-found-objects>
            </div>
          </res-split-pane>
        </v-window-item>
        <v-window-item value="foundObjects" :transition="false">
          <list-found-objects :object="object"></list-found-objects>
        </v-window-item>
        <v-window-item value="objectConstructor" :transition="false">

        </v-window-item>
      </v-window>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import customAppBar from "./customAppBar"
import speedDialOfTools from "../../WebsiteShell/AdditionalTools/speedDialOfTools"
import searchTreeView from "./searchTreeView";
import listFoundObjects from "./listFoundObjects";
import ResSplitPane from 'vue-resize-split-pane'

export default {
  name: "graphMenu",
  components: { searchTreeView, customAppBar, speedDialOfTools, listFoundObjects, ResSplitPane},
  computed: {
    ...mapGetters(['workAreaAboveObjects', 'activeObject', 'foundObjects']),
    window: {
      get: function () { return this.activeObject?.activeWindow },
      set: function (window) { this.setWindowForActiveObject(window) },
    },
    active: {
      get: function () { return this.activeObject?.tempId },
      set: function (id) { this.setActiveObjectId(id) },
    }
  },
  methods: {
    ...mapActions(['setWindowForActiveObject', 'setActiveObjectId', 'findObjectOnServer', ]),
    findObject () {
      this.findObjectOnServer()
    }
  },
}
</script>

<style scoped>

</style>