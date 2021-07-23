<template>
  <div>
    <v-treeview :items="searchTreeItems" :open="openObject" return-object item-children="rels">
      <template v-slot:label="{ item }">
        <custom-tooltip v-if="item.rel">
          <template v-slot:activator="{ on }">
            <div v-on="on" @contextmenu.stop="createContextMenu(item, $event)">
              <tree-item v-model="item.request">
                <template v-slot:label>
                  <v-icon size="20">{{ labelObject(item.object_id).icon }}</v-icon>
                </template>
              </tree-item>
            </div>
          </template>
          <template v-slot:body>
            <tooltip-tree-item :item="item"></tooltip-tree-item>
          </template>
        </custom-tooltip>
        <tree-item v-else v-model="item.request" @contextmenu.native="createContextMenu(item, $event)">
          <template v-slot:label>
            <v-icon size="20">{{ labelObject(item.object_id).icon }}</v-icon>
          </template>
          <template v-slot:append="">
            <span v-model="item.actual" class="pr-2 mt-1" style="color: #555555">Актуальность</span>
            <v-switch v-model="item.actual" hide-details color="teal" class="mt-0 pt-0"></v-switch>
          </template>
          <template v-slot:append-outer="">
            <v-btn v-if="!item.rel" :loading="searchStatus" icon large>
              <v-icon @click="$emit('findObject')" color="teal">mdi-magnify</v-icon>
            </v-btn>
          </template>
        </tree-item>
      </template>
    </v-treeview>
    <context-menu v-if="typeMenu === typeContextMenu">
      <context-search-tree-view
        :object="typeMenu"
        :newObject="newObject"
        :parent-object="parentItem"
        @selectMenuItemTreeView="selectMenuItem"
        @createNewRelation="createNewRelation"
        @changeNewRelation="changeNewRelation"
        @deleteNewRelation="deleteNewRelation"
      ></context-search-tree-view>
    </context-menu>
  </div>
</template>

<script>
import contextMenu from "../../../WebsiteShell/ContextMenu/contextMenu"
import toolsContextMenu from "../../../WebsiteShell/ContextMenu/Mixins/toolsContextMenu"
import contextSearchTreeView from "../../ContextMenus/contextSearchTree/contextSearchTreeView"
import customTooltip from "../../../WebsiteShell/UI/customTooltip";
import tooltipTreeItem from "./tooltipTreeItem";
import TreeItem from "./treeItem";

export default {
  name: "searchTreeView",
  mixins: [ toolsContextMenu, ],
  components: {TreeItem, customTooltip, tooltipTreeItem, contextMenu, contextSearchTreeView, },
  props: {
    searchTree: Object,
    searchStatus: Boolean,
  },
  data: () => ({
    openObject: [],
    contextMenu: { event: null, typeMenu: null },
    newObject: null,
  }),
  computed: {
    typeMenu: function () { return this.contextMenu.typeMenu },
    mainSearchTreeItem: function () { return this.searchTreeItems[0] },
    parentItem: function () { return this.typeMenu === this.mainSearchTreeItem ? null : this.findParentObject() },
    searchTreeItems: function () {
      if (this.searchTree) {
        this.openObject = []
        this.openTree(this.searchTree)
        return [this.searchTree]
      }
      return []
    },
  },
  methods: {
    labelObject (id) { return this.$store.getters.primaryObject(id) },
    createNewRelation() {
      this.typeMenu.rels.unshift(this.newObject)
      this.openObject.push(this.typeMenu)
      this.deactivateContextMenu()
      this.newObject = null
    },
    changeNewRelation() {
      this.deactivateContextMenu()
      this.deleteNewRelation()
    },
    deleteNewRelation() {
      this.newObject = null
    },
    selectMenuItem (id) {
      switch(id) {
        case 1:
          if (!this.newObject)
            this.createNewObject()
          break
        case 2:
          this.deleteSearchTreeItem(this.mainSearchTreeItem)
          this.deactivateContextMenu()
          break
        case 3:
          this.changeObject()
          break
      }
    },
    openTree (root) {
      this.openObject.push(root)
      for (let item of root.rels)
        this.openTree(item)
    },
    deleteSearchTreeItem (body) {
      let findIndexObject = body.rels.findIndex(object => object === this.typeMenu)
      if (findIndexObject === -1)
        for (let object of body.rels)
          this.deleteSearchTreeItem(object)
      else body.rels.splice(findIndexObject, 1)
    },
    findParentObject (body=this.mainSearchTreeItem) {
      if (!body.rels.find(object => object === this.typeMenu)) {
        for (let object of body.rels) {
          let findParent = this.findParentObject(object)
          if (findParent) return findParent
        } return null
      } else return body
    },
    changeObject () {
      this.newObject = this.contextMenu.typeMenu
    },
    createNewObject () {
      this.newObject = {
        object_id: null,
        request: null,
        actual: false,
        rels: [],
        rel: {
          id: null,
          value: null,
          date_time_start: null,
          date_time_end: null,
        }
      }
    },
    createContextMenu (item, event) {
      this.contextMenu = { event: event, typeMenu: item, }
    },
  },
}
</script>

<style scoped>

</style>
