<template>
  <v-menu
    v-model="options.visible"
    :position-x="options.x"
    :position-y="options.y"
    :close-on-content-click="false"
    class="select_off"
    min-width="500px"
    max-width="500px"
    absolute
    offset-y
    no-action
  >
    <v-list
      rounded
      oncontextmenu="return false"
    >
      <v-list-group
        v-for="(group_item, group_ind) in group_items"
        :key="'group_'+group_ind"
        no-action
      >

        <!-- АКТИВАТОР ПОДМЕНЮ -->
        <template v-slot:activator>
            <v-list-item-icon v-if="group_item.icon">
              <v-icon large v-text="group_item.icon"/>
            </v-list-item-icon>
            <v-list-item-content style="font-weight: bold;">
              <v-list-item-title v-text="group_item.title"/>
            </v-list-item-content>
        </template>


        <!-- ПОДМЕНЮ: ОБЩЕЕ -->
        <v-list-item
          v-if="!group_item.radio"
          v-for="(item, ind) in group_item.items"
          :key="group_item.key+'_'+ind"
          :disabled="item.disabled"
          class="select_off"
          style="padding-left: 15px;"
          @click.prevent="form[item.click](item.click_param)"
        >
          <!-- ИКОНКА -->
          <v-list-item-icon>
            <v-icon large v-text="item.icon"/>
          </v-list-item-icon>

          <!-- ТЕКСТ -->
          <v-list-item-content>
            <v-list-item-title v-text="item.title"/>
            <v-list-item-subtitle v-text="item.subtitle"/>
          </v-list-item-content>

          <!-- ACTION -->
          <v-list-item-action
            v-if="item.action"
          >
            <v-switch
              v-model="form[item.model]"
              color="green"
              @click.stop=""
            />
          </v-list-item-action>

        </v-list-item>


        <!-- ПОДМЕНЮ: RADIO -->
        <v-radio-group
          v-if="group_item.radio"
          v-for="(item, ind) in form[group_item.items]"
          v-model="form[group_item.model]"
          :key="group_item.key+'_'+ind"
          class="map-menu-radio-group select_off"
          hide-details
        >
          <v-list-item
            class="map-menu-tile-radio"
            @click.prevent="form[group_item.click](ind)"
          >
            <v-list-item-icon>
              <v-icon large v-text="item.icon"/>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="item.title"/>
              <v-list-item-subtitle v-text="item.subtitle"/>
            </v-list-item-content>
            <v-list-item-action>
              <v-radio
                color="green"
                :value="ind"
                :key="ind"
                @click.stop=""
              />
            </v-list-item-action>
          </v-list-item>
        </v-radio-group>


      </v-list-group>
    </v-list>
  </v-menu>
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
  MAP_TEST_EDIT_3,
  MAP_TEST_EDIT_4,
  MAP_TEST_EDIT_5,
} from '@/components/Map/Leaflet/Menu.test';

const props = {
  options: {
    type: Object,
    default() { return {}; },
  },
};

