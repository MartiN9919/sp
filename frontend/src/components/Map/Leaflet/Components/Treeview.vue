<template>
  <v-treeview
    ref="tree_view"
    :class="{ flat: isFlat }"
    :items="items"
    :open="items_active"
    @update:active="sel_item"
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
      <v-hover v-slot="{ hover }">
        <v-list-item
          :id="'id_'+_uid+'_'+item.id"
          :style="{'color': get_color(item)}"
          class="v-treeview-node__label"
        >
          <v-list-item-content>
            <v-list-item-title v-text="item.name" :style="{'color': get_color(item)}"/>
            <v-list-item-subtitle v-text="item.address" :style="{'color': get_color(item)}"/>
          </v-list-item-content>
          <v-list-item-action
            v-if="hover && !item.children"
            class="btns"
          >
            <v-btn class="btn" small icon>
              <v-icon @click="on_add(item)">mdi-plus-circle-outline</v-icon>
            </v-btn>
            <v-btn class="btn" small icon>
              <v-icon @click="on_new(item)">mdi-chevron-right</v-icon>
            </v-btn>
          </v-list-item-action>
        </v-list-item>
      </v-hover>
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
    iconDef: { type: String,  default: () => 'mdi-vector-polygon', }, // иконка по умолчанию
    isIcon:  { type: Boolean, default: () => true, },                 // наличие иконок
    isFlat:  { type: Boolean, default: () => false, },                // наличие отступов слева (как список)
  },
  emits: [
    'onNew',
    'onAdd',
    //'update:itemSel',
  ],

  data: () => ({
    items_path: {},             // список id родительских узлов: {1: [1, 2, ...], ...}
    items_active: [],
  }),

  watch: {
    items:    function(items)   { this.ini_items(); },
    item_sel: function(item_id) { this.sel_item(item_id); },
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




    sel_item(item_id) {
      // click на выделенном item ==> item_id=[]
      if ((item_id.length==0) && (this.item_sel>0)) { item_id = this.item_sel }
      else                                          { this.item_sel = item_id }

      setTimeout(function() {
        this.$vuetify.goTo(
          '#id_'+this._uid+'_'+item_id,
          { duration: 100, offset: 100, easing: 'easeInOutCubic', container: this.$refs.tree_view, }
        )
      }.bind(this), 100);
    },

    on_new(item) {
      this.$emit('onNew', item.id, item.name);
    },

    on_add(item) {
      this.$emit('onAdd', item.id, item.name);
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
          (this.items_path[this.item_sel].indexOf(item.id) !== -1)
        ) ? this.$CONST.TREE.COLOR_SELECT : this.$CONST.TREE.COLOR_DEFAULT;
    },

  },
}
</script>

<style scoped lang="scss">
  .v-treeview { overflow-y: auto !important; height: 100%; }

  div::v-deep .btns { margin: 0 !important; display: block; }
  div::v-deep .btn { display: inline-block; top: 50%; transform: translate(0, -50%); }

  div::v-deep .v-list-item { min-height: 24px; padding: 0 2px; }

  div.flat::v-deep .v-treeview-node__level { display: none; width: 0 !important; }
  div.flat::v-deep .v-list-item { padding: 0 !important; }
  div.flat::v-deep .v-treeview-node__prepend { margin-right: 12px !important; }
  /* div.flat::v-deep .v-list-item__content { padding: 6px 0 !important; } */
</style>
