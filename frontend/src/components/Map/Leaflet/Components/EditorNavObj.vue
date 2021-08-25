<template>
  <Treeview
    :items="items"
    :itemSel.number.sync="item_sel"
    @onNew="on_new"
    @onAdd="on_add"
  />
</template>

<script>
/*
 * КОМПОНЕНТ: ДЕРЕВО ГЕОМЕТРИЙ
 *  <EditorNavObj
 *    localStoragePrefix="key_name"
 *    @onNew=""
 *    @onAdd=""
 *  />
 *
 *  update_fc(fc) { },
 *  @update_fc  - событие при изменении на карте fc
 */

import router from '@/router'
import { getResponseAxios } from '@/plugins/axios_settings';
import Treeview from '@/components/Map/Leaflet/Components/Treeview';
import { fc_normalize, } from '@/components/Map/Leaflet/Lib/Lib';

export default {
  name: 'editor-nav-obj',
  components: { Treeview, },

  props: {
    localStoragePrefix: { type: String, default() { return '' } },
  },
  emits: [
    'onNew',
    'onAdd',
  ],

  data: () => ({
    item_sel: 0,
    items:    [],
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
    key_sel() { return router.currentRoute.name + '_editor_nav_obj_sel_' + this.localStoragePrefix },
  },

  methods: {
    on_new(id, name) { this.emit_fc(id, name, 'onNew') },
    on_add(id, name) { this.emit_fc(id, name, 'onAdd') },
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
