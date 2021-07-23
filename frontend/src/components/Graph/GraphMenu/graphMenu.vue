<template>
  <div v-if="positionNewGraphObject">
    <v-select
      :items="listOfPrimaryObjects" v-model="graphObject" :menu-props="{ offsetY: true }"
      item-text="title" item-value="id" hide-no-data hide-details outlined
      color="teal" item-color="teal" class="v-input--dense pa-2" label="Тип объекта"
    >
      <template v-slot:append-outer="" style="margin-top: 0">
        <v-menu offset-x z-index="10001" max-height="50%">
          <template v-slot:activator="{ on, value }">
            <v-btn :loading="searchStatus" v-on="on" icon large>
              <v-icon color="teal">mdi-cog-outline</v-icon>
            </v-btn>
          </template>
          <v-list rounded>
            <v-list-item v-if="modeInputMenu === 'search'" @click="modeInputMenu = 'create'">
              <v-list-item-icon>
                <v-icon>mdi-content-save-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Создать новый объект</v-list-item-title>
            </v-list-item>
            <v-list-item v-if="modeInputMenu === 'create'" @click="modeInputMenu = 'search'">
              <v-list-item-icon>
                <v-icon>mdi-magnify-plus-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Найти объект</v-list-item-title>
            </v-list-item>
            <v-list-item @click="setPositionNewGraphObject(null)">
              <v-list-item-icon>
                <v-icon>mdi-close-circle-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Отменить</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </v-select>
    <div v-if="modeInputMenu === 'search'" style="display: flex; flex-direction: column; height: calc(100% - 3em);">
      <search-tree-view
        :search-tree="searchTreeView"
        :search-status="searchStatus"
        @findObject="findObject"
        style="max-height: 30%; overflow-y: auto; flex-shrink: 0" class="pb-2 px-2"
      ></search-tree-view>
      <list-found-objects
        :object-id="graphObject"
        :found-objects="foundObjects"
        style="overflow-y: auto"
      ></list-found-objects>
    </div>
    <creator-object
      v-else-if="modeInputMenu === 'create'"
      :object-id="graphObject"
    ></creator-object>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import searchTreeView from "./searchTree/searchTreeView"
import listFoundObjects from "./foundObjects/listFoundObjects"
import creatorObject from "./createObject/creatorObject";

export default {
  name: "graphMenu",
  components: { searchTreeView, listFoundObjects, creatorObject, },
  data: () => ({
    searchTreeView: null,
    searchStatus: false,
    foundObjects: null,
    modeInputMenu: 'search',
  }),
  computed: {
    ...mapGetters(['positionNewGraphObject', 'selectedGraphObjectId', 'listOfPrimaryObjects', ]),
    graphObject: {
      get: function () { return this.selectedGraphObjectId },
      set: function (id) {
        this.setSelectedGraphObjectId(id)
        this.createSearchTreeView(id)
        this.foundObjects = null
        this.getListOfClassifiersOfObjects({ params: { object_id: this.graphObject } })
      },
    },
  },
  methods: {
    ...mapActions(['findObjectsOnServer', 'setSelectedGraphObjectId', 'getListOfClassifiersOfObjects',
      'setPositionNewGraphObject', ]),
    findObject () {
      this.searchStatus = true
      this.findObjectsOnServer({ searchTree: this.searchTreeView })
      .then(response => {
        this.searchStatus = false
        this.foundObjects = response.data
      })
      .catch(() => { this.searchStatus = false })
    },
    createSearchTreeView (id) {
      this.searchTreeView = { object_id: id, rel: null, request: '', actual: false, rels: [] }
    },
  },
}
</script>

<style>
.v-input__append-outer {
  margin: 0 !important;
  margin-left: 6px !important;
}
</style>