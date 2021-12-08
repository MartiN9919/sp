<template>
  <v-card style="height: 100%;">
    <v-combobox
      ref="inp"
      v-model="search_value"
      style="padding: 15px;"
      :color="$CONST.APP.COLOR_OBJ"
      :items="search_items_proxy"
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

    <EditorNavTree
      class="tree"
      style="height: calc( 100% - 70px ); overflow-y: auto;"
      :items="found_items"
      :itemSel.number.sync="found_sel"
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
import UserSetting from "@/store/addition"
import axios from '@/plugins/axiosSettings';
import EditorNavTree from '@/components/Map/Leaflet/Components/EditorNavTree';
import { fc_normalize, } from '@/components/Map/Leaflet/Lib/LibFc';

export default {
  name: 'editor-nav-osm',
  components: { EditorNavTree, },

  emits: [
    'onNavNew',
    'onNavAdd',
  ],

  data: () => ({
    search_value: undefined,
    search_items: new UserSetting('EditorNavOsm.search_items', []),
    search_wait:  false,
    found_items:  undefined,
    found_sel:    0,
  }),

  // created: function() {
  //   // watch fix bug
  //   this.$watch('found_sel', function(id) {
  //     console.log(id)
  //   });
  // },

  // watch: {
  //   tab(val) { if (val == 'tab-osm') this.on_tab(); },
  // },

  computed: {
    search_items_proxy: { // fix bug
      set: function(val) { this.search_items.value = val; },
      get: function()    { return this.search_items.value; },
    },
  },

  methods: {
    // setFocus()    { this.$refs.inp.$el.focus(); },

    on_search() {
      let self = this;
      this.$refs.inp.isMenuActive = false;
      let name = this.search_value;
      if (name) { name = name.trim().toLowerCase() }

      axios.get(this.$CONST.API.OBJ.OSM_SEARCH, { params: { text: name, } })
        .then(response => {
          self.found_items = response.data;

          // корректировать историю выбора
          if (
            (response.data.length > 0) &&
            (name) &&
            (name!='') &&
            (!self.search_items.value.find((item) => (item==name)))
          ) {
            let arr = self.search_items.value; // нельзя: self.search_items.value.unshift(name);
            arr.unshift(name);
            arr.splice(256);
            self.search_items.value = arr;
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
