<template>
  <v-treeview
    ref="tree_view"
    :class="{ dd: true, flat: isFlat }"
    :items="items"
    :open="items_active"
    @update:active="item_sel_id = $event"
    hoverable
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
        @contextmenu="$emit('onMenuShow', $event, item)"
      >
        {{ get_icon(item, open) }}
      </v-icon>
    </template>
    <template v-slot:label="{ item, open }">
      <v-tooltip right open-delay="200" close-delay="300" transition="scroll-x-transition">
        <template v-slot:activator="{ on, attrs }">
          <v-hover v-slot="{ hover }">
            <v-list-item
              :id="'id_'+_uid+'_'+item.id"
              :style="{'color': get_color(item)}"
              class="v-treeview-node__label"
              @contextmenu="$emit('onMenuShow', $event, item)"
              v-bind="attrs"
              v-on="on"
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
        <EditorPreview
          :id="item.id"
          :name="item.name"
          :funGetFC="funGetFC"
        />
      </v-tooltip>
    </template>
  </v-treeview>
</template>
<script>
// v-treeview activatable показывать выделение
// <v-tooltip right open-delay="200" close-delay="300"> позиционирование карты по fc производится ТОЛЬКО на видимом окне

import EditorPreview from '@/components/Map/Leaflet/Components/Editor/EditorPreview';

export default {
  name: 'EditorNavTree',
  components: { EditorPreview },
  props: {
    //...EditorPreview.options.props,
    items:     { type: Array,    default: () => [], },
    itemSelId: { type: Number,   default: () => 0, },
    iconDef:   { type: String,   default: () => 'mdi-vector-polygon', }, // иконка по умолчанию
    isIcon:    { type: Boolean,  default: () => true, },                 // наличие иконок
    isFlat:    { type: Boolean,  default: () => false, },                // наличие отступов слева (как список)
    funGetFC:  { type: Function, default: () => undefined, },
  },
  emits: [
    'onNavNew',
    'onNavAdd',
    'onMenuShow',
    'update:itemSelId',
  ],

  data: () => ({
    items_path: {},             // список id родительских узлов: {1: [1, 2, ...], ...}
    items_active: [],
  }),

  watch: {
    items: function(items)   { this.ini_items(); },
    item_sel_id: function(item_id) {
      // развернуть tree
      if (this.items_path[item_id]) { this.items_active = this.items_path[item_id]; }
      setTimeout(function() {
        if (!this.find_item_id(item_id, this.items)) return;
        this.$vuetify.goTo(
          '#id_'+this._uid+'_'+item_id,
          { duration: 100, offset: 100, easing: 'easeInOutCubic', container: this.$refs.tree_view, }
        )
      }.bind(this), 100);
    },
  },

  computed: {
    item_sel_id: {
      get()   {
        return this.itemSelId;
      },
      set(item_id) {
        // click на выделенном item ==> item_id=[]
        if (item_id instanceof Object) {
          if (item_id.length>0) { item_id = item_id[0]; }
          else                  { item_id = this.item_sel_id; }
        }
        this.$emit('update:itemSelId', item_id);  // вызывает watch.item_sel_id
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

    // найти узел с id в items
    find_item_id(id, items) {
      let ret = undefined;
      for (const item of items) {
        if (item.id == id) { ret = item; break; }
        if (item.children) { ret = this.find_item_id(id, item.children); }
        if (ret)           { break; }
      }
      return ret;
    },

    on_new(item) {
      this.$emit('onNavNew', item.id, item.name);
    },

    on_add(item) {
      this.$emit('onNavAdd', item.id, item.name);
    },




    get_icon(item, open) {
      if (!item.children) return (item.icon)?item.icon:this.iconDef;
      if (open)           return this.$CONST.TREE.ICON_FOLDER_OPEN;
      return this.$CONST.TREE.ICON_FOLDER_CLOSE;
    },

    get_color(item) {
      return (
          (this.item_sel_id) &&
          (this.items_path[this.item_sel_id]) &&
          (this.items_path[this.item_sel_id].indexOf(item.id) !== -1)
        ) ? this.$CONST.TREE.COLOR_SELECT : this.$CONST.TREE.COLOR_DEFAULT;
    },

  },
}
</script>

<style scoped lang="scss">
  div::v-deep .btns { margin: 0 !important; display: block; }
  div::v-deep .btn { display: inline-block; top: 50%; transform: translate(0, -50%); }

  div::v-deep .v-list-item { min-height: 24px; padding: 0 2px; }

  div.flat::v-deep .v-treeview-node__level { display: none; width: 0 !important; }
  div.flat::v-deep .v-list-item { padding: 0 !important; }
  div.flat::v-deep .v-treeview-node__prepend { margin-right: 12px !important; }
  /* div.flat::v-deep .v-list-item__content { padding: 6px 0 !important; } */
</style>
