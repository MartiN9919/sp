<template>
  <div>
    <custom-app-bar
      v-model="active" :work-place="workAreaOfObjects"
      @selectMenuItem="selectMenuItem" class="appbar"
    ></custom-app-bar>
    <div
      v-for="object in workAreaOfObjects" :key="object.tempId"
      v-show="object.tempId === active" class="workplace"
    >
      <div v-if="windowActiveObject === 'searchTree'" class="search-place">
        <search-tree-view
          v-model="object.searchTree"
          @findObject="findObject"
          class="search-tree-view"
        ></search-tree-view>
        <list-found-objects
          :object="object"
          @changeFindObject="changeFindObject(object, $event)"
          class="list-found-objects"
        ></list-found-objects>
      </div>
      <creator-object class="creator-object text-center"
        v-if="windowActiveObject === 'createObject'"
        :object="object"
      ></creator-object>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import customAppBar from "./customAppBar"
import searchTreeView from "./searchTree/searchTreeView"
import listFoundObjects from "./searchTree/listFoundObjects"
import creatorObject from "./createObject/creatorObject";

export default {
  name: "graphMenu",
  components: { searchTreeView, customAppBar, listFoundObjects, creatorObject, },
  computed: {
    ...mapGetters(['workAreaOfObjects', 'activeObject', 'windowActiveObject',]),
    active: {
      get: function () { return this.activeObject?.tempId },
      set: function (id) { this.$store.dispatch('setActiveObjectId', id) },
    }
  },
  methods: {
    changeFindObject(object, findObject) {
      object.params = findObject.params
      object.rec_id = findObject.rec_id
      object.activeWindow = 'createObject'
    },
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
.appbar {
  height: 2.7em;
}
.workplace {
  height: calc(100% - 2.7em);
}
.search-place, .creator-object {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.list-found-objects {
  max-height: calc(100% - 4em);
  overflow-y: hidden;
}
.search-tree-view {
  max-height: 36%;
  overflow-y: auto;
}
</style>