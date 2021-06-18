<template>

</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "ObjectFinder",
  computed: {
    ...mapGetters(['listObjects', ])
  },
  methods: {
    titleObject (objectId) {
      return this.listObjects.find(object => object.id === objectId)
    },
  }
}
</script>

<style scoped>

</style>