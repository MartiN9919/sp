<template>

</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "ObjectFinder",
  computed: {
    ...mapGetters(['listObjects', ])
  },
  methods: {
    ...mapActions(['addListObjects', ]),
    titleObject (objectId) {
      return this.listObjects.find(object => object.id === objectId)
    },
  },
  created() {
    this.addListObjects({})
  },
}
</script>

<style scoped>

</style>