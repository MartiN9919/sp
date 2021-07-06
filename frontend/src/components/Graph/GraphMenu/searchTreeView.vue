<template>
  <div>
    <v-treeview :items="[treeItems]" item-children="rels" :open="openObject" return-object>
      <template v-slot:label="{ item }">
        <v-tooltip v-if="item !== treeItems" bottom transition="false" color="#00796B" z-index="10001" max-width="30%">
          <template v-slot:activator="{ on }">
            <v-text-field
              v-model="item.request" v-on="on" autocomplete="off"
              @contextmenu.stop="contextMenu = { event: $event, typeMenu: item, }"
              hide-details outlined dense class="mt-1" color="teal"
            >
              <template v-slot:label="">
                <v-icon size="20">{{ labelObject(item).icon }}</v-icon>
              </template>
            </v-text-field>
          </template>
          <table style="width:100%">
            <tr><th>Связь</th><td colspan="2">{{ labelRelation(item) }}</td></tr>
            <tr><th rowspan="3">Период</th></tr>
            <tr><th>Дата начала</th><th>Дата конца</th></tr>
            <tr><td>{{ labelPeriod(item).start }}</td><td>{{ labelPeriod(item).end }}</td></tr>
            <tr>
              <th>Поиск по актуальным значениям</th>
              <td colspan="2">
                <v-icon v-if="item.actual" color="green">mdi-check</v-icon>
                <v-icon v-else color="red">mdi-close</v-icon>
              </td>
            </tr>
          </table>
        </v-tooltip>
        <v-text-field
          v-else v-model="item.request" autocomplete="off"
          @contextmenu.stop="contextMenu = { event: $event, typeMenu: item, }"
          hide-details outlined dense class="mt-1" color="teal"
        >
          <template v-slot:append="">
            <span v-model="item.actual" class="pr-2 mt-1" style="color: #555555">Актуальность</span>
            <v-switch v-model="item.actual" hide-details color="teal" class="mt-0 pt-0"></v-switch>
          </template>
        </v-text-field>
      </template>
      <template v-slot:append="{ item, open }">
        <v-btn large icon v-if="item === treeItems" class="mt-2">
          <v-icon color="teal" @click="$emit('findObject')">mdi-magnify mdi-36px</v-icon>
        </v-btn>
      </template>
    </v-treeview>
    <context-menu v-if="typeMenu === typeContextMenu">
      <context-search-tree-view
        :parent-object="typeMenu === treeItems ? null : findParentObject()" :object="typeMenu"
        @createNewRelation="createNewRelation" @selectMenuItemTreeView="selectMenuItem"
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
      return this.$store.getters.primaryObject(item.object_id)
    },
    labelRelation (item) {
      let relation = this.$store.getters.relationObject(item.rel.id)
      let relationTitle = relation ? relation.title: 'Не выбрана'
      let relationValueTitle = ''
      if (relation?.list) {
        let relationValue = relation.list.find(i => i.id === item.rel.value)
        if (relationValue) relationValueTitle = '(' + relationValue.value + ')'
      }
      return relationTitle + relationValueTitle
    },
    labelPeriod (item) {
      let startDate = item.rel.date_time_start.date
      let startTime = item.rel.date_time_start.time
      let dateTimeStart = startDate || startTime ? startDate + ' ' + startTime : 'с самого начала'
      let dateTimeEnd = item.rel.date_time_end.date + ' ' + item.rel.date_time_end.time
      return { start: dateTimeStart, end: dateTimeEnd }
    },
    createNewRelation(selectedProperties) {
      let rel = {
        id: selectedProperties.selectedRelation ? selectedProperties.selectedRelation.id : 0,
        value: selectedProperties.value,
        date_time_start: selectedProperties.date_time_start,
        date_time_end: selectedProperties.date_time_end,
      }
      this.typeMenu.rels.unshift({
        object_id: selectedProperties.selectedObject.id,
        actual: selectedProperties.actual,
        request: '',
        rel: rel,
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

<style scoped>
table {
  border-collapse: collapse;
  table-layout: fixed;
  font-size: 0.80em;
  color: white;
  width: 100%;
}

th {
  text-align: center;
}
td, th {
  border: 1px solid white;
  padding-left: 5px;
  padding-right: 5px;
  padding-top: 2px;
  padding-bottom: 2px;
  white-space: pre-wrap;
}
</style>
