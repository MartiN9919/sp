<template>
  <v-card>
    <v-hover v-slot="{ hover }">
      <v-combobox
        ref="inp"
        v-model="search_value"
        style="margin: 15px;"
        :color="$CONST.APP.COLOR_OBJ"
        :items="search_items"
        :loading="search_wait"
        label="Искать"
        @input="on_search"
        dense
        outlined
        hide-details
        clearable
      >
      </v-combobox>
    </v-hover>

    <v-divider class="mx-4"></v-divider>

    <Treeview
      class="tree"
      :items="found_items"
      iconDef="mdi-web"
      :isIcon="true"
      :isFlat="true"
      @onNew="on_new"
      @onAdd="on_add"
    />
    <-- :itemSel.number.sync="found_item_sel" -->

  </v-card>
</template>

<script>

import router from '@/router';
import { getResponseAxios } from '@/plugins/axios_settings';
import Treeview from '@/components/Map/Leaflet/Components/Treeview';
import { fc_normalize, } from '@/components/Map/Leaflet/Lib/Lib';

export default {
  name: 'editor-nav-osm',
  components: { Treeview, },

  props: {
    localStorageKeyPostfix: { type: String, default() { return '' } },
  },
  emits: [
    'onNew',
    'onAdd',
  ],

  data: () => ({
    // found_item_sel:  0,
    search_value: undefined,
    search_items: [],
    search_wait:  false,
    found_items:  undefined,
  }),

  created: function() {
  //   // watch fix bug
  //   this.$watch('found_item_sel', function(id) {
  //     console.log(id)
  //   });
    this.search_items = JSON.parse(localStorage.getItem(this.key_sel, []))
  },

  beforeDestroy () {
    //this.timer_abort();
  },

  computed: {
    key_sel() { return router.currentRoute.name + '_editor_nav_osm_items_' + this.localStorageKeyPostfix },
  },

  methods: {
    // on_input() { this.timer_abort(); this.timer_input = setTimeout(this.on_search, 1000); },
    // timer_abort() { if (this.timer_input) { clearTimeout(this.timer_input); this.timer_input = undefined; } },

    on_search() {
      this.$refs.inp.isMenuActive = false;
      let name = this.search_value;
      if (name) { name = name.trim().toLowerCase() }

      getResponseAxios(this.$CONST.API.OBJ.OSM_SEARCH, { params: { text: name, } })
        .then(response => {
          this.found_items = response.data;

          // корректировать историю выбора
          if (
            (response.data.length > 0) &&
            (name) &&
            (name!='') &&
            (!this.search_items.find((item) => (item==name)))
          ) {
            this.search_items.unshift(name);
            this.search_items.splice(100);
            localStorage.setItem(this.key_sel, JSON.stringify(this.search_items).toLowerCase());
          }

          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) });
    },

    on_new(id, name) { this.emit_fc(id, name, 'onNew') },
    on_add(id, name) { this.emit_fc(id, name, 'onAdd') },
    emit_fc(id, name, emit_name) {
      this.search_wait = true;

      getResponseAxios(this.$CONST.API.OBJ.OSM_FC, { params: {id: id,} })
        .then(response => {
          this.$emit(emit_name, id, name, fc_normalize(response.data));
          this.search_wait = false;
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
