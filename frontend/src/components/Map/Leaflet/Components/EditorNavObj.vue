<template>
  <Treeview
   v-on="$listeners"
   :items="items"
   :itemSel.number.sync="item_sel"
  />
</template>

<script>
/*
 * КОМПОНЕНТ: ДЕРЕВО ГЕОМЕТРИЙ
 *  <EditorNavObj
 *    localStoragePrefix="key_name"
 *    @selectedFc="selected_fc"
 *  />
 *
 *  update_fc(fc) { },
 *  @update_fc  - событие при изменении на карте fc
 */

import router from '@/router'
import { getResponseAxios } from '@/plugins/axios_settings';
import Treeview from '@/components/Map/Leaflet/Components/Treeview';

export default {
  name: 'editor-nav-obj',
  components: { Treeview, },

  props: {
    localStoragePrefix: { type: String, default() { return '' } },
  },
  emits: [
    'selectedFc',
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
          this.selected_fc(id);
        });

        return Promise.resolve(response)
      })
      .catch(error => { return Promise.reject(error) });
  },

  computed: {
    key_sel() { return router.currentRoute.name + '_editor_nav_obj_sel_' + this.localStoragePrefix },
  },

  methods: {
    selected_fc(id) {
      getResponseAxios(this.$CONST.API.OBJ.GEOMETRY, { params: {rec_id: id,} })
        .then(response => {
          this.$emit('selectedFc', response.data, this.get_name(id, this.items));
          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) });
    },

    get_name(id, items) {
      let ret = undefined;
      for(let ind=0; ind<items.length; ind++) {
        if (items[ind].id == id) { ret = items[ind].name; }
        if (items[ind].children) { ret = this.get_name(id, items[ind].children); }
        if (ret) break;
      }
      return ret;
    },

  },

}
</script>
