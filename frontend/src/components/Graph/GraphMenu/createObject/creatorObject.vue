<template>
  <div @contextmenu.stop="contextMenu = { event: $event, typeMenu: 'creatorObject' + object.tempId }">
    <v-form ref="form" v-model="valid" lazy-validation>
      <creator-form
        v-for="(classifier, key) in object.params" :key="key" class="px-3 pt-5"
        v-model="classifier.value" @observer="classifier.changed = $event"
        :classifier="getClassifier(object.object_id, classifier.id)"
        @contextmenu.native.stop="contextMenu = { event: $event,  typeMenu: getNameContextInput(classifier.id) }"
      >
        <context-menu v-if="getNameContextInput(classifier.id) === typeContextMenu && !('date' in classifier)">
          <context-creator-form @deleteClassifier="deleteClassifier(classifier)"></context-creator-form>
        </context-menu>
      </creator-form>
      <v-btn @click.right.stop="" @click="saveObject"  outlined color="teal" class="mt-5 mx-12">
        Сохранить
      </v-btn>
    </v-form>
    <context-menu v-if="typeContextMenu === 'creatorObject' + object.tempId">
      <context-creator-object
        :object-id="object.object_id" :classifiers="object.params" @selectClassifier="selectClassifier"
      ></context-creator-object>
    </context-menu>
  </div>
</template>

<script>
import creatorForm from "./creatorForm";
import toolsContextMenu from "../../../WebsiteShell/ContextMenu/Mixins/toolsContextMenu"
import contextMenu from "../../../WebsiteShell/ContextMenu/contextMenu"
import contextCreatorObject from "../../ContextMenus/contextCreatorObject"
import contextCreatorForm from "../../ContextMenus/contextCreatorForm";

export default {
  name: "creatorObject",
  props: { object: Object },
  mixins: [ toolsContextMenu, ],
  components: { creatorForm, contextMenu, contextCreatorObject, contextCreatorForm, },
  data: () => ({
    valid: true,
    contextMenu: { event: null, typeMenu: null,},
  }),
  methods: {
    getClassifier (objectId, classifierId) {
      return this.$store.getters.classifier({ objectId: objectId, classifierId: classifierId })
    },
    selectClassifier(classifier) {
      this.$store.dispatch('addClassifierToObject', {
        classifier: { id: classifier.id, value: null, },
        tempId: this.object.tempId
      })
      this.deactivateContextMenu()
    },
    getNameContextInput(classifierId) { return this.object.tempId.toString() + classifierId.toString() },
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