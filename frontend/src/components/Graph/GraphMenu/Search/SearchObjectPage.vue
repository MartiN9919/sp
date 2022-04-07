<template>
  <div class="overflow-x-hidden d-flex flex-column h-100" style="min-width: 300px">
    <search-tree-items :tree="searchTreeGraph" :find="findObjectsOnServer"/>
    <found-objects-list class="overflow-y-hidden"/>
  </div>
</template>

<script>
import SearchTreeItems from "@/components/Graph/GraphMenu/Search/SearchTree/SearchTreeItems"
import FoundObjectsList from "@/components/Graph/GraphMenu/Search/FoundObjectList/FoundObjectList"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "SearchObjectPage",
  components: {SearchTreeItems, FoundObjectsList},
  computed: mapGetters(['searchTreeGraph']),
  methods: mapActions(['findObjectsOnServer']),
}
</script>

<style scoped>

</style>