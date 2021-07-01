<template>
  <div style="height: 100%" class="overflow-y-auto">
    <custom-app-bar
      v-model="active"
      :work-place="workAreaOfObjects"
      @selectMenuItem="selectMenuItem"
    ></custom-app-bar>
    <div
      v-for="object in workAreaOfObjects" :key="object.tempId"
      v-show="object.tempId === active"
    >
      <search-tree-view
        v-if="windowActiveObject === 'searchTree'"
        v-model="object.searchTree"
        @findObject="findObject"
      ></search-tree-view>
      <list-found-objects
        v-if="windowActiveObject === 'searchTree'"
        :object="object"
      ></list-found-objects>
      <creator-object
        v-if="windowActiveObject === 'createObject'"
        :object="object"
      ></creator-object>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import customAppBar from "./customAppBar"
import searchTreeView from "./searchTreeView"
import listFoundObjects from "./listFoundObjects"
import creatorObject from "./creatorObject";

export default {
  name: "graphMenu",
  components: { searchTreeView, customAppBar, listFoundObjects, creatorObject},
  computed: {
    ...mapGetters(['workAreaOfObjects', 'activeObject', 'windowActiveObject',]),
    active: {
      get: function () { return this.activeObject?.tempId },
      set: function (id) { this.$store.dispatch('setActiveObjectId', id) },
    }
  },
  methods: {
    findObject () {
      this.$store.dispatch('findObjectsOnServer')
    },
    selectMenuItem(selected) {
      if(selected.window === 'createObject')
        this.$store.dispatch('createNewObject', selected.object)
    },
  },

}
</script>

<style scoped>
.column-settings {

}
</style>