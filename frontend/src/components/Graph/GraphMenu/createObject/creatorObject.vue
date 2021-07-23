<template>
  <div @contextmenu.stop="contextMenu = { event: $event, typeMenu: 'creatorObject' }">
    <v-form ref="form" v-model="valid" lazy-validation class="pb-3">
      <creator-form
        v-for="(classifier, key) in object.params" :key="key" class="px-3 pt-5"
        v-model="classifier.value"
        @observer="classifier.changed = $event"
        :classifier="getClassifier(object.object_id, classifier.id)"
        @contextmenu.native.stop="contextMenu = { event: $event, typeMenu: classifier.id }"
      >
        <context-menu v-if="classifier.id === typeContextMenu && !('date' in classifier)">
          <context-creator-form @deleteClassifier="deleteClassifier(classifier)"></context-creator-form>
        </context-menu>
      </creator-form>
      <v-btn @click.right.stop="" @click="saveObject"  outlined color="teal" class="mt-5 mx-12">
        Сохранить
      </v-btn>
    </v-form>
    <context-menu v-if="typeContextMenu === 'creatorObject'">
      <context-creator-object
        :object-id="object.object_id" :classifiers="object.params" @selectClassifier="selectClassifier"
      ></context-creator-object>
    </context-menu>
    <v-dialog v-model="conflictForm" width="70%" ref="conflictForm">
      <conflict-form></conflict-form>
    </v-dialog>
  </div>
</template>

<script>
import creatorForm from "./creatorForm"
import conflictForm from "./conflictForm/conflictForm"
import toolsContextMenu from "../../../WebsiteShell/ContextMenu/Mixins/toolsContextMenu"
import contextMenu from "../../../WebsiteShell/ContextMenu/contextMenu"
import contextCreatorObject from "../../ContextMenus/contextCreateObject/contextCreatorObject"
import contextCreatorForm from "../../ContextMenus/contextCreateObject/contextCreatorForm"

export default {
  name: "creatorObject",
  props: { objectId: Number },
  mixins: [ toolsContextMenu, ],
  components: { creatorForm, contextMenu, contextCreatorObject, contextCreatorForm, conflictForm, },
  data: () => ({
    newObject: null,
    valid: true,
    contextMenu: { event: null, typeMenu: null,},
  }),
  computed: {
    conflictForm: {
      get: function () { return this.$store.getters.conflictingObjects.length !== 0 },
      set: function (value) { if (!value) this.$store.dispatch('clearConflictingObjects') },
    },
    object: function () {
      this.newObject = JSON.parse(JSON.stringify(this.$store.getters.primaryObject(this.objectId)))
      this.newObject.params = []
    }
  },
  methods: {
    getClassifier (objectId, classifierId) {
      return this.$store.getters.classifier({ objectId: objectId, classifierId: classifierId })
    },
    selectClassifier(classifier) {

      this.deactivateContextMenu()
    },
    deleteClassifier (classifier) {
      this.object.params.splice(this.object.params.findIndex(item => item.id === classifier.id), 1)
    },
    saveObject () {
      if (this.$refs.form.validate())
        this.$store.dispatch('createNewObjectFromServer')
    }
  }
}
</script>

<style scoped>
</style>