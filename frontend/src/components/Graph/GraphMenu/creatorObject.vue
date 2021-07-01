<template>
  <div
    class="px-3 pt-5 text-center"
    @contextmenu.stop="contextMenu = { event: $event, typeMenu: 'creatorObject' }"
  >
    <settings-analytics
      autocomplete="off"
      v-for="(classifier, key) in object.params" :key="key"
      :title="getClassifier(object.object_id, classifier.id).title"
      :type="getClassifier(object.object_id, classifier.id).type"
      :hint="getClassifier(object.object_id, classifier.id).hint"
      :list="getClassifier(object.object_id, classifier.id).list_id"
      v-model="classifier.value"
    ></settings-analytics>
    <v-btn outlined color="teal" @click="saveObject">Временная кнопка сохранения объекта</v-btn>
    <context-menu v-if="contextMenu.typeMenu === typeContextMenu">
      <context-creator-object :object-id="object.object_id" @selectClassifier="selectClassifier"></context-creator-object>
    </context-menu>
  </div>
</template>

<script>
import settingsAnalytics from "../../WebsiteShell/NavigationDrawer/ConstructorBlocks/settingsAnalytics"
import toolsContextMenu from "../../WebsiteShell/ContextMenu/Mixins/toolsContextMenu"
import contextMenu from "../../WebsiteShell/ContextMenu/contextMenu"
import contextCreatorObject from "../ContextMenus/contextCreatorObject"

export default {
  name: "creatorObject",
  props: { object: Object },
  mixins: [ toolsContextMenu, ],
  components: { settingsAnalytics, contextMenu, contextCreatorObject, },
  data: () => ({
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
    saveObject () {
      this.$store.dispatch('createNewObjectFromServer')
    }
  }
}
</script>

<style scoped>

</style>