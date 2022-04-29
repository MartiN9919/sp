<template>
  <v-list class="py-0" v-if="foundObjects">
    <v-list-item class="title-table">
      <v-list-item-subtitle class="text-title-table">
        Найдено объектов: {{foundObjects.length}}
      </v-list-item-subtitle>
    </v-list-item>
    <div class="body-table">
      <found-object-item
          v-for="object in foundObjects"
          :key="object.rel_id"
          :object="object"
      />
    </div>
  </v-list>
</template>

<script>
import FoundObjectItem from "@/components/Graph/GraphMenu/Search/FoundObjectList/FoundObjectsItem"
import {mapGetters} from "vuex"

export default {
  name: "FoundObjectList",
  components: {FoundObjectItem},
  computed: mapGetters(['foundObjects'])
}
</script>

<style scoped>
.title-table {
  background-color: rgba(0, 0, 0, .1);
  min-height: 36px;
}
.text-title-table {
  display: flex;
  justify-content: space-around;
}
.body-table {
  overflow-y: auto;
  height: calc(100% - 36px);
}
</style>