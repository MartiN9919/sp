<template>
  <PaneTree
   :items="items"
   :itemSel.number.sync="item_sel"
   :showSel.sync="show_sel"
  />
</template>

<script>
/*
 * КОМПОНЕНТ: ДЕРЕВО ГЕОМЕТРИЙ
 *  <EditorNavObj
 *    :resetSelect="resetSelect"
 *    @updateFc="selected_fc"
 *  />
 *
 *  resetSelect: true,
 *  update_fc(fc) { },
 *
 * resetSelect - признак, изменение значения которого влечет сброс выделения выбранного item
 * @update_fc  - событие при изменении на карте fc
 */

import { getResponseAxios } from '@/plugins/axios_settings';
import PaneTree from '@/components/Map/Leaflet/Components/PaneTree';

export default {
  name: 'editor-nav-obj',
  components: { PaneTree, },

  props: {
    resetSelect: { type: Boolean, default: () => undefined, },
  },
  emits: [
    'updateFc',
  ],

  data: () => ({
    key_sel:  'sel_geometry',
    item_sel: 0,
    items:    [],
    show_sel: false,
  }),

  watch: {
    resetSelect: function() { this.show_sel=false },  // изменение свойства влечет сброс выделения (через событие не нужно делать)
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
          this.updateFc(id);
        });

        return Promise.resolve(response)
      })
      .catch(error => { return Promise.reject(error) });
  },

  methods: {
    updateFc(id) {
      getResponseAxios(this.$CONST.API.OBJ.GEOMETRY, {params: {rec_id: id,}})
        .then(response => {
          this.$emit('updateFc', response.data);
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