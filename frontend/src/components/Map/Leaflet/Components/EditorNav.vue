<template>
  <PaneTree
   v-model.number="item_sel"
   :items="items"
   :showSel="show_sel"
  />
</template>

<script>
/*
 * КОМПОНЕНТ: ДЕРЕВО ГЕОМЕТРИЙ 2
 *  <EditorNav
 *    :selReset="selReset"
 *    @selectedGeometry="selected_geometry"
 *  />
 *
 *  selReset: true,
 *  selected_geometry(fc) { },
 *
 * selReset           - признак, изменение значения которого влечет сброс выделения выбранного item
 * @selected_geometry - событие при выборе геометрии, возвращает fc
 */

import { getResponseAxios } from '@/plugins/axios_settings';
import PaneTree from '@/components/Map/Leaflet/Components/PaneTree';

export default {
  name: 'EditorNav',
  components: { PaneTree, },

  props: {
    selReset: { type: Boolean, default: () => undefined, },
  },

  data: () => ({
    key_sel:  'sel_geometry',
    item_sel: 0,
    items:    [],
    show_sel: false,
  }),

  watch: {
    selReset: function() { this.show_sel=false },  // изменение свойства влечет сброс выделения (через событие не нужно делать)
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
          this.selectedGeometry(id);
        });

        return Promise.resolve(response)
      })
      .catch(error => { return Promise.reject(error) });
  },

  methods: {
    selectedGeometry(id) {
      getResponseAxios(this.$CONST.API.OBJ.GEOMETRY, {params: {rec_id: id,}})
        .then(response => {
          this.$emit('selectedGeometry', response.data);
          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) });
    },

  },

}
</script>


