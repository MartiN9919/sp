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

import contextMenuNested from '@/components/WebsiteShell/UIMainComponents/contextMenuNested';
import MixMenuStruct from '@/components/Map/Leaflet/Mixins/Menu.struct';
import { str_cut, str_copy_deep, } from '@/components/Map/Leaflet/Lib/Lib';
import { fc_exist, } from '@/components/Map/Leaflet/Lib/LibFc';
import axios from '@/plugins/axiosSettings';


const
  MENU_IND_NEW    = 0,
  MENU_IND_SAVE   = 1,
  MENU_IND_CHANGE = 2,
  MENU_IND_DEL    = 4;

export default {
  mixins: [ MixMenuStruct, ],
  components: { contextMenuNested, },

  data: () => ({
    menu_item:                  undefined,  // копия item, на котором открыто меню

    menu_dialog_param_show:     false,      // отображение диалога
    menu_dialog_param_name:     undefined,  // редактируемое имя
    menu_dialog_param_name_old: undefined,  // редактируемое имя: начальное значение
    menu_dialog_param_icon:     undefined,  // редактируемая иконка
    menu_dialog_param_icon_old: undefined,  // редактируемая иконка: начальное значение
    menu_dialog_param_type:     undefined,  // тип операции: MENU_IND_NEW, ...
    menu_dialog_param_title:    '',         // заголовок окна
    menu_dialog_param_icons:    undefined,  // список икнок

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
        title:    'Изменить ...',
        action:   'action_obj_change',
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
      'userInformation',
    ]),

    form: vm => vm,
  },

  methods: {
    ...mapActions([
      //'MAP_ACT_ITEM_ADD',
      //'MAP_ACT_ITEM_DEL',
      //'MAP_ACT_ITEM_COLOR',
      //'MAP_ACT_EDIT',
      'addNotification',
    ]),


    // Показать первый уровень меню, вызывается из родителя
    on_menu_show(e, menu_item) {
      e.preventDefault();
      e.stopPropagation();

      // нет прав
      if (!this.is_right()) return;

      // скорректировать базовое меню
      this.menu_struct = JSON.parse(JSON.stringify(this.menu_struct_base));
      let is_obj = ((menu_item !== undefined) && (menu_item?.children === undefined));
      let is_fc  = fc_exist(this.fc);
      this.menu_struct[MENU_IND_NEW   ].disabled = !is_fc;
      this.menu_struct[MENU_IND_SAVE  ].disabled = !is_fc || !is_obj;
      this.menu_struct[MENU_IND_CHANGE].disabled =           !is_obj;
      this.menu_struct[MENU_IND_DEL   ].disabled =           !is_obj;

      this.menu_item = (menu_item !== undefined) ? JSON.parse(JSON.stringify(menu_item)) : undefined;
      let obj_name = str_cut(menu_item?.name, 25, true);
      if              (is_fc)  this.menu_struct[MENU_IND_NEW   ].subtitle = "Создать объект";
      if ((is_obj) && (is_fc)) this.menu_struct[MENU_IND_SAVE  ].subtitle = "Сохранить объект [ "+obj_name+" ]";
      if  (is_obj)             this.menu_struct[MENU_IND_CHANGE].subtitle = "Изменить объект [ " +obj_name+" ]";
      if  (is_obj)             this.menu_struct[MENU_IND_DEL   ].subtitle = "Отключить объект [ "+obj_name+" ]";

      // показать корневой уровень меню
      this.$refs.menu_obj.show_root(e.clientX, e.clientY);
    },



    //
    // DIALOG: PARAM
    //
    on_menu_dialog_param_show(item_type) {
      this.menu_dialog_param_type     = item_type;
      this.menu_dialog_param_name     = (this.menu_item)?str_copy_deep(this.menu_item.name):'';
      this.menu_dialog_param_name_old = (this.menu_item)?str_copy_deep(this.menu_item.name):'';
      this.menu_dialog_param_icon     = (this.menu_item)?str_copy_deep(this.menu_item.icon):'';
      this.menu_dialog_param_icon_old = (this.menu_item)?str_copy_deep(this.menu_item.icon):'';
      this.menu_dialog_param_title    = (item_type==MENU_IND_NEW   )?'Создать объект':
                                        (item_type==MENU_IND_CHANGE)?'Изменить объект':
                                        '';
      this.menu_dialog_param_icons_set(this.items);
      this.menu_dialog_param_show     = true;
      //this.$nextTick(function() { this.$refs.input_name.onFocus(); });
    },
    is_disabled_menu_dialog_param_ok() {
      return (
        (!this.menu_dialog_param_name) ||
        (this.menu_dialog_param_name.trim()=='') ||
        (
          (this.menu_dialog_param_name.trim()==this.menu_dialog_param_name_old) &&
          (this.menu_dialog_param_icon?.trim()==this.menu_dialog_param_icon_old)
        )
      );
    },
    on_menu_dialog_param_ok() {
      if (this.is_disabled_menu_dialog_param_ok()) return;

      this.menu_dialog_param_show = false;
      this.menu_dialog_param_name = this.menu_dialog_param_name.trim();

      if (this.menu_dialog_param_type == MENU_IND_NEW)    this.action_obj_new_execute();
      if (this.menu_dialog_param_type == MENU_IND_CHANGE) this.action_obj_change_execute();
    },

    // найти все уникальные иконки узлов
    menu_dialog_param_icons_set() {
      this.menu_dialog_param_icons = new Set();
      this.menu_dialog_param_icons_step(this.items);
      this.menu_dialog_param_icons = Array.from(this.menu_dialog_param_icons);
    },
    menu_dialog_param_icons_step(items) {
      for (const item of items) {
        if (item.icon)     { this.menu_dialog_param_icons.add(item.icon); }
        if (item.children) { this.menu_dialog_param_icons_step(item.children); }
      }
    },




    //
    // DIALOG: AGREE
    //
    on_menu_dialog_agree_show() {
      this.menu_dialog_agree_val   = false;
      this.menu_dialog_agree_title = "Я подтверждаю отключение объекта [ "+this.menu_item.name+" ]";
      this.menu_dialog_agree_show  = true;
      // this.$nextTick(function() { this.$refs.input_agree.onFocus(); });
    },
    on_menu_dialog_agree_ok() {
      if (!this.menu_dialog_agree_val) return;
      this.menu_dialog_agree_show = false;
      this.action_obj_del_execute();
    },



    // всплывающее сообщение
    on_menu_msg(str) {
      this.addNotification({content: str, timeout: 3});
    },

    // наличие права редактирования объектов
    is_right() {
      return (this.userInformation.admin || this.userInformation.write);
    },




    //
    // ACTION
    //

    // action: create
    action_obj_new(menu_item) {
      this.on_menu_dialog_param_show(MENU_IND_NEW);
    },
    async action_obj_new_execute() {
      await axios.post(this.$CONST.API.OBJ.GEOMETRY, {
        parent_id: (this.menu_item?.parent_id) ? this.menu_item?.parent_id : 0,
        name:      this.menu_dialog_param_name,
        //icon:      (this.menu_dialog_param_icon!='')?this.menu_dialog_param_icon:undefined,
        location:  this.fc,
      })
        .then (r => { return Promise.resolve(r) })  // r.data?.object
        .catch(e => { return Promise.reject(e) });
      this.refresh_items();
      this.on_menu_msg('Объект сохранен под именем [ '+this.menu_dialog_param_name+' ]');
    },


    // action: save
    async action_obj_save(menu_item) {
      await axios.post(this.$CONST.API.OBJ.GEOMETRY, {
        rec_id:    this.menu_item.id,
        location:  this.fc,
      })
        .then (r => { return Promise.resolve(r) })
        .catch(e => { return Promise.reject(e) });
      this.refresh_items();
      this.on_menu_msg('Объект сохранен [ '+this.menu_item.name+' ]');
    },


    // action: change
    action_obj_change(menu_item) {
      this.on_menu_dialog_param_show(MENU_IND_CHANGE);
    },
    async action_obj_change_execute() {
      await axios.post(this.$CONST.API.OBJ.GEOMETRY, {
        rec_id:    this.menu_item.id,
        name:      this.menu_dialog_param_name,
        //icon:      (this.menu_dialog_param_icon!='')?this.menu_dialog_param_icon:undefined,
      })
        .then (r => { return Promise.resolve(r) })
        .catch(e => { return Promise.reject(e) });
      this.refresh_items();
      this.on_menu_msg('Объект изменен [ '+this.menu_dialog_param_name+' ]');
    },


    // action: del
    action_obj_del(menu_item) {
      this.on_menu_dialog_agree_show();
    },
    action_obj_del_execute() {
      this.refresh_items();
      this.on_menu_msg('Объект отключен [ '+this.menu_item.name+' ]');
    },



  },

}
