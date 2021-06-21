<template>
  <v-container class="pa-0">
    <v-treeview :items="items" :open="openObject" return-object>
      <template v-slot:label="{ item, open }">
        <v-text-field
          @contextmenu.stop="openContextMenu($event, 'searchTreeView', item)"
          outlined dense color="teal" hide-details
          :background-color="item.id !== 0 ? 'teal lighten-5' : ''" class="mt-2"
        ></v-text-field>
      </template>
      <template v-slot:append="{ item, open }">
        <v-btn large icon v-if="item.id === 0" class="mt-2">
          <v-icon color="teal">mdi-magnify mdi-36px</v-icon>
        </v-btn>
      </template>
    </v-treeview>
    <context-menu v-if="['searchTreeView', ].includes(typeContextMenu)">
      <graph-menu_cm :active-object="activeObject"></graph-menu_cm>
    </context-menu>
  </v-container>
</template>

<script>
import { mapActions } from "vuex";
import contextMenu from "@/components/ContextMenu/contextMenu";
import toolsContextMenu from "@/components/ContextMenu/Mixins/toolsContextMenu";
import graphMenu_cm from "../../../ContextMenu/BodysContextMenu/graphMenu_cm";

export default {
  name: "searchTreeView",
  components: {contextMenu, graphMenu_cm, },
  mixins: [ toolsContextMenu, ],
  props: {
    activeObject: Object,
  },
  data: () => ({
    selectedItem: null,
    openObject: [],
    items: [{ id: 0, children: [], label: 'Найти объект'}],
    contextMenu: {
      event: null,
      position: 'searchTreeView',
    },
  }),
  methods: {
    ...mapActions(['addRelations', ]),
    openContextMenu (event, typeMenu, selectedItem) {
      this.contextMenu = { event: event, typeMenu: typeMenu }
      this.selectedItem = selectedItem
    },
    appendRelation() {
      this.selectedItem.children.unshift({ children: [], })
      this.openObject.push(this.selectedItem)
    },
  },
}
</script>

<style scoped>

</style>