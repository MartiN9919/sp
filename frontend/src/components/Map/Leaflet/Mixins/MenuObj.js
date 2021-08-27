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
    menu_struct: undefined,
    menu_struct_base: [
      {
        icon:     'mdi-new-box',
        title:    'Создать',
        subtitle: 'Создать объект',
        action:   'on_obj_create',
      },
      {
        icon:     'mdi-content-save',
        title:    'Сохранить',
        subtitle: 'Сохранить объект',
        action:   'on_obj_save',
      },
      {
        icon:     'mdi-delete',
        title:    'Отключить',
        subtitle: 'Сделать объект неактуальным',
        action:   'on_obj_save',
      },
    ],
  }),

  computed: {
    ...mapGetters([
    ]),

    form: vm => vm,
  },


  methods: {
    ...mapActions([
      'MAP_ACT_ITEM_ADD',
      'MAP_ACT_ITEM_DEL',
      'MAP_ACT_ITEM_COLOR',
      'MAP_ACT_EDIT',
    ]),


    // Показать первый уровень меню, вызывается из родителя
    on_menu_show(e, item) {
      e.preventDefault();
      e.stopPropagation();

      // скорректировать базовое меню
      this.menu_struct = JSON.parse(JSON.stringify(this.menu_struct_base));
      let is_obj = ((item !== undefined) && (item?.children === undefined));
      this.menu_struct[1].disabled = !is_obj;
      this.menu_struct[2].disabled = !is_obj;

      // показать корневой уровень меню
      this.$refs.menu_obj.show_root(e.clientX, e.clientY);
    },

    on_obj_create(item){
      console.log(item)
    },

    on_obj_save(item){
      console.log(item)
    },

  },

}
