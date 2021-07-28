<template>
  <v-menu
    v-model="menuModal" offset-x offset-y fixed bottom right
    :close-on-content-click="false" :close-on-click="false" ref="menuSettings"
    transition="slide-x-reverse-transition" min-width="350" nudge-left="340" z-index="10001"
  >
    <template v-slot:activator="{ on }">
      <v-btn icon @click="createNewObject()" v-on="on">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </template>
    <select-object
      v-if="menuModal"
      :object="object"
      :new-object="newObject"
      @create="create"
      @cancel="cancel"
    ></select-object>
  </v-menu>
</template>

<script>
import selectObject from "../menuSettings/selectObject"
import mixinActionButton from "./mixinActionButton"

export default {
  name: "createButton",
  mixins: [ mixinActionButton, ],
  components: { selectObject, },
  data: () => ({
    newObject: null,
  }),
  methods: {
    create() {
      this.$emit('create', this.newObject)
      this.cancel()
    },
    createNewObject () {
      this.newObject = {
        object_id: null,
        request: null,
        actual: false,
        rels: [],
        rel: {
          id: null,
          value: null,
          date_time_start: null,
          date_time_end: null,
        }
      }
    },
  }
}
</script>

<style scoped>

</style>