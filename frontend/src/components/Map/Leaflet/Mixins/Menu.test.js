import { mapGetters, mapActions } from 'vuex';
import {
  MAP_TEST_ITEM_1,
  MAP_TEST_ITEM_2,
  MAP_TEST_ITEM_3,
  MAP_TEST_EDIT_1,
  MAP_TEST_EDIT_2,
} from '@/components/Map/Leaflet/Mixins/Menu.test.data';

const menu = {
  icon:     'mdi-wrench',
  title:    'ТЕСТЫ',
  subtitle: 'Для разработчиков',
  menu:     [
    {
      title: 'Отображение',
      menu:  [
        {
          icon:     'mdi-map-marker-plus',
          title:    'Набор 1',
          subtitle: 'Добавить набор фигур 1 (font+animation) Shift+[',
          action:   'test_item_add_1',
        },
        {
          icon:     'mdi-map-marker-plus',
          title:    'Набор 2',
          subtitle: 'Добавить набор фигур 2 (pulse) Shift+]',
          action:   'test_item_add_2',
        },
        {
          icon:     'mdi-map-marker-plus',
          title:    'Набор 3',
          subtitle: 'Добавить набор фигур 3 (color) Shift+"',
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
          subtitle: 'Удалить набор 1 Shift+\\',
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
      title: 'Редактирование',
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
  ],
};

export default {
  beforeDestroy: function() {
    if (this.map) {
      this.map.removeEventListener('keydown', this.menu_test_key_down);
    };
  },

  data() {
    return {
      menu_struct_base: [],
    };
  },

  methods: {
    ...mapActions([
      'MAP_ACT_ITEM_ADD',
      'MAP_ACT_ITEM_DEL',
      'MAP_ACT_ITEM_COLOR',
      'MAP_ACT_EDIT',
    ]),

    // ВАЖНО
    // вызывать из родительского mounted или method.onMapReady
    // должна быть установлена переменная this.map
    mounted_menu_test() {
      this.map.addEventListener('keydown', this.menu_test_key_down);
    },

    // добавить в контекстное меню
    menu_test_add() {
      return JSON.parse(JSON.stringify(menu));
    },

    // событие: нажатие клавиши
    menu_test_key_down(e) {
      if (e.originalEvent.shiftKey) {
        switch(e.originalEvent.code) {
          case 'BracketLeft':  { this.test_item_add_1(); return; }
          case 'BracketRight': { this.test_item_add_2(); return; }
          case 'Quote':        { this.test_item_add_3(); return; }
          case 'Backslash':    { this.test_item_del();   return; }
        }
      }
      // console.log(e.originalEvent.ctrlKey, e.originalEvent.code)
    },

    test_item_add_1() { this.MAP_ACT_ITEM_ADD(MAP_TEST_ITEM_1); },
    test_item_add_2() { this.MAP_ACT_ITEM_ADD(MAP_TEST_ITEM_2); },
    test_item_add_3() { this.MAP_ACT_ITEM_ADD(MAP_TEST_ITEM_3); },
    test_item_color() { this.MAP_ACT_ITEM_COLOR({ind: 0, color: "blue"}); },
    test_item_del()   { this.$emit('legend_hide'); this.MAP_ACT_ITEM_DEL({id: 0}); },
    test_item_get()   { this.$emit('event_get', 'Получить результат'); },

    test_edit_1()     { this.MAP_ACT_EDIT(MAP_TEST_EDIT_1); },
    test_edit_2()     { this.MAP_ACT_EDIT(MAP_TEST_EDIT_2); },

    // тест action
    dd(item) {
      console.log(1, item)
    },
  },
}
