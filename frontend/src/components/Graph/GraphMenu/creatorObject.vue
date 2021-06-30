<template>
  <div
    style="height: 100%" class="px-3 pt-5 text-center"
    @contextmenu.stop="contextMenu = { event: $event, typeMenu: 'creatorObject' }"
  >
    <settings-analytics
      autocomplete="off"
      v-for="classifier in object.params"
      :title="$store.getters.classifiersForObjects(object.object_id).find(object => object.id === classifier.id).title"
      :type="$store.getters.classifiersForObjects(object.object_id).find(object => object.id === classifier.id).type"
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
import {mapActions, mapGetters} from "vuex"

export default {
  name: "creatorObject",
  props: { object: Object },
  mixins: [ toolsContextMenu, ],
  components: { settingsAnalytics, contextMenu, contextCreatorObject, },
  data: () => ({
    contextMenu: { event: null, typeMenu: null,},
  }),
  methods: {
    ...mapActions(['addClassifierToObject', ]),
    selectClassifier(classifier) {
      this.addClassifierToObject({ classifier: { id: classifier.id, value: null, }, tempId: this.object.tempId})
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