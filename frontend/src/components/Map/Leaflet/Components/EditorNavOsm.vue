<template>
  <v-card>
    <v-hover v-slot="{ hover }">
      <v-text-field
        v-model="value"
        style="margin: 15px;"
        :color="$CONST.APP.COLOR_OBJ"
        @input="on_input"
        dense
        outlined
        hide-details
        clearable
        autocomplete="off"
      >
      </v-text-field>
    </v-hover>

    <v-divider class="mx-4"></v-divider>

    <Treeview
      class="tree"
      :items="items"
      :itemSel.number.sync="item_sel"
      iconDef="mdi-web"
      :isIcon="true"
      :isFlat="true"
      @onNew="on_new"
      @onAdd="on_add"
    />
  </v-card>
</template>

<script>

/*
      :itemSel.number.sync="item_sel"
 */
import { getResponseAxios } from '@/plugins/axios_settings';
import Treeview from '@/components/Map/Leaflet/Components/Treeview';
import { fc_normalize, } from '@/components/Map/Leaflet/Lib/Lib';

export default {
  name: 'editor-nav-osm',
  components: { Treeview, },

  emits: [
    'onNew',
    'onAdd',
  ],

  data: () => ({
    item_sel:    0,
    value:       undefined,
    items:       undefined,
    timer_input: undefined,
  }),

  // created: function() {
  //   // watch fix bug
  //   this.$watch('item_sel', function(id) {
  //     console.log(id)
  //   });
  // },

  beforeDestroy () {
    this.timer_abort();
  },

  methods: {
    on_input() { this.timer_abort(); this.timer_input = setTimeout(this.search, 1000); },
    timer_abort() { if (this.timer_input) { clearTimeout(this.timer_input); this.timer_input = undefined; } },

    search() {
      getResponseAxios(this.$CONST.API.OBJ.OSM_SEARCH, { params: { text: this.value,} })
        .then(response => {
          this.items = response.data;
          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) });
    },

    on_new(id, name) { this.emit_fc(id, name, 'onNew') },
    on_add(id, name) { this.emit_fc(id, name, 'onAdd') },
    emit_fc(id, name, emit_name) {
      getResponseAxios(this.$CONST.API.OBJ.OSM_FC, { params: {id: id,} })
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
  div.tree::v-deep { overflow-y: auto !important; height: calc( 100% - 120px ); }
</style>
