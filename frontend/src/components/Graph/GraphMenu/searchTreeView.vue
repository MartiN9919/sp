<template>
  <v-container class="pa-0">
    <v-treeview
      :items="[object.searchTree]" item-children="rels"
      :open="openObject" open-all  return-object expand-icon=""
      style="margin-left: -1.2em"
    >
      <template v-slot:label="{ item, open }">
        <v-text-field
          autocomplete="off"
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
        :parent-object="contextMenu.typeMenu === object.searchTree ? null : findParentObject()"
        :object="contextMenu.typeMenu"
        @createNewRelation="createNewRelation"
        @selectMenuItem="selectMenuItem"
      ></context-search-tree-view>
    </context-menu>
  </v-container>
</template>

<script>
import contextMenu from "../../WebsiteShell/ContextMenu/contextMenu"
import toolsContextMenu from "../../WebsiteShell/ContextMenu/Mixins/toolsContextMenu"
import contextSearchTreeView from "../ContextMenus/contextSearchTreeView/contextSearchTreeView"
import { mapGetters } from "vuex";

export default {
  name: "searchTreeView",
  components: {contextMenu, contextSearchTreeView, },
  mixins: [ toolsContextMenu, ],
  props: { object: Object, },
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
    selectMenuItem (item) {
      if (item.id === 2)
        if (this.contextMenu.typeMenu !== this.object.searchTree)
          this.deleteSearchTreeItem(this.object.searchTree)
      this.deactivateContextMenu()
    },
    deleteSearchTreeItem (body) {
      let findIndexObject = body.rels.findIndex(object => object === this.contextMenu.typeMenu)
      if (findIndexObject === -1)
        for (let object of body.rels)
          this.deleteSearchTreeItem(object)
      else body.rels.splice(findIndexObject, 1)
    },
    findParentObject (body=this.object.searchTree) {
      if (!body.rels.find(object => object === this.contextMenu.typeMenu)) {
        for (let object of body.rels) {
          let findParent = this.findParentObject(object)
          if (findParent) return findParent
        }
        return null
      } else return body
    }
  },
}
</script>

<style scoped>

</style>