export default {
  name: 'Menu',
  props,
  data: () => ({
    group_items: [
      {
        title:        'КАРТА: ПОДЛОЖКА',
        key:          'tile',
        model:        'prop_tile',
        click:        'click_tile',
        radio:        true,
        items:        'MAP_GET_TILES',
      },
      {
        title:        'КАРТА: ЭЛЕМЕНТЫ',
        items: [
          {
            icon:        'mdi-calendar-range',
            title:       'Дата-время',
            subtitle:    'Фильтр отображаемых данных по дате-времени',
            model:       'prop_range',
            click:       'click_prop_invert',
            click_param: 'prop_range',
            action:      true,
          },
          {
            icon:        'mdi-google-circles-group',
            title:       'Группировка маркеров',
            subtitle:    'Объединять близлежащие маркеры в группы',
            model:       'prop_cluster',
            click:       'click_prop_invert',
            click_param: 'prop_cluster',
            action:      true,
          },
          {
            icon:        'mdi-message',
            title:       'Подсказки',
            subtitle:    'Показывать всплывающие подсказки',
            model:       'prop_hint',
            click:       'click_prop_invert',
            click_param: 'prop_hint',
            action:      true,
          },
          {
            icon:        'mdi-map-legend',
            title:       'Легенды',
            subtitle:    'Показывать всплывающие легенды',
            model:       'prop_legend',
            click:       'click_prop_invert',
            click_param: 'prop_legend',
            action:      true,
          },
          {
            icon:        'mdi-ruler',
            title:       'Масштаб',
            subtitle:    'Показывать масштабную линейку',
            model:       'prop_scale',
            click:       'click_prop_invert',
            click_param: 'prop_scale',
            action:      true,
          },
          {
            icon:        'mdi-arrow-expand-right', //'mdi-tape-measure',
            title:       'Рулетка',
            subtitle:    'Показывать рулетку',
            model:       'prop_measure',
            click:       'click_prop_invert',
            click_param: 'prop_measure',
            action:      true,
          },
          {
            icon:        'mdi-copyright',
            title:       'Логотип',
            subtitle:    'Показывать логотип',
            model:       'prop_logo',
            click:       'click_prop_invert',
            click_param: 'prop_logo',
            action:      true,
          },
        ],
      },
      {
        title: 'ТЕСТ ITEM',
        active: true,
        items: [
          {
            icon:        'mdi-map-marker-plus',
            title:       'Набор 1',
            subtitle:    'Добавить набор фигур 1 (font+animation)',
            click:       'test_item_add_1',
          },
          {
            icon:        'mdi-map-marker-plus',
            title:       'Набор 2',
            subtitle:    'Добавить набор фигур 2 (pulse)',
            click:       'test_item_add_2',
          },
          {
            icon:        'mdi-map-marker-plus',
            title:       'Набор 3',
            subtitle:    'Добавить набор фигур 3 (color)',
            click:       'test_item_add_3',
          },
          {
            icon:        'mdi-border-color',
            title:       'Цвет 0',
            subtitle:    'Изменить цвет набора 1',
            click:       'test_item_color',
            // ВАРИАНТ 2 - РАБОТАЕТ
            // click:       'MAP_ACT_ITEM_COLOR',
            // click_param: {ind: 0, color: "blue"},
          },
          {
            icon:        'mdi-map-marker-remove',
            title:       'Удалить',
            subtitle:    'Удалить набор 1',
            click:       'test_item_del',
          },
          {
            icon:        'mdi-briefcase-check',
            title:       'Прочитать',
            subtitle:    '',
            click:       'test_item_get',
          },
        ],
      },
      {
        title:        'ТЕСТ EDIT',
        items: [
          {
            icon:        'mdi-vector-polyline-edit',
            title:       'Данные 1',
            subtitle:    'Изменение элементов карты',
            click:       'test_edit_1',
          },
          {
            icon:        'mdi-vector-polyline-edit',
            title:       'Данные 2',
            subtitle:    'Изменение элементов карты',
            click:       'test_edit_2',
          },
          {
            icon:        'mdi-vector-polyline-edit',
            title:       'Данные 3',
            subtitle:    'Изменение элементов карты (пусто)',
            click:       'test_edit_3',
          },
          {
            icon:        'mdi-vector-polyline-edit',
            title:       'Данные 4',
            subtitle:    'Изменение элементов карты лайт 1 (пусто)',
            click:       'test_edit_4',
          },
          {
            icon:        'mdi-vector-polyline-edit',
            title:       'Данные 5',
            subtitle:    'Изменение элементов карты лайт 2 (пусто)',
            click:       'test_edit_5',
          },
        ],
      },
    ],


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
    // https://coderoad.ru/63553151/Vue-как-использовать-Getter-настройка-в-v-модели-с-v-for
    form: vm => vm,

    prop_range: {
      set: function(val) { this.MAP_ACT_RANGE_SHOW({on: val}); },
      get: function()    { return this.MAP_GET_RANGE_SHOW; },
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

      'MAP_ACT_EDIT_ON',
      'MAP_ACT_ITEM_DEL',
      'MAP_ACT_ITEM_COLOR',
    ]),
    click_tile (ind)          { this.prop_tile=ind; },
    click_prop_invert(val)    { this.form[val] = !this.form[val]; },

    test_item_add_1()         { this.MAP_ACT_ITEM_ADD(MAP_TEST_ITEM_1); },
    test_item_add_2()         { this.MAP_ACT_ITEM_ADD(MAP_TEST_ITEM_2); },
    test_item_add_3()         { this.MAP_ACT_ITEM_ADD(MAP_TEST_ITEM_3); },
    test_item_color()         { this.MAP_ACT_ITEM_COLOR({ind: 0, color: "blue"}); },
    test_item_del()           { this.$emit('legend_hide'); this.MAP_ACT_ITEM_DEL({id: 0}); },
    test_item_get()           { this.$emit('event_get', 'Получить результат'); },

    test_edit_1()             { this.MAP_ACT_EDIT_ON(MAP_TEST_EDIT_1); },
    test_edit_2()             { this.MAP_ACT_EDIT_ON(MAP_TEST_EDIT_2); },
    test_edit_3()             { this.MAP_ACT_EDIT_ON(MAP_TEST_EDIT_3); },
    test_edit_4()             { this.MAP_ACT_EDIT_ON(MAP_TEST_EDIT_4); },
    test_edit_5()             { this.MAP_ACT_EDIT_ON(MAP_TEST_EDIT_5); },
  },
}

</script>

<style scoped lang="scss">
  .map-menu-radio-group {
    margin: 0;
    padding: 0;
  }
</style>
