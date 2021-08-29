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
import { str_cut, str_copy_deep, } from '@/components/Map/Leaflet/Lib/Lib';
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
    menu_item_name:           undefined,    // наименование item, на котором открыто меню
    menu_dialog_show:         false,        // отображение диалога
    menu_dialog_name:         undefined,    // редактируемое имя
    menu_dialog_name_old:     undefined,    // редактируемое имя: начальное значение
    menu_dialog_type:         undefined,    // тип операции

    menu_dialog_agree_show:   false,        // отображение диалога
    menu_dialog_agree_title:  '',           // текст согласия
    menu_dialog_agree_val:    false,        // подтверждение согласия

    menu_struct: undefined,
    menu_struct_base: [
      {
        icon:     'mdi-vector-polyline-plus',
        title:    'Создать ...',
        action:   'action_obj_new',
      },
      {
        icon:     'mdi-vector-polyline-edit',
        title:    'Сохранить',
        action:   'action_obj_save',
      },
      {
        icon:     'mdi-vector-polyline-edit',
        title:    'Переименовать ...',
        action:   'action_obj_rename',
      },
      { divider: true },
      {
        icon:     'mdi-vector-polyline-remove',
        title:    'Отключить ...',
        action:   'action_obj_del',
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
      'appendErrorAlert',
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

      this.menu_item_name = str_copy_deep(item?.name);
      let obj_name = str_cut(item?.name, 25, true);
      if              (is_fc)  this.menu_struct[MENU_IND_NEW   ].subtitle = "Создать объект";
      if ((is_obj) && (is_fc)) this.menu_struct[MENU_IND_SAVE  ].subtitle = "Сохранить объект как [ "+obj_name+" ]";
      if  (is_obj)             this.menu_struct[MENU_IND_RENAME].subtitle = "Переименовать объект [ "+obj_name+" ]";
      if  (is_obj)             this.menu_struct[MENU_IND_DEL   ].subtitle = "Отключить объект [ "    +obj_name+" ]";

      // показать корневой уровень меню
      this.$refs.menu_obj.show_root(e.clientX, e.clientY);
    },



    //
    // DIALOG: NAME
    //
    on_menu_dialog_show(item_type) {
      this.menu_dialog_type     = item_type;
      this.menu_dialog_name     = (item_type != MENU_IND_NEW)?str_copy_deep(this.menu_item_name):'';
      this.menu_dialog_name_old = str_copy_deep(this.menu_item_name);
      this.menu_dialog_show     = true;
      //this.$nextTick(function() { this.$refs.input_nam.onFocus(); });
    },
    is_disabled_menu_dialog_ok() {
      return (
        (!this.menu_dialog_name) ||
        (this.menu_dialog_name.trim()=='') ||
        (this.menu_dialog_name.trim()==this.menu_dialog_name_old)
      );
    },
    on_menu_dialog_ok() {
      if (this.is_disabled_menu_dialog_ok()) return;

      this.menu_dialog_show = false;
      this.menu_dialog_name = this.menu_dialog_name.trim();

      if (this.menu_dialog_type == MENU_IND_NEW)    this.action_obj_new_execute();
      if (this.menu_dialog_type == MENU_IND_RENAME) this.action_obj_rename_execute();
    },
    on_menu_msg(str) {
      this.appendErrorAlert({status: 501, content: str , show_time: 3, });
    },




    //
    // DIALOG: AGREE
    //
    on_menu_dialog_agree_show() {
      this.menu_dialog_agree_val   = false;
      this.menu_dialog_agree_title = "Я подтверждаю отключение объекта [ "+this.menu_item_name+" ]";
      this.menu_dialog_agree_show  = true;
      // this.$nextTick(function() { this.$refs.input_agree.onFocus(); });
    },
    on_menu_dialog_agree_ok() {
      if (!this.menu_dialog_agree_val) return;
      this.menu_dialog_agree_show = false;
      this.action_obj_del_execute();
    },



    // наличие права редактирования объектов
    is_right() {
      return true;
    },



    //
    // ACTION
    //

    // action: create
    action_obj_new(item) {
      this.on_menu_dialog_show(MENU_IND_NEW);
    },
    action_obj_save_execute() {
      this.on_menu_msg('Объект сохранен под именем [ '+this.menu_dialog_name+' ]');
    },


    // action: save
    action_obj_save(item) {
      this.on_menu_msg('Объект сохранен [ '+this.menu_dialog_name+' ]');
    },


    // action: rename
    action_obj_rename(item) {
      this.on_menu_dialog_show(MENU_IND_RENAME);
    },
    action_obj_rename_execute() {
      this.on_menu_msg('Объект пересохранен под именем [ '+this.menu_dialog_name+' ]');
    },


    // action: del
    action_obj_del(item) {
      this.on_menu_dialog_agree_show();
    },
    action_obj_del_execute() {
      this.on_menu_msg('Объект отключен [ '+this.menu_item_name+' ]');
    },



  },

}
