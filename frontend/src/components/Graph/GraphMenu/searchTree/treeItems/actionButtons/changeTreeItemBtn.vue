<template>
  <v-menu
    v-model="menuModal" offset-x offset-y fixed bottom right
    :close-on-content-click="false" :close-on-click="false" ref="menuSettings"
    transition="slide-x-reverse-transition" min-width="350" nudge-left="340" z-index="10001"
  >
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on">
        <v-icon>mdi-pencil-outline</v-icon>
      </v-btn>
    </template>
    <select-object
      v-if="menuModal && parentObject"
      :object="parentObject"
      :new-object="newObject"
      @change="changeChildObject"
      @cancel="cancel"
    ></select-object>
    <change-root-object
      v-else-if="menuModal && !parentObject"
      :object="object"
      @cancel="cancel"
      @change="changeRootObject"
    ></change-root-object>
  </v-menu>
</template>

<script>
import ChangeRootObject from "../menuSettings/changeRootObject"
import SelectObject from "../menuSettings/selectObject"
import mixinActionButton from "./mixinActionButton"

export default {
  name: "changeTreeItemBtn",
  mixins: [ mixinActionButton, ],
  components: { SelectObject, ChangeRootObject, },
  props: {
    parentObject: {
      type: Object,
      default: function () { return null },
    },
  },
  data: () => ({
    newObject: null
  }),
  methods: {
    changeRootObject(newData) {
      this.$emit('change', newData)
      this.cancel()
    },
    changeChildObject() {
      this.$emit('change', this.newObject)
      this.cancel()
    }
  },
  mounted() {
    if (this.parentObject)
      this.newObject = JSON.parse(JSON.stringify(this.object))
  }
}
</script>

<style scoped>

</style>