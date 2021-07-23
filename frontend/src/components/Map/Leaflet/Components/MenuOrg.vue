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

  mounted() {
    // this.menu_items[0]['menu'] = this.MAP_GET_TILES;
  },

  data() {
    return {
      menu_items: [
        {
          icon:     'mdi-map-outline',
          title:    'Подложка',
          subtitle: 'Фон карты',
          menu:     [
            {
              model: 'prop_tile',
              radio: [
                {
                  title:    'OSM',
                  subtitle: 'Схема (Интернет)',
                  url:      'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                  attr:     '',
                  tms:      false,
                  //crs:      L.CRS.EPSG3857,
                },
                {
                  title:    'OSM',
                  subtitle: 'Схема (Локальная сеть)',
                  url:      'http://200.200.200.231/osm/{z}/{x}/{y}.png',
                  attr:     '',
                  tms:      false,
                },
                // {
                //   title:    'OSM',
                //   subtitle: 'Схема (Локальная сеть)',
                //   url:      'http://192.168.56.1:8080/osm/{z}/{x}/{y}.png',
                //   attr:     '',
                //   tms:      false,
                //   enabled:  false,
                // },
                {
                  title:    'Yandex',
                  subtitle: 'Интернет',
                  url:      'https://core-sat.maps.yandex.net/tiles?l=sat&v=3.786.0&x={x}&y={y}&z={z}&scale=2&lang=ru_UA',
                  attr:     '',
                  tms:      false,
                  crs:      L.CRS.EPSG3395,
                  enabled:  false,
                },
                {
                  title:    'ESRI',
                  subtitle: 'Спутник (Интернет)',
                  url:      'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                  attr:     '',
                  tms:      false,
                },
                {
                  title:    'ОТМ',
                  subtitle: 'Схема (Интернет)',
                  url:      'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
                  attr:     '',
                  tms:      false,
                },
                {
                  title:    'Stamen',
                  subtitle: 'Черно-белая (Интернет)',
                  url:      'http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png',
                  attr:     '',
                  tms:      false,
                },
                {
                  title:    'Yandex',
                  subtitle: 'Спутник (Локальная сеть)',
                  url:      'http://200.200.200.232/{z}/{x}/{y}.jpg',
                  attr:     '',
                  tms:      false,
                  crs:      L.CRS.EPSG3395, //+L.CRS.EPSG3857,  -L.CRS.EPSG4326
                  enabled:  false,
                },
              ],
            },
          ],
        },
        {
          icon:     'mdi-eye',
          title:    'Оформление',
          subtitle: 'Отображаемые элементы карты',
          menu:  [
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
          ],
        },


        { divider: true },
        {
          icon:     'mdi-wrench',
          title:    'ТЕСТЫ',
          subtitle: 'На этапе разработки',
          menu:  [
            {
              title: 'Отображение элементов карты',
              menu:  [
                {
                  icon:     'mdi-map-marker-plus',
                  title:    'Набор 1',
                  subtitle: 'Добавить набор фигур 1 (font+animation)',
                  action:   'test_item_add_1',
                },
                {
                  icon:     'mdi-map-marker-plus',
                  title:    'Набор 2',
                  subtitle: 'Добавить набор фигур 2 (pulse)',
                  action:   'test_item_add_2',
                },
                {
                  icon:     'mdi-map-marker-plus',
                  title:    'Набор 3',
                  subtitle: 'Добавить набор фигур 3 (color)',
                  action:   'test_item_add_3',
                },
                {
                  icon:     'mdi-border-color',
                  title:    'Цвет 0',
                  subtitle: 'Изменить цвет набора 1',
                  action:   'test_item_color',
                  // ВАРИАНТ 2 - РАБОТАЕТ
                  // action: 'MAP_ACT_ITEM_COLOR',
                },
                {
                  icon:     'mdi-map-marker-remove',
                  title:    'Удалить',
                  subtitle: 'Удалить набор 1',
                  action:   'test_item_del',
                },
                {
                  icon:     'mdi-briefcase-check',
                  title:    'Прочитать',
                  subtitle: '',
                  action:   'test_item_get',
                },
              ],
            },

            {
              title: 'Редактирование элементов карты',
              menu:  [
                {
                  icon:     'mdi-vector-polyline-edit',
                  title:    'Данные 1',
                  subtitle: 'Изменение элементов карты',
                  action:   'test_edit_1',
                },
                {
                  icon:     'mdi-vector-polyline-edit',
                  title:    'Данные 2',
                  subtitle: 'Изменение элементов карты',
                  action:   'test_edit_2',
                },
              ],
            },

            {
              title: 'MENU',
              menu:  [
                {
                  icon:     'mdi-google-circles-group',
                  title:    '1111',
                  subtitle: '22222',
                  action:   'dd',
                },
                { title: "Menu Item 1" },
                { divider: true },
                { title: "Menu Item 2", menu: [], },
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
                { title: "Menu Item 4" },
                { title: "Menu Item 5" },
              ],
            }

          ],
        },
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

    prop_tile: {
      set: function(val) {
        console.log('set', val)
        this.MAP_ACT_TILE({ind: val});
      },
      get: function()    {
        console.log('get', this.MAP_GET_TILE)
        return this.MAP_GET_TILE;
      },
    },
    prop_range: {
      set: function(val) { this.MAP_ACT_RANGE_SHOW({on: val}); },
      get: function()    { return this.MAP_GET_RANGE_SHOW; },
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

    // Показать первый уровень меню, вызывается из родителя
    menu_show(x, y)   { this.$refs.menu.show_root(x, y); },

    test_item_add_1() { this.MAP_ACT_ITEM_ADD(MAP_TEST_ITEM_1); },
    test_item_add_2() { this.MAP_ACT_ITEM_ADD(MAP_TEST_ITEM_2); },
    test_item_add_3() { this.MAP_ACT_ITEM_ADD(MAP_TEST_ITEM_3); },
    test_item_color() { this.MAP_ACT_ITEM_COLOR({ind: 0, color: "blue"}); },
    test_item_del()   { this.$emit('legend_hide'); this.MAP_ACT_ITEM_DEL({id: 0}); },
    test_item_get()   { this.$emit('event_get', 'Получить результат'); },

    test_edit_1()     { this.MAP_ACT_EDIT(MAP_TEST_EDIT_1); },
    test_edit_2()     { this.MAP_ACT_EDIT(MAP_TEST_EDIT_2); },

    dd(item) {
      console.log(1, item)
    },
  },

}

</script>
