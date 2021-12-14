<template>
  <v-treeview
    ref="tree_view"
    :class="{ flat: isFlat }"
    :items="items"
    :color="$CONST.APP.COLOR_OBJ"
    hoverable
    transition
    dense
    open-on-click
  >
    <template v-slot:prepend="{ item, open }" v-if="isIcon">
      <v-icon
        :size="$CONST.TREE.ICON_SIZE"
        :color="$CONST.TREE.COLOR_SELECT"
        @contextmenu="$emit('onMenuShow', $event, item)"
      >
        {{ get_icon(item, open) }}
      </v-icon>
    </template>
    <template v-slot:label="{ item, open }">
      <!-- позиционирование карты EditorPreview производится ТОЛЬКО на видимом окне -->
      <v-tooltip right open-delay="200" close-delay="400" transition="scroll-x-transition">
        <template v-slot:activator="{ on, attrs }">
          <v-hover v-slot="{ hover }">
            <v-list-item
              :id="'id_'+_uid+'_'+item.id"
              :disabled="is_disabled(item)"
              class="v-treeview-node__label"
              @contextmenu="$emit('onMenuShow', $event, item)"
              v-bind="attrs"
              v-on="on"
            >
              <v-list-item-content @click="on_new(item)">
                <v-list-item-title v-text="item.name"/>
                <v-list-item-subtitle v-text="item.address"/>
              </v-list-item-content>
              <v-list-item-action
                v-if="hover && !item.children"
                class="btns"
              >
                <v-btn class="btn" small icon>
                  <v-icon :color="$CONST.TREE.COLOR_SELECT" @click="on_add(item)">mdi-plus-circle-outline</v-icon>
                </v-btn>
                <!--
                <v-btn class="btn" small icon>
                  <v-icon @click="on_new(item)">mdi-chevron-right</v-icon>
                </v-btn>
                -->
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
// v-treeview @update:active="item_sel_id = $event"

import EditorPreview from '@/components/Map/Leaflet/Components/Editor/EditorPreview';

export default {
  name: 'EditorNavTree',
  components: { EditorPreview },
  props: {
    //...EditorPreview.options.props,
    items:     { type: Array,    default: () => [], },
    iconDef:   { type: String,   default: () => $CONST.ICON.OBJ.GEOMETRY, }, // иконка по умолчанию
    isIcon:    { type: Boolean,  default: () => true, },                     // наличие иконок
    isFlat:    { type: Boolean,  default: () => false, },                    // отсутствие отступов слева (как список)
    funGetFC:  { type: Function, default: () => undefined, },
  },
  emits: [
    'onNavNew',                 // event: установить геометрию
    'onNavAdd',                 // event: добавить геометрию
    'onMenuShow',               // event: контекстное меню, не обязательно
  ],

  watch: {
    items: function(items)   {
      this.$nextTick(function(){ this.$refs.tree_view.updateAll(true); });    // раскрыть узлы
    },
  },

  methods: {
    on_new(item) { if (item.id != undefined) { this.$emit('onNavNew', item.id, item.name) } },
    on_add(item) { if (item.id != undefined) { this.$emit('onNavAdd', item.id, item.name) } },

    is_disabled(item) {
      if (item.id == undefined) { return (item.children?.length == 0) }
      return false;
    },

    get_icon(item, open) {
      if (!item.children) return (item.icon)?item.icon:this.iconDef;
      if (open)           return this.$CONST.TREE.ICON_FOLDER_OPEN;
      return this.$CONST.TREE.ICON_FOLDER_CLOSE;
    },
  },
}
</script>

<style scoped lang="scss">
  div::v-deep .btns { margin: 0 !important; display: block; }
  div::v-deep .btn { display: inline-block; } /* для нескольких кнопок: top: 50%; transform: translate(0, -50%); */

  div::v-deep .v-list-item { min-height: 24px; padding: 0 2px; }

  div.flat::v-deep .v-treeview-node__level { display: none; width: 0 !important; }
  div.flat::v-deep .v-list-item { padding: 0 !important; }
  div.flat::v-deep .v-treeview-node__prepend { margin-right: 12px !important; }
  /* div.flat::v-deep .v-list-item__content { padding: 6px 0 !important; } */
</style>
