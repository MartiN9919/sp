<template>

  <v-card>
    <v-text-field
      ref="inp"
      style="padding: 15px;"
      :color="$CONST.APP.COLOR_OBJ"
      label="Искать"
      @input="on_search"
      @focus="on_focus(true)"
      @blur="on_focus(false)"
      dense
      outlined
      hide-details
      clearable
      autofocus
    >
      <template v-slot:append>
        <v-btn
          v-show="btn_show"
          :disabled="btn_prev_disabled"
          @click="on_click_btn_prev"
          icon
        >
          <v-icon size="24" :color="btn_color">mdi-arrow-left-bold</v-icon>
        </v-btn>
        <v-btn
          v-show="btn_show"
          :disabled="btn_next_disabled"
          @click="on_click_btn_next"
          icon
        >
          <v-icon size="24" :color="btn_color">mdi-arrow-right-bold</v-icon>
        </v-btn>
    </template>
    </v-text-field>

    <v-divider class="mx-4"></v-divider>

    <EditorTree
      class="tree"
      style="height: calc(100% - 70px);"
      :items="items"
      :itemSelId.number.sync="item_sel_id.value"
      @onNavNew="on_nav_new"
      @onNavAdd="on_nav_add"
      @onMenuShow=""
    />

  </v-card>
</template>

<script>
/*
 * КОМПОНЕНТ: ДЕРЕВО ГЕОМЕТРИЙ
 *  <EditorNavObj
 *    @onNavNew=""
 *    @onNavAdd=""
 *  />
 */

import router from '@/router';
import UserSetting from "@/store/addition"
import axios from '@/plugins/axiosSettings';
import EditorTree from '@/components/Map/Leaflet/Components/Editor/EditorTree';
import SelectorInput from "@/components/WebsiteShell/InputForms/selectorInput"
import { fc_normalize, } from '@/components/Map/Leaflet/Lib/LibFc';


export default {
  name: 'editor-nav-obj',
  components: { EditorTree, SelectorInput, },

  emits: [
    'onNavNew',
    'onNavAdd',
  ],

  data: () => ({
    items:             [],
    item_sel_id:       new UserSetting('EditorNavObj.item_sel_id', 0),
    items_search_list: [],
    items_search_id:   undefined,

    btn_show:          false,
    btn_color:         undefined,
    btn_prev_disabled: true,
    btn_next_disabled: true,
  }),

  created: function() { this.refresh_items(); },

  methods: {
    refresh_items() {
      axios.get(this.$CONST.API.OBJ.GEOMETRY_TREE)
        .then(response => {
          this.items = response.data;
          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) });
    },

    on_nav_new(id, name) { this.on_nav(id, name, 'onNavNew') },
    on_nav_add(id, name) { this.on_nav(id, name, 'onNavAdd') },
    on_nav(id, name, emit_name) {
      axios.get(this.$CONST.API.OBJ.GEOMETRY, { params: {rec_id: id,} })
        .then(response => {
          this.$emit(emit_name, id, name, fc_normalize(response.data));
          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) });
    },



    on_search(val) {
      val = ((val === undefined) || (val == null)) ? '' : val.trim();

      this.items_search_list = (val != '') ? this.find_items_name(val, this.items) : [];
      this.set_items_search_id(0);

      this.btn_show          = (val != '');
      this.btn_prev_disabled = (this.items_search_list.length < 2);
      this.btn_next_disabled = (this.items_search_list.length < 2);
    },
    // найти все узлы с *name* в items
    find_items_name(name, items) {
      let ret = [];
      let r = RegExp(name, 'i')
      for (const item of items) {
        if (item.name.match(r)) { ret.push(item); }
        if (item.children)      { ret = ret.concat(this.find_items_name(name, item.children)); }
      }
      return ret;
    },

    set_items_search_id(val) {
      if ((this.items_search_list.length == 0) || (val == undefined)) {
        this.items_search_id = undefined;
        return;
      }
      this.items_search_id = val;
      if ((this.items_search_id >= 0) && (this.items_search_id < this.items_search_list.length)) {
        this.item_sel_id.value = this.items_search_list[this.items_search_id].id;
      }
    },

    on_click_btn_next() {
      this.set_items_search_id(
        (this.items_search_id < this.items_search_list.length-1) ?
        this.items_search_id+1 :
        0
      );
    },
    on_click_btn_prev() {
      this.set_items_search_id(
        (this.items_search_id > 0) ?
        this.items_search_id-1 :
        this.items_search_list.length-1
      );
    },



    on_focus(val) {
      this.btn_color = (val) ? this.$CONST.APP.COLOR_OBJ : 'grey darken-1';
    },


  },

}
</script>

<style scoped lang="scss">
  div::v-deep .v-input__append-inner:nth-of-type(3) { margin-top: 2px !important; }
  div.tree::v-deep { overflow-y: auto !important; height: 100%; } /*calc( 100% - 50px );*/
</style>
