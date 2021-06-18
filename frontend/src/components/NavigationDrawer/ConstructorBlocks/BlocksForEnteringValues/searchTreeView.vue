<template>
  <v-container class="pa-0">
    <v-treeview :items="items" :open="open">
      <template v-slot:label="{ item, open }">
        <v-text-field
          @contextmenu="clickMenuItem(contextMenus.rightClickMenuObject, $event, item)"
          outlined dense color="teal" hide-details label="asdasd"
          :background-color="item.id !== 0 ? 'teal lighten-5' : ''" class="mt-2"
        ></v-text-field>
      </template>
      <template v-slot:append="{ item, open }">
        <v-btn large icon v-if="item.id === 0" class="mt-2">
          <v-icon color="teal">mdi-magnify mdi-36px</v-icon>
        </v-btn>
      </template>
    </v-treeview>
    <right-click-menu
        v-if="showContextMenu"
        @selectedItem="selectedMenuItem($event)"
    ></right-click-menu>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import rightClickMenu from "@/components/RightClickMenu/rightClickMenu";
import ActivatorContextMenu from "@/components/RightClickMenu/Mixins/ActivatorContextMenu";

export default {
  name: "searchTreeView",
  components: { rightClickMenu, },
  mixins: [ActivatorContextMenu, ],
  data: () => ({
    open: [],
    idItem: 0,
    selectedItem: {},
    items: [{ id: 0, children: [], label: 'Найти объект'}],
  }),
  computed: {
    ...mapGetters(['listObjects', ]),
    contextMenus: function () {
      return {
        rightClickMenuObject: [
          {
            type: 'actions1',
            body: [
              {type: 'action', title: 'Добавить объект для связи', icon: 'mdi-plus', next: 'lists1',},
              {type: 'action', title: 'Удалить объект', icon: 'mdi-delete-outline',},
            ],
          },
          {
            type: 'lists1',
            title: 'Выберете объект',
            body: [
              {type: 'list', title: 'Выберете объект', list: this.listObjects, next: "lists2"},
            ],
          },
          {
            type: 'lists2',
            title: 'Выберете связь между объектами',
            body: [
              {type: 'list', title: 'Выберете объект', list: this.listObjects,},
            ],
          },
        ],
      }
    },
  },
  methods: {
    clickMenuItem(menu, event, item) {
      this.selectedItem = item
      this.activateMenu(menu, event)
    },
    selectedMenuItem(event) {
      if (this.contextMenus.rightClickMenuObject.body.findIndex(e => e === event) === 1) {
        this.appendRelation()
      }
    },
    appendRelation() {
      this.idItem ++
      this.selectedItem.children.unshift({ id: this.idItem, children: [], })
      this.open.push(this.selectedItem.id)
    },
  }

}
</script>

<style scoped>

</style>