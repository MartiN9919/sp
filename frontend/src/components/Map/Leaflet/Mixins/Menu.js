import { mapGetters, mapActions } from 'vuex';

import {
  MAP_TEST_ITEM_1,
  MAP_TEST_ITEM_2,
  MAP_TEST_ITEM_3,
  MAP_TEST_EDIT_1,
  MAP_TEST_EDIT_2,
} from '@/components/Map/Leaflet/Mixins/Menu.test';

import contextMenuNested from '@/components/WebsiteShell/UIMainComponents/contextMenuNested';
import MixMenuStruct     from '@/components/Map/Leaflet/Mixins/Menu.struct';
import MixMenuMap        from '@/components/Map/Leaflet/Mixins/Menu.map';
import MixMenuSet        from '@/components/Map/Leaflet/Mixins/Menu.set';
import MixMenuPos        from '@/components/Map/Leaflet/Mixins/Menu.pos';

export default {
  mixins: [ MixMenuStruct, MixMenuMap, MixMenuSet, MixMenuPos, ],
  components: { contextMenuNested, },

  data: () => ({
    menu_struct: undefined,
  }),

  computed: {
    form: vm => vm,
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
    mounted_menu() {
      this.mounted_menu_set();
      this.mounted_menu_pos();
    },

    // Показать первый уровень меню, вызывается из родителя
    on_menu_show(e, mode) {
      e.originalEvent.preventDefault();
      e.originalEvent.stopPropagation();

      // обновить menu_struct
      this.menu_struct = JSON.parse(JSON.stringify(this.menu_struct_base)); // основа - глубокая копия
      this.menu_struct.splice(0, 0, this.menu_set_add());                   // добавить menu.set (оформление)
      this.menu_struct.splice(0, 0, this.menu_map_add());                   // добавить menu.map (подложка)
      this.menu_struct.splice(0, 0, this.menu_pos_add());                   // добавить menu.pos (фрагмент)

      if (mode=='editor') {
        this.menu_struct[2]['menu'].splice(0, 4);                           // удалить некоторые настройки оформления
        this.menu_struct.splice(4, 1);                                      // удалить тесты
        this.menu_struct.splice(3, 1);                                      // удалить сепаратор
      } else {
        //this.menu_struct[2]['menu'].splice(4, 1);                         // удалить некоторые настройки оформления
      }

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

    // тест action
    dd(item) {
      console.log(1, item)
    },
  },

}
