<template>
  <v-row no-gutters style="flex-wrap: nowrap; height: 100%;">
    <v-col style="max-width: 56px">
      <tools-menu></tools-menu>
    </v-col>
    <v-col v-if="activeWindow === 'dossierPage'" style="max-width: calc(100% - 56px)">
      <dossier></dossier>
    </v-col>
    <v-col v-if="activeWindow === 'searchPage'" class="search-page" style="max-width: calc(100% - 56px)">
      <search-tree v-model="searchTreeItems" @findObject="findObject" class="search-tree pb-2"></search-tree>
      <found-objects v-if="foundObjects" :objects="foundObjects"></found-objects>
    </v-col>
    <v-col v-if="activeWindow === 'addPage'" style="max-width: calc(100% - 56px)">
      <div style="height: calc(100% - 3em)">
        <select-object
          v-model="selectedEditableObject"
          :items="listOfPrimaryObjects"
          style="height: 3.3em"
          class="py-2"
        ></select-object>
        <object-record-area
          v-if="editableObject"
          :classifiers="editableObject.params"
          class="overflow-y-auto"
          style="max-height: calc(100% - 3em)"
        ></object-record-area>
      </div>
      <v-divider></v-divider>
      <control-menu style="align-items: flex-end; height: 3em" @save="saveObject"></control-menu>
    </v-col>
  </v-row>
</template>

<script>
import ToolsMenu from "../../WebsiteShell/UI/toolsMenu"
import SearchTree from "./searchTree/searchTree"
import FoundObjects from "./searchTree/foundObjects"
import router from '@/router'
import { mapActions, mapGetters } from "vuex"
import SelectObject from "./createObject/selectorObject";
import ObjectRecordArea from "./createObject/objectRecordArea";
import ControlMenu from "./createObject/controlMenu";
import Dossier from "./dossierObject/dossier";

export default {
  name: "graphMenu",
  components: {Dossier, ControlMenu, ObjectRecordArea, SelectObject, FoundObjects, SearchTree, ToolsMenu, },
  computed: {
    ...mapGetters(['activeTool', 'searchTreeGraph', 'foundObjects', 'primaryObject', 'listOfPrimaryObjects', 'editableObject', ]),
    activeWindow: function () {
      return this.activeTool(router.currentRoute.name)
    },
    searchTreeItems: {
      get: function () { return this.searchTreeGraph },
      set: function (value) { this.setRootSearchTreeGraph(value) }
    },
    selectedEditableObject: {
      get: function () { return this.primaryObject(this.editableObject?.object_id) },
      set: function (object) {
        this.getListOfClassifiersOfObjects({ params: { object_id: object.id } })
        .then(() => {
          this.setEditableObject({ object_id: object.id })
        })
      },
    }
  },
  methods: {
    ...mapActions(['setRootSearchTreeGraph', 'findObjectsOnServer', 'setEditableObject', 'getListOfClassifiersOfObjects', 'saveEditableObject']),
    findObject () {
      this.findObjectsOnServer({ searchTree: this.searchTreeItems })
    },
    saveObject () {
      this.saveEditableObject()
    }
  },
}
</script>

<style scoped>
.search-tree {
  max-height: 100%;
  overflow-y: auto
}
</style>