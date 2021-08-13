<template>
  <v-treeview
    ref="tree_view"
    :items="items"
    :open="items_active"
    @update:active="activate_item"
    hoverable
    activatable
    transition
    dense
    open-on-click
    active-class=""
    color=""
  >
    <template v-slot:prepend="{ item, open }">
      <v-icon
        :id="'id_'+_uid+'_'+item.id"
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
// :active="items_active"
export default {
  name: 'PaneTree',
  props: {
    items:   { type: Array,   default: () => [], },
    itemSel: { type: Number,  default: () => 0, },
    showSel: { type: Boolean, default: () => true, },
  },

  data: () => ({
    items_path: {},             // список id родительских узлов: {1: [1, 2, ...], ...}
    items_active: [],
  }),

  watch: {
    items:    function(items)   { this.ini_items(); },
    item_sel: function(item_id) { this.activate_item(item_id); },
    //showSel: function(val)     { },
  },

  computed: {
    item_sel: {
      get()   {
        return this.itemSel;
      },
      set(val) {
        let id = 0;
        if (val instanceof Object) { id = (val.length > 0) ? val[0] : 0; }
        else                       { id = val; }
        if (id == 0) return;

        if (this.items_path[id])   { this.items_active = this.items_path[id].slice(0, -1); } // .slice(0, -1) - нет эффекта
        if (this.item_sel != id)   { this.$emit('update:itemSel', id); }
      },
    },

    show_sel: {
      get()    { return this.showSel               },
      set(val) { this.$emit('update:showSel', val) },
    },
  },

  methods: {
    ini_items() {
      if (!this.items) return;
      this._loop_items_(this.items, [], function(item, path_id) {
        this.items_path[item.id] = path_id;
      }.bind(this));
    },

    // вызывать fun(item) для всех item, в т.ч. вложенных
    _loop_items_(items, path_id, fun) {
      for (let item of items) {
        const path_id_new = [...path_id, ...[item.id]]
        fun(item, path_id_new)
        if (item.children) this._loop_items_(item.children, path_id_new, fun)
      }
    },

    activate_item(item_id) {
      // когда click на item, который выделен, но не подсвечивается (item_id==[])
      if ((item_id.length==0) && (this.item_sel>0)) {
        item_id       = this.item_sel;
        this.show_sel = true;
      } else {
        this.item_sel = item_id;
      }

      setTimeout(function() {
        this.$vuetify.goTo(
          '#id_'+this._uid+'_'+item_id,
          { duration: 100, offset: 100, easing: 'easeInOutCubic', container: this.$refs.tree_view, }
        )
      }.bind(this), 100);
    },

    get_icon(item, open) {
      if (!item.children) return (item.icon)?item.icon:'mdi-vector-polygon';
      if (open)           return this.$CONST.TREE.ICON_FOLDER_OPEN;
      return this.$CONST.TREE.ICON_FOLDER_CLOSE;
    },

    get_color(item) {
      return (
          (this.item_sel) &&
          (this.items_path[this.item_sel]) &&
          (this.items_path[this.item_sel].indexOf(item.id) !== -1) &&
          (
            (this.items_path[this.item_sel].slice(-1)[0] != item.id) ||
            ((this.items_path[this.item_sel].slice(-1)[0] == item.id) && (this.showSel))
          )
        ) ? this.$CONST.TREE.COLOR_SELECT : this.$CONST.TREE.COLOR_DEFAULT;
    },

  },
}
</script>
