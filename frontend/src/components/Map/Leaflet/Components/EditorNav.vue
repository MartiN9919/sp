<template>
  <PaneTree
   v-model.number="item_sel"
   :items="items"
  />
</template>

<script>
import { getResponseAxios } from '@/plugins/axios_settings';
import PaneTree from '@/components/Map/Leaflet/Components/PaneTree';

export default {
  name: 'EditorNav',
  components: { PaneTree, },

  created: function() {
    getResponseAxios(this.$CONST.API.OBJ.GEOMETRY_TREE)
      .then(response => {
        // get data
        this.items = response.data;
        if (localStorage[this.key_sel]) { this.item_sel = parseInt(localStorage[this.key_sel]); }

        // fix bug
        this.$watch('item_sel', function(id) {
          localStorage[this.key_sel] = id;
          this.load_geometry(id);
        });

        return Promise.resolve(response)
      })
      .catch(error => { return Promise.reject(error) });
  },

  methods: {
    load_geometry(id) {
      getResponseAxios(this.$CONST.API.OBJ.GEOMETRY, {params: {rec_id: id,}})
        .then(response => {
          this.$emit('loadGeometry', response.data);
          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) });
    },
  },

  data: () => ({
    key_sel:  'sel_geometry',
    item_sel: 0,
    items:    [],
  }),

}
</script>


