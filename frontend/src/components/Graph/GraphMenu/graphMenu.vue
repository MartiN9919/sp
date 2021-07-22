<template>
  <div v-if="positionNewGraphObject">
    <div class="px-2 pt-2" style="height: 3em">
      <v-select
        :items="listOfPrimaryObjects" v-model="graphObject" :menu-props="{ offsetY: true }" @change="getClassifiersOfObject"
        item-text="title" item-value="id" hide-no-data hide-details outlined
        color="teal" item-color="teal" class="v-input--dense" label="Тип объекта"
      ></v-select>
    </div>
    <div style="display: flex; flex-direction: column; height: calc(100% - 3em);">
      <div ref="searchTreeView" style="max-height: 30%; overflow-y: auto; flex-shrink: 0">
        <search-tree-view
          :search-tree="searchTreeView"
          :search-status="searchStatus"
          @findObject="findObject"
        ></search-tree-view>
      </div>
      <div style="max-height: calc(100% - 4em); overflow-y: auto">
        <list-found-objects
          :object-id="graphObject"
          :found-objects="foundObjects"
        ></list-found-objects>
      </div>

    </div>
<!--    <creator-object></creator-object>-->
  </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex"
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
  }),
  computed: {
    ...mapGetters(['positionNewGraphObject', 'selectedGraphObjectId', 'listOfPrimaryObjects', ]),
    graphObject: {
      get: function () { return this.selectedGraphObjectId },
      set: function (id) {
        this.setSelectedGraphObjectId(id)
        this.createSearchTreeView(id)
        this.foundObjects = null
      },
    },
  },
  methods: {
    ...mapActions(['setSelectedGraphObjectId', ]),
    findObject () {
      this.searchStatus = true
      this.$store.dispatch('findObjectsOnServer', { searchTree: this.searchTreeView })
      .then(response => {
        this.searchStatus = false
        this.foundObjects = response.data
      })
      .catch(() => { this.searchStatus = false })
    },
    createSearchTreeView (id) {
      this.searchTreeView = { object_id: id, rel: null, request: '', actual: false, rels: [] }
    },
    getClassifiersOfObject () {
      this.$store.dispatch('getListOfClassifiersOfObjects', { params: { object_id: this.graphObject } })
    }
  },
}
</script>

<style scoped>
</style>