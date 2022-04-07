<template>
  <div>
    <v-card flat v-if="!searchRelationTreeGraph">
      <v-card-subtitle class="text-center text-no-wrap">
        Выберите на графе объект для поиска связей
      </v-card-subtitle>
    </v-card>
    <search-tree-items :tree="searchRelationTreeGraph" :find="findRelationsOnServer"/>
  </div>
</template>

<script>
import SearchTreeItems from "@/components/Graph/GraphMenu/Search/SearchTree/SearchTreeItems"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "SearchRelationPage",
  components: {SearchTreeItems},
  computed: mapGetters(['searchRelationTreeGraph']),
  methods: mapActions(['findRelationsOnServer']),
}
</script>

<style scoped>

</style>