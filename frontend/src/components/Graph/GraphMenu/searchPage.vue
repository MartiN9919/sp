<template>
  <v-col>
    <v-treeview :items="searchTreeItems" :open="openObject" item-children="rels" return-object class="search-tree pb-2">
      <template v-slot:label="{ item }">
        <tree-item-info :object="item"></tree-item-info>
        <v-hover v-slot="{ hover }">
          <v-text-field v-model="item.request" dense outlined hide-details color="teal" autocomplete="off"
                        class="treeItemInput">
            <template v-slot:append-outer="">
              <v-btn v-if="item === searchTreeItems[0]" icon>
                <v-icon @click.stop="findObject" size="30">mdi-magnify</v-icon>
              </v-btn>
            </template>
            <template v-slot:append="">
              <div v-show="hover">
                <change-tree-item-btn
                  :object="item"
                  :parent-object="findParentObject(item)"
                  @change="changeItem(item, $event)"
                ></change-tree-item-btn>
                <create-tree-item-btn
                  :object-id="item.object_id"
                  @create="createItem(item, $event)"
                ></create-tree-item-btn>
                <v-btn
                  v-if="item !== searchTreeItems[0]"
                  icon @click="deleteChildObject(item)"
                ><v-icon>mdi-delete</v-icon></v-btn>
              </div>
            </template>
          </v-text-field>
        </v-hover>
      </template>
    </v-treeview>
    <found-objects v-if="foundObjects" :objects="foundObjects"></found-objects>
  </v-col>
</template>

<script>
import TreeItemInfo from "./searchPageComponents/treeItemInfo"
import ChangeTreeItemBtn from "./searchPageComponents/changeTreeItemBtn"
import CreateTreeItemBtn from "./searchPageComponents/createTreeItemBtn"
import FoundObjects from "./searchPageComponents/foundObjects"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "searchPage",
  components: {CreateTreeItemBtn, ChangeTreeItemBtn, TreeItemInfo, FoundObjects},
  data: () => ({
    openObject: [],
  }),
  computed: {
    ...mapGetters(['searchTreeGraph', 'foundObjects']),
    searchTreeItems: function () { return this.searchTreeGraph ? [this.searchTreeGraph] : [] },
  },
  methods: {
    ...mapActions(['setRootSearchTreeGraph', 'changeItemSearchTreeGraph', 'setNewItemSearchTreeGraph', 'findObjectsOnServer', 'removeItemSearchTreeGraph']),
    findObject () {
      this.findObjectsOnServer()
    },
    deleteChildObject(removeItem) {
      let item = this.findParentObject(removeItem)
      this.removeItemSearchTreeGraph({item, removeItem})
    },
    changeItem(item, newItem) {
      if(item === this.searchTreeItems[0])
        this.setRootSearchTreeGraph({objectId: newItem.object_id, actual: newItem.actual})
      else
        this.changeItemSearchTreeGraph({item, newItem})
    },
    createItem(item, newItem) {
      this.setNewItemSearchTreeGraph({item, newItem})
      this.openObject.push(item)
    },
    findParentObject(item, body = this.searchTreeItems[0]) {
      if (!body.rels.find(object => object === item)) {
        for (let object of body.rels) {
          let findParent = this.findParentObject(item, object)
          if (findParent) return findParent
        }
        return null
      } else return body
    },
  },
}
</script>

<style scoped>
.search-tree {
  max-height: 100%;
  overflow-y: auto;
}

.treeItemInput >>> .v-input__append-inner {
  margin-top: 2 !important;
}

.treeItemInput >>> .v-input__append-outer {
  margin-top: 2 !important;
}
</style>