<template>
  <v-treeview :items="items" :open="openItems" item-children="rels" return-object class="search-tree">
    <template v-slot:label="{ item }">
      <item-description :item="item"/>
      <v-hover v-slot="{ hover }">
        <search-tree-item :item="item" :base="item === items[0]" @find="find" :relation="!!item.recId" class="pb-2">
          <div v-show="hover">
            <btn-create v-if="item.objects.length === 1" :object-id="item.objects[0].id" @create="create(item, $event)"/>
            <btn-change v-if="!item.recId" :item="item" :parent="findParent(item)" @change="change(item, $event)"/>
            <btn-remove v-if="item !== items[0]" @remove="remove(item)"/>
          </div>
        </search-tree-item>
      </v-hover>
    </template>
  </v-treeview>
</template>

<script>
import SearchTreeItem from "@/components/Graph/GraphMenu/Search/SearchTree/SearchTreeItem"
import ItemDescription from "@/components/Graph/GraphMenu/Search/SearchTree/ItemDescription"
import BtnCreate from "@/components/Graph/GraphMenu/Search/SearchTree/ControllBtns/BtnCreate"
import BtnChange from "@/components/Graph/GraphMenu/Search/SearchTree/ControllBtns/BtnChange"
import BtnRemove from "@/components/Graph/GraphMenu/Search/SearchTree/ControllBtns/BtnRemove"
import {mapActions} from "vuex";

export default {
  name: "SearchTree",
  components: {BtnRemove, BtnChange, BtnCreate, SearchTreeItem, ItemDescription},
  props: {
    tree: Object,
    find: Function,
  },
  data: () => ({
    openItems: [],
  }),
  computed: {
    items: function () {
      return this.tree ? [this.tree] : []
    }
  },
  methods: {
    ...mapActions(['setRootSearch', 'changeSearchTreeItem', 'addSearchTreeItem', 'removeSearchTreeItem']),
    create(item, newItem) {
      this.addSearchTreeItem({rootItem: item, newItem: newItem})
      this.openItems.push(item)
    },
    change(item, newItem) {
      if(item === this.items[0])
        this.setRootSearch(newItem)
      else this.changeSearchTreeItem({rootItem: item, newItem: newItem})
    },
    remove(removeItem) {
      let item = this.findParent(removeItem)
      this.removeSearchTreeItem({item, removeItem})
    },
    findParent(item, body = this.items[0]) {
      if (!body.rels.find(object => object === item)) {
        for (let object of body.rels) {
          let findParent = this.findParent(item, object)
          if (findParent) {
            return findParent
          }
        }
        return null
      } else {
        return body
      }
    },
  }
}
</script>

<style scoped>
.search-tree {
  max-height: 100%;
  overflow-y: auto;
  flex-shrink: 0;
}
</style>