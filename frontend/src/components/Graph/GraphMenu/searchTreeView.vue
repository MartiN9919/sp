<template>
  <div>
    <v-treeview
      :items="[treeItems]" item-children="rels" return-object
      :open="openObject" open-all class="py-1"
    >
      <template v-slot:label="{ item }">
        <v-text-field
          v-model="item.request" :label="item === treeItems ? '' : labelObject(item)"
          @contextmenu.stop="contextMenu = { event: $event, typeMenu: item, }"
          hide-details outlined dense autocomplete="off" class="mt-2" color="teal"
        ></v-text-field>
      </template>
      <template v-slot:append="{ item, open }">
        <v-btn large icon v-if="item === treeItems" class="mt-2">
          <v-icon color="teal" @click="$emit('findObject')">mdi-magnify mdi-36px</v-icon>
        </v-btn>
      </template>
    </v-treeview>
    <context-menu v-if="typeMenu === typeContextMenu">
      <context-search-tree-view
        :parent-object="typeMenu === treeItems ? null : findParentObject()"
        :object="typeMenu"
        @createNewRelation="createNewRelation"
        @selectMenuItemTreeView="selectMenuItem"
      ></context-search-tree-view>
    </context-menu>
  </div>
</template>

<script>
import contextMenu from "../../WebsiteShell/ContextMenu/contextMenu"
import toolsContextMenu from "../../WebsiteShell/ContextMenu/Mixins/toolsContextMenu"
import contextSearchTreeView from "../ContextMenus/contextSearchTreeView/contextSearchTreeView"

export default {
  name: "searchTreeView",
  mixins: [ toolsContextMenu, ],
  components: {contextMenu, contextSearchTreeView, },
  props: { searchTree: Object, },
  model: { prop: 'searchTree', event: 'changeSearchTree', },
  data: () => ({
    openObject: [],
    contextMenu: { event: null, typeMenu: null,},
  }),
  computed: {
    treeItems: {
      get: function () { return this.searchTree },
      set: function (tree) { this.$emit('changeSearchTree', tree) },
    },
    typeMenu: function () { return this.contextMenu.typeMenu },
  },
  methods: {
    labelObject (item) {
      let relation = this.$store.getters.relationObject(item.rel_id)
      let relationTitle = relation ? relation.title: 'Отсутствует'
      return this.$store.getters.primaryObject(item.object_id).title_single + ': ' + relationTitle
    },
    createNewRelation(selectedProperties) {
      this.typeMenu.rels.unshift({
        object_id: selectedProperties.selectedObject.id,
        rel_id: selectedProperties.selectedRelation ? selectedProperties.selectedRelation.id : 0,
        request: '',
        rels: [],
      },)
      this.openObject.push(this.typeMenu)
      this.deactivateContextMenu()
    },
    selectMenuItem (item) {
      if (item.id === 2)
        this.deleteSearchTreeItem(this.treeItems)
      this.deactivateContextMenu()
    },
    deleteSearchTreeItem (body) {
      let findIndexObject = body.rels.findIndex(object => object === this.typeMenu)
      if (findIndexObject === -1)
        for (let object of body.rels)
          this.deleteSearchTreeItem(object)
      else body.rels.splice(findIndexObject, 1)
    },
    findParentObject (body=this.treeItems) {
      if (!body.rels.find(object => object === this.typeMenu)) {
        for (let object of body.rels) {
          let findParent = this.findParentObject(object)
          if (findParent) return findParent
        } return null
      } else return body
    }
  },
}
</script>
