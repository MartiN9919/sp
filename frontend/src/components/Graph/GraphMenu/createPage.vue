<template>
  <v-col>
    <div class="work-place">
      <selector-object
          v-model="selectedEditableObject"
          :items="listOfPrimaryObjects"
          class="selector-object py-2"
      ></selector-object>
      <v-form ref="form">
        <object-record-area
            v-if="editableObject"
            :classifiers="editableObject.params"
            class="object-record-area overflow-y-auto"
        ></object-record-area>
      </v-form>
    </div>
    <v-divider></v-divider>
    <control-menu
      class="control-menu"
      @save="saveObject"
      :text-button="textButton"
    ></control-menu>
  </v-col>
</template>

<script>
import SelectorObject from "./createPageComponents/selectorObject"
import ObjectRecordArea from "./createPageComponents/objectRecordArea"
import ControlMenu from "./createPageComponents/controlMenu"
import {mapActions, mapGetters} from "vuex";

export default {
  name: "createPage",
  components: {ControlMenu, ObjectRecordArea, SelectorObject},
  computed: {
    ...mapGetters(['primaryObject', 'listOfPrimaryObjects', 'editableObject']),
    textButton: function () { return this.editableObject?.rec_id ? 'Сохранить' : 'Создать' },
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
    ...mapActions(['getListOfClassifiersOfObjects', 'setEditableObject', 'saveEditableObject']),
    saveObject () {
      if(this.$refs.form.validate())
        this.saveEditableObject()
    }
  }
}
</script>

<style scoped>
.work-place {
  height: calc(100% - 3em);
}
.selector-object {
  height: 3.3em;
}
.object-record-area {
  max-height: calc(100% - 3em);
}
.control-menu {
  height: 3em;
  align-items: flex-end;
}
</style>