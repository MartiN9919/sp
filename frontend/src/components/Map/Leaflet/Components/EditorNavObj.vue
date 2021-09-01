<template>

  <v-card>
    <v-text-field
      ref="inp"
      style="margin: 15px;"
      :color="$CONST.APP.COLOR_OBJ"
      label="Искать"
      @input="on_search"
      dense
      outlined
      hide-details
      clearable
      autofocus
    >
      <template v-slot:append >
        <v-btn
          v-show="btn_show"
          :disabled="btn_prev_disabled"
          @click="on_click_btn_prev"
          icon
        >
          <v-icon size="24" :color="$CONST.APP.COLOR_OBJ">mdi-arrow-left-bold</v-icon>
        </v-btn>
        <v-btn
          v-show="btn_show"
          :disabled="btn_next_disabled"
          @click="on_click_btn_next"
          icon
        >
          <v-icon size="24" :color="$CONST.APP.COLOR_OBJ">mdi-arrow-right-bold</v-icon>
        </v-btn>
    </template>
    </v-text-field>

    <v-divider class="mx-4"></v-divider>

    <div
      @contextmenu="on_menu_show($event)"
    >

      <Treeview
        class="tree"
        :items="items"
        :itemSelId.number.sync="item_sel_id"
        @onNavNew="on_nav_new"
        @onNavAdd="on_nav_add"
        @onMenuShow="on_menu_show"
      />

      <contextMenuNested
        ref="menu_obj"
        :form="form"
        :items="menu_struct"
      />

      <v-dialog
        v-model="menu_dialog_show"
        max-width="400px"
        style="z-index: 10000002"
        @keydown.enter="on_menu_dialog_ok"
        @keydown.esc="menu_dialog_show = false"
        transition="dialog-bottom-transition"
        persistent
      >
        <v-card>
          <v-card-title>Название объекта</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-text-field
              ref="input_nam"
              v-model="menu_dialog_name"
              required
              autofocus
            />
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn :color="$CONST.APP.COLOR_OBJ" text @click="menu_dialog_show = false">Отмена</v-btn>
            <v-btn :color="$CONST.APP.COLOR_OBJ" text @click="on_menu_dialog_ok" :disabled="is_disabled_menu_dialog_ok()">Ок</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog
        v-model="menu_dialog_agree_show"
        max-width="600px"
        style="z-index: 10000003"
        @keydown.enter=""
        @keydown.esc="menu_dialog_agree_show = false"
        transition="dialog-bottom-transition"
        persistent
      >
        <v-card>
          <v-card-title>Подтвердите операцию</v-card-title>
          <v-divider></v-divider>
          <v-card-text>

            <v-checkbox
              ref="input_agree"
              v-model="menu_dialog_agree_val"
              :label="menu_dialog_agree_title"
              color="warning"
              value="true"
              hide-details
            ></v-checkbox>

          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn :color="$CONST.APP.COLOR_OBJ" text @click="menu_dialog_agree_show = false">Отмена</v-btn>
            <v-btn :color="$CONST.APP.COLOR_OBJ" text @click="on_menu_dialog_agree_ok" :disabled="!menu_dialog_agree_val">Ок</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    </div>

  </v-card>
</template>

<script>
/*
 * КОМПОНЕНТ: ДЕРЕВО ГЕОМЕТРИЙ
 *  <EditorNavObj
 *    localStorageKeyPostfix="key_name"
 *    @onNavNew=""
 *    @onNavAdd=""
 *  />
 *
 *  update_fc(fc) { },
 *  @update_fc  - событие при изменении на карте fc
 */

import router from '@/router';
import { getResponseAxios } from '@/plugins/axios_settings';
import Treeview from '@/components/Map/Leaflet/Components/Treeview';
import MixMenuNavObj from '@/components/Map/Leaflet/Mixins/MenuNavObj';
import { fc_normalize, } from '@/components/Map/Leaflet/Lib/LibFc';


export default {
  name: 'editor-nav-obj',
  components: { Treeview, },
  mixins: [ MixMenuNavObj, ],

  props: {
    localStorageKeyPostfix: { type: String, default() { return '' } },
    fc: Object,
  },
  emits: [
    'onNavNew',
    'onNavAdd',
  ],

  data: () => ({
    items:             [],
    item_sel_id:       0,
    items_search_list: [],
    items_search_id:   undefined,

    btn_show:          false,
    btn_prev_disabled: true,
    btn_next_disabled: true,
  }),

  computed: {
    key_sel() { return router.currentRoute.name + '_editor_nav_obj_sel_' + this.localStorageKeyPostfix },
  },

  watch: {
    item_sel_id: function(id) {
      localStorage[this.key_sel] = id;
    },
  },

  created: function() { this.refresh_items(); },

  methods: {
    refresh_items() {
      getResponseAxios(this.$CONST.API.OBJ.GEOMETRY_TREE)
        .then(response => {
          // get data
          this.items = response.data;
          if (localStorage[this.key_sel]) { this.item_sel_id = parseInt(localStorage[this.key_sel]); }

          // // watch fix bug
          // this.$watch('item_sel_id', function(id) {
          //   localStorage[this.key_sel] = id;
          // });

          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) });
    },

    on_nav_new(id, name) { this.on_nav(id, name, 'onNavNew') },
    on_nav_add(id, name) { this.on_nav(id, name, 'onNavAdd') },
    on_nav(id, name, emit_name) {
      getResponseAxios(this.$CONST.API.OBJ.GEOMETRY, { params: {rec_id: id,} })
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
        this.item_sel_id = this.items_search_list[this.items_search_id].id;
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

  },

}
</script>

<style scoped lang="scss">
  div::v-deep .v-input__append-inner:nth-of-type(3) { margin-top: 2px !important; }
  div.tree::v-deep { overflow-y: auto !important; height: calc( 100% - 120px ); } /*calc( 100% - 50px );*/
</style>
