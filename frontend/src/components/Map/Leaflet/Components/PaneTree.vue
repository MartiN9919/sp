<template>
  <v-treeview
    :items="items"
    :open="items_active"
    :active="items_active"
    @update:active="activate_item"
    hoverable
    activatable
    transition
    dense
    open-on-click
  >
    <template v-slot:prepend="{ item, open }">
      <v-icon
        :id="item.id"
        :size="$CONST.TREE.ICON_SIZE"
        :color="get_color(item)"
      >
        {{ get_icon(item, open) }}
      </v-icon>
    </template>
    <template v-slot:label="{ item, open }">
      <div
        class="v-treeview-node__label"
        :style="{'color': get_color(item)}"
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
    items_path: {},             // список id родительских узлов: {1: [1, 2, ...], ...}
    items_active: [],
  }),

  watch: {
    item_sel_prop: function(item_id) {
      this.activate_item(item_id);
    },
  },

  created: function() {
    this.ini_items();
    this.activate_item(this.item_sel);
  },

  computed: {
    item_sel: {
      get()   { return this.item_sel_prop; },
      set(id) { this.$emit('item_sel_change', id); },
    },
  },

  methods: {
    ini_items() {
      this.loop_items(this.items, [], function(item, path_id) {
        this.items_path[item.id] = path_id;
      }.bind(this));
    },

    // вызывать fun(item) для всех item, в т.ч. вложенных
    loop_items(items, path_id, fun) {
      for (let item of items) {
        const path_id_new = [...path_id, ...[item.id]]
        fun(item, path_id_new)
        if (item.children) this.loop_items(item.children, path_id_new, fun)
      }
    },

    activate_item(item_id) {
      this.item_sel = item_id;
      this.items_active = this.items_path[this.item_sel];
    },

    get_icon(item, open) {
      if (!item.children) return 'mdi-vector-polygon';
      if (open)           return this.$CONST.TREE.ICON_FOLDER_OPEN;
      return this.$CONST.TREE.ICON_FOLDER_CLOSE;
    },

    get_color(item) {
      return (
          (this.item_sel) &&
          (this.items_path[this.item_sel]) &&
          (this.items_path[this.item_sel].indexOf(item.id) !== -1)
        ) ? this.$CONST.TREE.COLOR_SELECT : this.$CONST.TREE.COLOR_DEFAULT;
    },

  },
}
</script>
