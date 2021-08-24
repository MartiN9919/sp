<template>
  <Treeview
   :items="items"
   :itemSel.number.sync="item_sel"
   :showSel.sync="show_sel"
  />
</template>

<script>
/*
 * КОМПОНЕНТ: ДЕРЕВО ГЕОМЕТРИЙ
 *  <EditorNavObj
 *    localStoragePrefix="key_name"
 *    :triggerResetSelect="triggerResetSelect"
 *    @selectedFc="selected_fc"
 *  />
 *
 *  triggerResetSelect: true,
 *  update_fc(fc) { },
 *
 * triggerResetSelect - признак, изменение значения которого влечет сброс выделения выбранного item
 * @update_fc  - событие при изменении на карте fc
 */

import router from '@/router'
import { getResponseAxios } from '@/plugins/axios_settings';
import Treeview from '@/components/Map/Leaflet/Components/Treeview';

export default {
  name: 'editor-nav-obj',
  components: { Treeview, },

  props: {
    localStoragePrefix: { type: String, default() { return '' } },
    triggerResetSelect: { type: Boolean, default: () => undefined, },
  },
  emits: [
    'selectedFc',
  ],

  data: () => ({
    item_sel: 0,
    items:    [],
    show_sel: false,
  }),

  watch: {
    triggerResetSelect: function() { this.show_sel=false },  // изменение свойства влечет сброс выделения (через событие не нужно делать)
  },

  created: function() {
    getResponseAxios(this.$CONST.API.OBJ.GEOMETRY_TREE)
      .then(response => {
        // get data
        this.items = response.data;
        if (localStorage[this.key_sel]) { this.item_sel = parseInt(localStorage[this.key_sel]); }

        // watch fix bug
        this.$watch('item_sel', function(id) {
          localStorage[this.key_sel] = id;
          this.show_sel = true;             // выделить выбранный item
          this.selectedFc(id);
        });

        return Promise.resolve(response)
      })
      .catch(error => { return Promise.reject(error) });
  },

  computed: {
    key_sel() { return router.currentRoute.name + '_editor_nav_obj_sel_' + this.localStoragePrefix },
  },

  methods: {
    selectedFc(id) {
      getResponseAxios(this.$CONST.API.OBJ.GEOMETRY, { params: {rec_id: id,} })
        .then(response => {
          this.$emit('selectedFc', response.data);
          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) });
    },

  },

}
</script>

<style scoped>
  .v-treeview {
    overflow-y: auto !important;
    height: 100%;
  }
</style>