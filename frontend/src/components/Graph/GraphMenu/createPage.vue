<template>
  <v-col>
    <div style="height: calc(100% - 3em)">
      <selector-object
          v-model="selectedEditableObject"
          :items="listOfPrimaryObjects"
          style="height: 3.3em"
          class="py-2"
      ></selector-object>
      <object-record-area
          v-if="editableObject"
          :classifiers="editableObject.params"
          class="overflow-y-auto"
          style="max-height: calc(100% - 3em)"
      ></object-record-area>
    </div>
    <v-divider></v-divider>
    <control-menu style="align-items: flex-end; height: 3em" @save="saveObject"></control-menu>
  </v-col>
</template>

<script>
import SelectorObject from "./createObject/selectorObject"
import ObjectRecordArea from "./createObject/objectRecordArea"
import ControlMenu from "./createObject/controlMenu"
import {mapActions, mapGetters} from "vuex";

export default {
  name: "createPage",
  components: {ControlMenu, ObjectRecordArea, SelectorObject},
  computed: {
    ...mapGetters(['primaryObject', 'listOfPrimaryObjects', 'editableObject']),
    selectedEditableObject: {
      get: function () { return this.primaryObject(this.editableObject?.object_id) },
      set: function (object) {
        this.getListOfClassifiersOfObjects({ params: { object_id: object.id } })
            .then(() => {
              this.setEditableObject({ object_id: object.id })
            })
      },
    },
  },
  methods: {
    ...mapActions(['getListOfClassifiersOfObjects', 'setEditableObject']),
    saveObject () {
      this.saveEditableObject()
    }
  }
}
</script>

<style scoped>

</style>