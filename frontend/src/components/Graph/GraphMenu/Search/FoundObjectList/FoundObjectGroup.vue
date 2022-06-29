<template>
  <div>
    <v-list-item v-if="title" dense dark class="blue-grey text-center text-uppercase">
      <v-list-item-title>{{ title }}: {{ objects.length }}</v-list-item-title>
    </v-list-item>
    <found-object-item v-for="object in objects" :key="`${object.object_id}-${object.rec_id}`" :object="object"/>
  </div>
</template>

<script>
import FoundObjectItem from "@/components/Graph/GraphMenu/Search/FoundObjectList/FoundObjectsItem"

export default {
  name: "FoundObjectGroup",
  components: {FoundObjectItem},
  props: {
    objects: Array,
    title: String
  }
}
</script>

<style scoped>

</style>