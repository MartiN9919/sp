<template>
  <v-card style="height: 100%;">
    <v-combobox
      ref="inp"
      v-model="search_value"
      style="padding: 15px;"
      :color="$CONST.APP.COLOR_OBJ"
      :items="search_items"
      :loading="search_wait"
      label="Искать"
      @input="on_search"
      dense
      outlined
      hide-details
      clearable
      autofocus
    />

    <v-divider class="mx-4"></v-divider>

    <Treeview
      class="tree"
      style="height: calc( 100% - 70px ); overflow-y: auto;"
      :items="found_items"
      :itemSel.number.sync="found_item_sel"
      iconDef="mdi-web"
      :isIcon="true"
      :isFlat="true"
      @onNavNew="on_nav_new"
      @onNavAdd="on_nav_add"
    />

  </v-card>
</template>

<script>

import router from '@/router';
import axios from '@/plugins/axiosSettings';
import Treeview from '@/components/Map/Leaflet/Components/Treeview';
import { fc_normalize, } from '@/components/Map/Leaflet/Lib/LibFc';

export default {
  name: 'editor-nav-osm',
  components: { Treeview, },

  props: {
    localStorageKeyPostfix: { type: String, default() { return '' } },
  },
  emits: [
    'onNavNew',
    'onNavAdd',
  ],

  data: () => ({
    search_value: undefined,
    search_items: [],
    search_wait:  false,
    search_timer: undefined,
    found_items:  undefined,
    found_item_sel: 0,
  }),

  created: function() {
  //   // watch fix bug
  //   this.$watch('found_item_sel', function(id) {
  //     console.log(id)
  //   });
    this.search_items = JSON.parse(localStorage.getItem(this.key_sel) || "[]")
  },

  // beforeDestroy () {
  //   this.timer_abort();
  // },

  // watch: {
  //   tab(val) { if (val == 'tab-osm') this.on_tab(); },
  // },

  computed: {
    key_sel() { return router.currentRoute.name + '_editor_nav_osm_items_' + this.localStorageKeyPostfix },
  },

  methods: {
    // on_tab()      { this.timer_abort(); this.timer_input = setTimeout(this.setFocus, 1000); },
    // timer_abort() { if (this.timer_input) { clearTimeout(this.timer_input); this.timer_input = undefined; } },
    // setFocus()    { this.$refs.inp.$el.focus(); },

    on_search() {
      this.$refs.inp.isMenuActive = false;
      let name = this.search_value;
      if (name) { name = name.trim().toLowerCase() }

      axios.get(this.$CONST.API.OBJ.OSM_SEARCH, { params: { text: name, } })
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
            this.search_items.splice(256);
            localStorage.setItem(this.key_sel, JSON.stringify(this.search_items).toLowerCase());
          }

          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) });
    },

    on_nav_new(id, name) { this.emit_fc(id, name, 'onNavNew') },
    on_nav_add(id, name) { this.emit_fc(id, name, 'onNavAdd') },
    emit_fc(id, name, emit_name) {
      this.search_wait = true;

      axios.get(this.$CONST.API.OBJ.OSM_FC, { params: {id: id,} })
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

</style>
