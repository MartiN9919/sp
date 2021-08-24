<template>
  <v-treeview
    ref="tree_view"
    :class="{ flat: isFlat }"
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
    <template v-slot:prepend="{ item, open }" v-if="isIcon">
      <v-icon
        :size="$CONST.TREE.ICON_SIZE"
        :color="get_color(item)"
      >
        {{ get_icon(item, open) }}
      </v-icon>
    </template>
    <template v-slot:label="{ item, open }">
      <v-list-item
        :id="'id_'+_uid+'_'+item.id"
        :style="{'color': get_color(item)}"
        class="v-treeview-node__label"
      >
        <v-list-item-content>
          <v-list-item-title v-text="item.name" :style="{'color': get_color(item)}"/>
          <v-list-item-subtitle v-text="item.address" :style="{'color': get_color(item)}"/>
        </v-list-item-content>
      </v-list-item>
    </template>
  </v-treeview>
</template>

<script>
// :active="items_active"
export default {
  name: 'Treeview',
  props: {
    items:   { type: Array,   default: () => [], },
    itemSel: { type: Number,  default: () => 0, },
    showSel: { type: Boolean, default: () => true, },
    iconDef: { type: String,  default: () => 'mdi-vector-polygon', }, // иконка по умолчанию
    isIcon:  { type: Boolean, default: () => true, },                 // наличие иконок
    isFlat:  { type: Boolean, default: () => false, },                // наличие отступов слева (как список)
  },
  // emits: ['update:itemSel', 'update:showSel', ], /// ?

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
      if (!item.children) return (item.icon)?item.icon:this.iconDef;
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
//div::v-deep .v-list-item { min-height: 24px !important; }
</script>

<style scoped lang="scss">
  .v-treeview { overflow-y: auto !important; height: 100%; }

  div::v-deep .v-list-item { min-height: 24px; padding: 0 2px; }

  div.flat::v-deep .v-treeview-node__level { display: none; width: 0 !important; }
  div.flat::v-deep .v-list-item__content { padding: 6px 0 !important; }
  div.flat::v-deep .v-list-item { padding: 0 !important; }
  div.flat::v-deep .v-treeview-node__prepend { margin-right: 12px !important; }
</style>
