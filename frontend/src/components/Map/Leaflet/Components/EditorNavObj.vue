<template>
  <div
    @contextmenu="on_menu_show($event)"
  >

    <Treeview
      class="tree"
      :items="items"
      :itemSel.number.sync="item_sel"
      @onNavNew="on_nal_new"
      @onNavAdd="on_nav_add"
      @onMenuShow="on_menu_show"
    />

    <contextMenuNested
      ref="menu_obj"
      :form="form"
      :items="menu_struct"
    />

  </div>
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
import MixMenuObj from '@/components/Map/Leaflet/Mixins/MenuObj';
import { fc_normalize, } from '@/components/Map/Leaflet/Lib/Lib';


export default {
  name: 'editor-nav-obj',
  components: { Treeview, },
  mixins: [ MixMenuObj, ],

  props: {
    localStorageKeyPostfix: { type: String, default() { return '' } },
    fc: Object,
  },
  emits: [
    'onNavNew',
    'onNavAdd',
  ],

  data: () => ({
    items:    [],
    item_sel: 0,
  }),

  created: function() {
    getResponseAxios(this.$CONST.API.OBJ.GEOMETRY_TREE)
      .then(response => {
        // get data
        this.items = response.data;
        if (localStorage[this.key_sel]) { this.item_sel = parseInt(localStorage[this.key_sel]); }

        // watch fix bug
        this.$watch('item_sel', function(id) {
          localStorage[this.key_sel] = id;
        });

        return Promise.resolve(response)
      })
      .catch(error => { return Promise.reject(error) });
  },

  computed: {
    key_sel() { return router.currentRoute.name + '_editor_nav_obj_sel_' + this.localStorageKeyPostfix },
  },

  methods: {
    on_nal_new(id, name) { this.emit_fc(id, name, 'onNavNew') },
    on_nav_add(id, name) { this.emit_fc(id, name, 'onNavAdd') },
    emit_fc(id, name, emit_name) {
      getResponseAxios(this.$CONST.API.OBJ.GEOMETRY, { params: {rec_id: id,} })
        .then(response => {
          this.$emit(emit_name, id, name, fc_normalize(response.data));
          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) });
    },
  },

}
</script>

<style scoped lang="scss">
  div.tree::v-deep { overflow-y: auto !important; height: calc( 100% - 50px ); }
</style>
