<template>
  <v-treeview
    :items="items"
    :open="openObject"
    return-object
    item-children="rels"
  >
    <template v-slot:label="{ item }">
      <root-tree-item
        v-if="item === searchTree"
        :object="item"
        @createNewObject="createNewObject($event)"
        @changeRootObject="changeRootObject"
      >
        <template v-slot:append-outer>
          <v-btn icon>
            <v-icon @click.stop="findObject" size="30">mdi-magnify</v-icon>
          </v-btn>
        </template>
      </root-tree-item>
      <child-tree-item
        v-else
        :object="item"
        :parent-object="findParentObject(item)"
        @createNewObject="createNewObject($event, item)"
        @changeChildObject="changeChildObject(item, $event)"
        @deleteChildObject="deleteChildObject(item)"
      ></child-tree-item>
    </template>
  </v-treeview>
</template>

<script>
import RootTreeItem from "./treeItems/rootTreeItem"
import ChildTreeItem from "./treeItems/childTreeItem"
import {mapActions} from "vuex"

export default {
  name: "searchTree",
  components: { ChildTreeItem, RootTreeItem, },
  props: {
    searchTree: Object,
  },
  model: {
    prop: 'searchTree',
    event: 'changeSearchTree',
  },
  data: () => ({
    openObject: [],
  }),
  computed: {
    items: {
      get: function () { return this.searchTree ? [this.searchTree] : [] },
      set: function (value) { return value[0] },
    },
  },
  methods: {
    ...mapActions(['setRootSearchTreeGraph', ]),
    createNewObject(newObject, item=this.items[0]) {
      item.rels.unshift(newObject)
      this.openObject.push(item)
    },
    changeRootObject(newData) {
      this.setRootSearchTreeGraph(newData)
    },
    changeChildObject(object, newData) {
      if (object.object_id !== newData.object_id) {
        object.request = ''
        object.object_id = newData.object_id
      }
      object.actual = newData.actual
      object.rel = newData.rel
      object.rels = newData.rels
    },
    deleteChildObject(object) {
      this.deleteSearchTreeItem(object)
    },
    findParentObject (item, body=this.searchTree) {
      if (!body.rels.find(object => object === item)) {
        for (let object of body.rels) {
          let findParent = this.findParentObject(item, object)
          if (findParent) return findParent
        } return null
      } else return body
    },
    deleteSearchTreeItem (item, body=this.searchTree) {
      let findIndexObject = body.rels.findIndex(object => object === item)
      if (findIndexObject === -1)
        for (let object of body.rels)
          this.deleteSearchTreeItem(item, object)
      else body.rels.splice(findIndexObject, 1)
    },
    findObject() {
      this.$emit('findObject')
    }
  }
}
</script>

<style scoped>

</style>