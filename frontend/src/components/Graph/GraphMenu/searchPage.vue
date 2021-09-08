<template>
  <v-col class="d-flex flex-column">
    <v-treeview :items="searchTreeItems" :open="openObject" item-children="rels" return-object class="search-tree pb-2">
      <template v-slot:label="{ item }">
        <span class="message-text-style v-messages">
          <v-icon size="15">{{item.object.icon}}</v-icon>
          {{item.getInformation()}}
          Актуальность:
          <v-icon size="15" :color="item.getInformationActual().color">
            {{item.getInformationActual().icon}}
          </v-icon>
        </span>
        <v-hover v-slot="{ hover }">
          <v-text-field v-model="item.request" dense outlined hide-details color="teal" autocomplete="off"
                        class="tree-item-input">
            <template v-slot:append-outer="">
              <v-btn v-if="item === searchTreeItems[0]" icon>
                <v-icon @click.stop="findObject" size="30">mdi-magnify</v-icon>
              </v-btn>
            </template>
            <template v-slot:append="">
              <div v-show="hover">
                <change-tree-item-btn
                  :item="item"
                  :parent-item="findParentObject(item)"
                  @change="changeItem(item, $event)"
                ></change-tree-item-btn>
                <create-tree-item-btn
                  :object-id="item.object.id"
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
    <found-objects
      v-if="foundObjects"
      :objects="foundObjects"
      @change="changeObject"
      @select="selectObject"
      class="overflow-y-hidden"
    ></found-objects>
  </v-col>
</template>

<script>
import ChangeTreeItemBtn from "./searchPageComponents/changeTreeItemBtn"
import CreateTreeItemBtn from "./searchPageComponents/createTreeItemBtn"
import FoundObjects from "./searchPageComponents/foundObjects"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "searchPage",
  components: {CreateTreeItemBtn, ChangeTreeItemBtn, FoundObjects},
  data: () => ({
    openObject: [],
  }),
  computed: {
    ...mapGetters(['searchTreeGraph', 'foundObjects']),
    searchTreeItems: function () { return this.searchTreeGraph ? [this.searchTreeGraph] : [] },
  },
  methods: {
    ...mapActions(['setRootSearchTreeItem', 'changeSearchTreeItem', 'setActiveTool', 'addSearchTreeItem',
    'findObjectsOnServer', 'removeSearchTreeItem', 'setEditableObject', 'getObjectFromServer', 'addObjectToGraph', 'getBaseClassifiers']),
    selectObject(object) {
      this.getObjectFromServer({params: {record_id: object.rec_id, object_id: object.object_id}})
        .then(response => { this.addObjectToGraph(response) })
    },
    changeObject(object) {
      this.getObjectFromServer({params: {record_id: object.rec_id, object_id: object.object_id}})
      .then(response => {
        this.setEditableObject(response)
        this.setActiveTool('createPage')
      })
    },
    findObject () {
      this.findObjectsOnServer()
    },
    deleteChildObject(removeItem) {
      let item = this.findParentObject(removeItem)
      this.removeSearchTreeItem({item, removeItem})
    },
    changeItem(item, newItem) {
      if(item === this.searchTreeItems[0])
        this.setRootSearchTreeItem({id: newItem.object_id, actual: newItem.actual})
      else this.changeSearchTreeItem({rootItem: item, newItem: newItem})
    },
    createItem(item, newItem) {
      this.addSearchTreeItem({rootItem: item, newItem: newItem})
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
.message-text-style {
  white-space: normal
}

.search-tree {
  max-height: 100%;
  overflow-y: auto;
  flex-shrink: 0;
}

.tree-item-input >>> .v-input__append-inner {
  margin-top: 2px !important;
}

.tree-item-input >>> .v-input__append-outer {
  margin-top: 2px !important;
}
</style>