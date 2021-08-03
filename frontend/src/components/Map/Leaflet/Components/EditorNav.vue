<template>
  <div>
  <v-btn @click="tt">aaa</v-btn>
  <v-btn @click="tt5">bbb</v-btn>

  <PaneTree
   v-model.number="item_sel"
   :items="items"
  />
</div>
</template>

<script>
import { getResponseAxios } from '@/plugins/axios_settings';
import PaneTree from '@/components/Map/Leaflet/Components/PaneTree';

export default {
  name: 'EditorNav',
  components: { PaneTree, },

  created: function() {
    // fix bug
    this.$watch('item_sel', function(val) {
      console.log('Changed', val);
      localStorage[this.key_sel] = val;
    });

    // get data
    getResponseAxios(this.$CONST.API.OBJ.GEOMETRY_TREE)
      .then(response => {
        this.items = response.data;
        if (localStorage[this.key_sel]) { this.item_sel = parseInt(localStorage[this.key_sel]); }
        return Promise.resolve(response)
      })
      .catch(error => { return Promise.reject(error) });
  },

  methods: {
    tt() {
      this.item_sel = 36;
    },
    tt5() {
      console.log(this.item_sel);
    },
  },

  data: () => ({
    key_sel:  'sel_geometry',
    item_sel: 0,
    items:    [],
    // [
    //   {
    //     id: 1,
    //     name: 'Applications :',
    //     children: [
    //       { id: 2, name: 'Calendar : app' },
    //       { id: 3, name: 'Chrome : app' },
    //       { id: 4, name: 'Webstorm : app' },
    //     ],
    //   },
    //   {
    //     id: 5,
    //     name: 'Documents :',
    //     children: [
    //       {
    //         id: 6,
    //         name: 'vuetify :',
    //         children: [
    //           {
    //             id: 7,
    //             name: 'src :',
    //             children: [
    //               { id: 8, name: 'index : ts' },
    //               { id: 9, name: 'bootstrap : ts' },
    //             ],
    //           },
    //         ],
    //       },
    //       {
    //         id: 10,
    //         name: 'material2 :',
    //         children: [
    //           {
    //             id: 11,
    //             name: 'src :',
    //             children: [
    //               { id: 12, name: 'v-btn : ts' },
    //               { id: 13, name: 'v-card : ts' },
    //               { id: 14, name: 'v-window : ts' },
    //             ],
    //           },
    //         ],
    //       },
    //     ],
    //   },
    //   {
    //     id: 15,
    //     name: 'Downloads :',
    //     children: [
    //       { id: 16, name: 'October : pdf' },
    //       { id: 17, name: 'November : pdf' },
    //       { id: 18, name: 'Tutorial : html' },
    //     ],
    //   },
    //   {
    //     id: 99,
    //     name: 'zzzzz',
    //   },
    //   {
    //     id: 19,
    //     name: 'Videos :',
    //     children: [
    //       {
    //         id: 20,
    //         name: 'Tutorials :',
    //         children: [
    //           { id: 21, name: 'Basic layouts : mp4' },
    //           { id: 22, name: 'Advanced techniques : mp4' },
    //           { id: 23, name: 'All about app : dir' },
    //         ],
    //       },
    //       { id: 24, name: 'Intro : mov' },
    //       { id: 25, name: 'Conference introduction : avi' },
    //     ],
    //   },
    // ],
  }),

  watch: {

  },

}
</script>


