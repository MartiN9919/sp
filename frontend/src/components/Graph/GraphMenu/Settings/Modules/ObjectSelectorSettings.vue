<template>
  <v-list dense class="py-0">
    <v-list-item two-line class="px-2">
      <selector-object v-model="id" start-object/>
    </v-list-item>
    <slot/>
  </v-list>
</template>

<script>
import SelectorObject from "@/components/Graph/GraphMenu/Create/Headers/SelectorObject"

export default {
  name: "ObjectSelectorSettings",
  components: {SelectorObject},
  model: {
    prop: 'objectId',
    event: 'changeId',
  },
  props: {
    objectId: Number,
  },
  computed: {
    id: {
      get: function () {
        return this.objectId
      },
      set: function (id) {
        this.$emit('changeId', id)
      }
    }
  }
}
</script>

<style scoped>

</style>