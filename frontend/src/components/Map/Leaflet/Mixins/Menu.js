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
} from '@/components/Map/Leaflet/Mixins/Menu.test';

import contextMenuNested from '@/components/WebsiteShell/ContextMenu/contextMenuNested';
import MixMenuStruct     from '@/components/Map/Leaflet/Mixins/Menu.struct';

export default {
  mixins: [ MixMenuStruct, ],
  components: { contextMenuNested, },

  data: () => ({
    menu_items: undefined,
  }),

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
      set: function(val) { this.MAP_ACT_TILE({ind: val}); },
      get: function()    { return this.MAP_GET_TILE; },
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
    menu_show(e) {
      e.originalEvent.preventDefault();
      e.originalEvent.stopPropagation();

      // обновить menu_items
      let menu = this.menu_struct;                           // основа
      menu[0]['menu'][0]['radio'] = this.MAP_GET_TILES  ;    // добавить выбор тайлов
      this.menu_items = [...this.menu_items_key(), ...menu]; // добавить работу с фрагментами

      // показать корневой уровень меню
      this.$refs.menu.show_root(e.originalEvent.clientX, e.originalEvent.clientY);
    },


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
