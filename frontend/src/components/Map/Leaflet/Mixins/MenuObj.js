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
import { str_cut, }      from '@/components/Map/Leaflet/Lib/Lib';
import { fc_exist, }     from '@/components/Map/Leaflet/Lib/LibFc';

const
  MENU_IND_NEW    = 0,
  MENU_IND_SAVE   = 1,
  MENU_IND_RENAME = 2,
  MENU_IND_DEL    = 4;

export default {
  mixins: [ MixMenuStruct, ],
  components: { contextMenuNested, },

  data: () => ({
    menu_struct: undefined,
    menu_struct_base: [
      {
        icon:     'mdi-vector-polyline-plus',
        title:    'Создать ...',
        action:   'on_obj_create',
      },
      {
        icon:     'mdi-vector-polyline-edit',
        title:    'Сохранить',
        action:   'on_obj_save',
      },
      {
        icon:     'mdi-vector-polyline-edit',
        title:    'Переименовать ...',
        action:   'on_obj_rename',
      },
      { divider: true },
      {
        icon:     'mdi-vector-polyline-remove',
        title:    'Отключить',
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

      // нет прав
      if (!this.is_right()) return;

      // скорректировать базовое меню
      this.menu_struct = JSON.parse(JSON.stringify(this.menu_struct_base));
      let is_obj = ((item !== undefined) && (item?.children === undefined));
      let is_fc  = fc_exist(this.fc);
      this.menu_struct[MENU_IND_NEW   ].disabled = !is_fc;
      this.menu_struct[MENU_IND_SAVE  ].disabled = !is_fc || !is_obj;
      this.menu_struct[MENU_IND_RENAME].disabled =           !is_obj;
      this.menu_struct[MENU_IND_DEL   ].disabled =           !is_obj;

      let obj_name = str_cut(item?.name, 25, true);
      if              (is_fc)  this.menu_struct[MENU_IND_NEW   ].subtitle = "Создать объект";
      if ((is_obj) && (is_fc)) this.menu_struct[MENU_IND_SAVE  ].subtitle = "Сохранить объект как [ "+obj_name+" ]";
      if  (is_obj)             this.menu_struct[MENU_IND_RENAME].subtitle = "Переименовать объект [ "+obj_name+" ]";
      if  (is_obj)             this.menu_struct[MENU_IND_DEL   ].subtitle = "Отключить объект [ "    +obj_name+" ]";

      // показать корневой уровень меню
      this.$refs.menu_obj.show_root(e.clientX, e.clientY);
    },

    on_obj_create(item){
      console.log(item, fc_exist(this.fc))
    },

    on_obj_save(item){
      console.log(item, fc_exist(this.fc))
    },

    is_right() {
      return true;
    },

  },

}
