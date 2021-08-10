<template>
  <drop-down-menu min-width="350" left :close-on-content-click="false">
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on">
        <v-icon>mdi-pencil-outline</v-icon>
      </v-btn>
    </template>
    <template v-slot:body="{ status, closeMenu }">
      <select-object
        v-if="status && parentObject"
        :object="parentObject"
        :new-object="newObject"
        @change="changeChildObject()"
        @cancel="closeMenu"
      ></select-object>
      <change-root-object
        v-else-if="status && !parentObject"
        :object="object"
        @cancel="closeMenu"
        @change="changeRootObject"
      ></change-root-object>
    </template>
  </drop-down-menu>
</template>

<script>
import DropDownMenu from "../../../../../WebsiteShell/InputForms/BodyToForm/dropDownMenu"
import ChangeRootObject from "../menuSettings/changeRootObject"
import SelectObject from "../menuSettings/selectObject"

export default {
  name: "changeTreeItemBtn",
  components: {DropDownMenu, SelectObject, ChangeRootObject, },
  props: {
    object: Object,
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
    },
    changeChildObject() {
      this.$emit('change', this.newObject)
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