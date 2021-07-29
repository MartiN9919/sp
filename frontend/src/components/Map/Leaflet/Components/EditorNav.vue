<template>
  <v-treeview
    active-class=""
    color=""
    :items="items"
    return-object
    hoverable
    transition
    dense
    open-on-click
    activatable
  >
    <template v-slot:prepend="{ item, open }">
      <v-icon :size="getIconSize()" :color="getColor(item)">{{ getIcon(item, open) }}</v-icon>
    </template>
  </v-treeview>
</template>



<script>

import { TREE } from '@/plugins/const';

export default {
  name:       'EditorNav',
  data: () => ({
    id_select: 8,
    items: [
      {
        id: 1,
        name: 'Applications :',
        children: [
          { id: 2, name: 'Calendar : app' },
          { id: 3, name: 'Chrome : app' },
          { id: 4, name: 'Webstorm : app' },
        ],
      },
      {
        id: 5,
        name: 'Documents :',
        children: [
          {
            id: 6,
            name: 'vuetify :',
            children: [
              {
                id: 7,
                name: 'src :',
                children: [
                  { id: 8, name: 'index : ts' },
                  { id: 9, name: 'bootstrap : ts' },
                ],
              },
            ],
          },
          {
            id: 10,
            name: 'material2 :',
            children: [
              {
                id: 11,
                name: 'src :',
                children: [
                  { id: 12, name: 'v-btn : ts' },
                  { id: 13, name: 'v-card : ts' },
                  { id: 14, name: 'v-window : ts' },
                ],
              },
            ],
          },
        ],
      },
      {
        id: 15,
        name: 'Downloads :',
        children: [
          { id: 16, name: 'October : pdf' },
          { id: 17, name: 'November : pdf' },
          { id: 18, name: 'Tutorial : html' },
        ],
      },
      {
        id: 19,
        name: 'Videos :',
        children: [
          {
            id: 20,
            name: 'Tutorials :',
            children: [
              { id: 21, name: 'Basic layouts : mp4' },
              { id: 22, name: 'Advanced techniques : mp4' },
              { id: 23, name: 'All about app : dir' },
            ],
          },
          { id: 24, name: 'Intro : mov' },
          { id: 25, name: 'Conference introduction : avi' },
        ],
      },
    ],
  }),

  methods: {
    getIcon(item, open) {
      if (!item.children) return 'mdi-vector-polygon'
      if (open)           return TREE.ICON_FOLDER_OPEN
      return TREE.ICON_FOLDER_CLOSE //'mdi-folder-outline'
    },

    getIconSize() { return TREE.ICON_SIZE; },

    getColor(item) {
      return (item.id == this.id_select) ? TREE.COLOR_SELECT : TREE.COLOR_DEFAULT;
    },
  },
}
</script>


