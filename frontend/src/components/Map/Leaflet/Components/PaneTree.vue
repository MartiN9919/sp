<template>
  <v-treeview
    :items="items"
    @update:active="activateItem"
    hoverable
    activatable
    transition
    dense
    open-on-click
    return-object
  >
    <template v-slot:prepend="{ item, open }">
      <v-icon
        :id="item.id"
        :size="$CONST.TREE.ICON_SIZE"
        :color="getColor(item)"
      >
        {{ getIcon(item, open) }}
      </v-icon>
    </template>
    <template v-slot:label="{ item, open }">
      <div
        class="v-treeview-node__label"
        :style="{'color': getColor(item)}"
      >
        {{ item.name }}
      </div>
    </template>
  </v-treeview>
</template>

<script>

export default {
  name: 'PaneTree',
  model: { prop: 'item_sel_prop', event: 'item_sel_change', },
  props: {
    items: Array,
    item_sel_prop: Number,
  },

  data: () => ({
    items_path_id: {},
    items_parent: {},          // id родителя по id узла
    items_node:  {},           // узлел по его id
  }),

  watch: {
    item_sel_prop: function(item_id) {
      console.log(111, item_id);
      this.setActiveChain(item_id);
    },
  },

  mounted: function() {
    // построить словари по id
    this.items_step(this.items, [], function(item, path_id) {
      this.items_node[item.id] = item;
      this.items_path_id[item.id] = path_id;
      if (item.children) {
        for (const item_children of item.children) {
          this.items_parent[item_children.id] = item.id
        }
      }
    }.bind(this));

    //console.log(this.items_parent)
    console.log(this.items_path_id)
  },

  computed: {
    item_sel: {
      get()    { return this.item_sel_prop; },
      set(val) { this.$emit('item_sel_change', val); },
    },
  },

  methods: {
    // вызвать fun(item) для всех item, в т.ч. вложенных
    items_step(items, path_id, fun) {
      for (const item of items) {
        const path_id_new = [...path_id, ...[item.id]]
        fun(item, path_id_new)
        if (item.children) this.items_step(item.children, path_id_new, fun)
      }
    },

    getIcon(item, open) {
      if (!item.children) return 'mdi-vector-polygon';
      if (open)           return this.$CONST.TREE.ICON_FOLDER_OPEN;
      return this.$CONST.TREE.ICON_FOLDER_CLOSE;
    },

    getColor(item) {
      console.log(1)
      return ((this.items_path_id[item.id] != undefined) && (this.items_path_id[item.id].indexOf(this.item_sel) !== -1)) ? this.$CONST.TREE.COLOR_SELECT : this.$CONST.TREE.COLOR_DEFAULT;
    },

    activateItem (item) {
      if (!item) return;
      this.item_sel = item[0].id;
      // if (item.length) {
      //   /** Вызов родительского метода и передача ему глубокой копии выбранного скрипта */
      //   this.$emit('changeSelectedTreeViewItem', JSON.parse(JSON.stringify(item[0])))
      //   this.lastActiveItem = item[0]
      // } else {
      //   /** Вызов родительского метода и передача ему глубокой копии выбранного скрипта */
      //   this.$emit('changeSelectedTreeViewItem', JSON.parse(JSON.stringify(this.lastActiveItem)))
      //   this.lastActiveItem = null
      // }
    },

    setActiveChain(item_id) {
      this.items_active_chain = []
      // this.findItemInTreeView(item, this.treeViewItems)
      // this.listOpenFolder = this.listOpenFolder.concat(this.items_active_chain)
      // sleep(500).then(() => {
      //   this.$vuetify.goTo(
      //     '#' + this.iconId(item.id),
      //     { duration: 300, offset: 100, easing: 'easeInOutCubic', container: '.v-treeview' })
      // })
    },

  },
}
</script>
