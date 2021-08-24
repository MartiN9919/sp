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
      :items="items"
      :itemSel.number.sync="item_sel"
      :isIcon="false"
      :isFlat="true"
    />
  </v-card>
</template>

<script>

/*
      :itemSel.number.sync="item_sel"
      :showSel.sync="show_sel"
 */
import { getResponseAxios } from '@/plugins/axios_settings';
import Treeview from '@/components/Map/Leaflet/Components/Treeview';
import { fc_normalize, } from '@/components/Map/Leaflet/Lib/Lib';

export default {
  name: 'editor-nav-osm',
  components: { Treeview, },

  props: {
    showSel: { type: Boolean, default: () => true, },
  },
  //emits: ['selectedGeometry', 'update:showSel'],
  data: () => ({
    item_sel:    0,
    value:       undefined,
    items:       undefined,
    timer_input: undefined,
  }),


  created: function() {
    // watch fix bug
    this.$watch('item_sel', function(id) {
      console.log(id)
      //this.show_sel = true;             // выделить выбранный item
      this.selectedFc(id);
    });
  },

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

    selectedFc(id) {
      getResponseAxios(this.$CONST.API.OBJ.OSM_FC, { params: {id: id,} })
        .then(response => {
          console.log(response.data);
          let dd = fc_normalize(response.data);

          this.$emit('selectedFc', dd);
          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) });
    },


  },
}

/*
        <template v-slot:append="">
          <div v-show="hover" style="margin-top: -6 !important;">
            <v-btn icon @click="dd" :color="$CONST.APP.COLOR_OBJ">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </div>
        </template>

    <v-list-item-group>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Single-line item</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item two-line>
        <v-list-item-content>
          <v-list-item-title>Two-line item</v-list-item-title>
          <v-list-item-subtitle>Secondary text</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-list-item three-line>
        <v-list-item-content>
          <v-list-item-title>Three-line item</v-list-item-title>
          <v-list-item-subtitle>
            Secondary line text Lorem ipsum dolor sit amet,
          </v-list-item-subtitle>
          <v-list-item-subtitle>
            consectetur adipiscing elit.
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

    </v-list-item-group>

 */

</script>
