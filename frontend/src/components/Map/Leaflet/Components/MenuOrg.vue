<template>
  <div>
  <contextMenuNested
    ref="menu"
    :form="form"
    :items='menu_items'
  />
  </div>
</template>

<script>
import {
  mapGetters,
  mapActions,
} from 'vuex';

import {
  MAP_TEST_ITEM_1,
  MAP_TEST_ITEM_2,
  MAP_TEST_ITEM_3,
  MAP_TEST_EDIT_1,
  MAP_TEST_EDIT_2,
} from '@/components/Map/Leaflet/Components/Menu.test';

import contextMenuNested from '@/components/WebsiteShell/ContextMenu/contextMenuNested';

export default {
  name: 'MenuOrg',

  components: {
    contextMenuNested,
  },

  data() {
    return {
      menu_items: [
        {
          icon:     ' ',
          title:    'Подложка',
          menu: [],
        },
        {
          icon:     'mdi-calendar-range',
          title:    'Элементы',
          menu: [
            {
              icon:     'mdi-calendar-range',
              title:    'Дата-время',
              subtitle: 'Фильтр отображаемых данных по дате-времени',
              model:    'prop_range',
              color:    'red',
            },
            {
              icon:     'mdi-google-circles-group',
              title:    'Группировка маркеров',
              subtitle: 'Объединять близлежащие маркеры в группы',
              model:    'prop_cluster',
            },
            {
              icon:     'mdi-message',
              title:    'Подсказки',
              subtitle: 'Показывать всплывающие подсказки',
              model:    'prop_hint',
            },
            {
              icon:     'mdi-map-legend',
              title:    'Легенды',
              subtitle: 'Показывать всплывающие легенды',
              model:    'prop_legend',
            },
            {
              icon:     'mdi-ruler',
              title:    'Масштаб',
              subtitle: 'Показывать масштабную линейку',
              model:    'prop_scale',
            },
            {
              icon:     'mdi-arrow-expand-right', //'mdi-tape-measure',
              title:    'Рулетка',
              subtitle: 'Показывать рулетку',
              model:    'prop_measure',
            },
            {
              icon:     'mdi-copyright',
              title:    'Логотип',
              subtitle: 'Показывать логотип',
              model:    'prop_logo',
            },
            // {
            //   icon:     'mdi-google-circles-group',
            //   title:    '1111',
            //   subtitle: '22222',
            //   action:   'dd',
            // },
          ],
        },




        {
          title: "Menu Item 1",
          // action: () => {
          //   console.log("menu-item-1");
          // }
        },
        { divider: true },
        { title: "Menu Item 2" },
        {
          title: "Sub 1",
          menu: [
            { title: "1.1" },
            { title: "1.2" },
            {
              title: "Sub-menu 2",
              menu: [
                { title: "2.1" },
                { title: "2.2" },
                {
                  title: "Sub-menu 3",
                  menu: [
                    { title: "3.1" },
                    { title: "3.2" },
                    {
                      title: "Sub-menu 4",
                      menu: [{ title: "4.1" }, { title: "4.2" }, { title: "4.3" }]
                    }
                  ]
                }
              ]
            }
          ],
        },

        { title: "Menu Item 3" },
        { divider: true },
        {
          title: "Menu Item 4",
          // action: () => {
          //   console.log("menu-item-4");
          // }
        },
        {
          title: "Menu Item 5",
          // action: () => {
          //   console.log("menu-item-5");
          // }
        }
      ],

    };
  },


  computed: {
    ...mapGetters([
      'MAP_GET_RANGE_SHOW',
      'MAP_GET_TILES',
      'MAP_GET_TILE',
      'MAP_GET_CLUSTER',
      'MAP_GET_HINT',
      'MAP_GET_LEGEND',
      'MAP_GET_SCALE',
      'MAP_GET_MEASURE',
      'MAP_GET_LOGO',
    ]),

    form: vm => vm,

    prop_range: {
      set: function(val) {
        console.log('set', val)
        this.MAP_ACT_RANGE_SHOW({on: val});
      },
      get: function()    {
        console.log('get', this.MAP_GET_RANGE_SHOW)
        return this.MAP_GET_RANGE_SHOW;
      },
    },
    prop_tile: {
      set: function(val) { this.MAP_ACT_TILE({ind: val}); },
      get: function()    { return this.MAP_GET_TILE; },
    },
    prop_cluster: {
      set: function(val) { this.MAP_ACT_CLUSTER({on: val}); },
      get: function()    { return this.MAP_GET_CLUSTER; },
    },
    prop_hint: {
      set: function(val) { this.MAP_ACT_HINT({on: val}); },
      get: function()    { return this.MAP_GET_HINT; },
    },
    prop_legend: {
      set: function(val) { this.MAP_ACT_LEGEND({on: val}); },
      get: function()    { return this.MAP_GET_LEGEND; },
    },
    prop_scale: {
      set: function(val) { this.MAP_ACT_SCALE({on: val}); },
      get: function()    { return this.MAP_GET_SCALE; },
    },
    prop_measure: {
      set: function(val) { this.MAP_ACT_MEASURE({on: val}); },
      get: function()    { return this.MAP_GET_MEASURE; },
    },
    prop_logo: {
      set: function(val) { this.MAP_ACT_LOGO({on: val}); },
      get: function()    { return this.MAP_GET_LOGO; },
    },

  },


  methods: {
    ...mapActions([
      'MAP_ACT_RANGE_SHOW',
      'MAP_ACT_TILE',
      'MAP_ACT_CLUSTER',
      'MAP_ACT_HINT',
      'MAP_ACT_LEGEND',
      'MAP_ACT_SCALE',
      'MAP_ACT_MEASURE',
      'MAP_ACT_LOGO',

      'MAP_ACT_ITEM_ADD',
      'MAP_ACT_ITEM_DEL',
      'MAP_ACT_ITEM_COLOR',
      'MAP_ACT_EDIT',
    ]),

    click_tile (ind)          {
      this.prop_tile=ind;
    },

    menu_show(x, y) {
      this.$refs.menu.show_root(x, y);
    },

    dd(item) {
      console.log(item)
    }
  },

}

</script>
