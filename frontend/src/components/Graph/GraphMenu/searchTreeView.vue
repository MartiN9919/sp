<template>
  <v-container class="pa-0">
    <v-treeview :items="[object.searchTree]" :open="openObject" return-object item-children="rels">
      <template v-slot:label="{ item, open }">
        <v-text-field
          @contextmenu.stop="contextMenu = { event: $event, typeMenu: item, }"
          outlined dense color="teal" hide-details v-model="item.request"
          :background-color="item !== object.searchTree ? 'teal lighten-5' : ''" class="mt-2"
          :label="item === object.searchTree ? labelRootObject() : labelObject(item)"
        ></v-text-field>
      </template>
      <template v-slot:append="{ item, open }">
        <v-btn large icon v-if="item === object.searchTree" class="mt-2">
          <v-icon color="teal" @click="$emit('findObject')">mdi-magnify mdi-36px</v-icon>
        </v-btn>
      </template>
    </v-treeview>
    <context-menu v-if="contextMenu.typeMenu === typeContextMenu">
      <context-search-tree-view
        :object="contextMenu.typeMenu"
        @createNewRelation="createNewRelation"
      ></context-search-tree-view>
    </context-menu>
  </v-container>
</template>

<script>
import contextMenu from "../../WebsiteShell/ContextMenu/contextMenu"
import toolsContextMenu from "../../WebsiteShell/ContextMenu/Mixins/toolsContextMenu"
import contextSearchTreeView from "../ContextMenus/contextSearchTreeView"
import { mapGetters } from "vuex";

export default {
  name: "searchTreeView",
  components: {contextMenu, contextSearchTreeView, },
  mixins: [ toolsContextMenu, ],
  props: { object: Object, searchTree: Object},
  data: () => ({
    openObject: [],
    contextMenu: { event: null, typeMenu: null,},
  }),
  computed: {
    ...mapGetters(['relationObject', 'objectTemplates', ]),
  },
  methods: {
    labelRootObject () {
      return 'Объект: ' + this.objectTemplates(this.object.objectId).title_single
    },
    labelObject (item) {
      let object = this.objectTemplates(item.object_id)
      let relation = this.relationObject(item.rel_id)
      let objectTitle = 'Объект: ' + object.title_single
      let relationTitle = relation ? relation.title: 'Отсутствует'
      return  objectTitle + '; Связь: ' + relationTitle
    },
    createNewRelation(selectedProperties) {
      this.contextMenu.typeMenu.rels.unshift({
        object_id: selectedProperties.selectedObject.id,
        rel_id: selectedProperties.selectedRelation ? selectedProperties.selectedRelation.id : 0,
        request: '',
        rels: [],
      },)
      this.openObject.push(this.contextMenu.typeMenu)
      this.deactivateContextMenu()
    },
  },
}
</script>

<style scoped>

</style>