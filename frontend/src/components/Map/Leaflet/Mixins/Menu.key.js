import { mapGetters } from 'vuex';
import { cook_set, cook_get_str } from '@/plugins/sys'
import { MAP_CONST } from '@/components/Map/Leaflet/Lib/Const';
import DialogMenuPos from '@/components/Map/Leaflet/Components/DialogMenuPos';

export default {
  components: {
    DialogMenuPos,
  },

  beforeDestroy: function() {
    if (this.map) {
      this.map.removeEventListener('keydown', this.menu_key_down);
    };
  },

  computed: {
    ...mapGetters([
      'userInformation',
    ]),

    menu_pos_coord: function() { return 'MAP_POS_COORD_' +this.userInformation.id+'_' },
    menu_pos_name:  function() { return 'MAP_POS_NAME_'  +this.userInformation.id+'_' },
  },

  methods: {
    // ВАЖНО
    // вызывать из родительского mounted или method.onMapReady
    // должна быть установлена переменная this.map
    mounted_menu_key() {
      this.map.addEventListener('keydown', this.menu_key_down);
      this.menu_pos_coord_load(1);
    },


    // добавляется в контекстное меню
    menu_items_key() {
      return [
        {
          icon:     'mdi-border-none-variant',
          title:    'Фрагмент',
          subtitle: 'Позиция и масштаб карты',
          menu:     [
            {
              icon:     'mdi-upload',
              title:    'Загрузить',
              //subtitle: 'Позиция и масштаб карты',
              menu:     [
                { title: this.menu_pos_name_load(1), subtitle: '[1]', slot: 1, action: this.action_menu_pos_load, },
                { divider: true },
                { title: this.menu_pos_name_load(2), subtitle: '[2]', slot: 2, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(3), subtitle: '[3]', slot: 3, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(4), subtitle: '[4]', slot: 4, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(5), subtitle: '[5]', slot: 5, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(6), subtitle: '[6]', slot: 6, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(7), subtitle: '[7]', slot: 7, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(8), subtitle: '[8]', slot: 8, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(9), subtitle: '[9]', slot: 9, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(0), subtitle: '[0]', slot: 0, action: this.action_menu_pos_load, },
              ],
            },
            {
              icon:     'mdi-download',
              title:    'Сохранить',
              //subtitle: 'Позиция и масштаб карты',
              menu:     [
                { title: this.menu_pos_name_load(1), subtitle: '[Shift+1]', slot: 1, action: this.action_menu_pos_save, },
                { divider: true },
                { title: this.menu_pos_name_load(2), subtitle: '[Shift+2]', slot: 2, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(3), subtitle: '[Shift+3]', slot: 3, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(4), subtitle: '[Shift+4]', slot: 4, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(5), subtitle: '[Shift+5]', slot: 5, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(6), subtitle: '[Shift+6]', slot: 6, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(7), subtitle: '[Shift+7]', slot: 7, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(8), subtitle: '[Shift+8]', slot: 8, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(9), subtitle: '[Shift+9]', slot: 9, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(0), subtitle: '[Shift+0]', slot: 0, action: this.action_menu_pos_save, },
              ],
            },
          ],
        },
      ]
    },

    // событие: нажатие клавиши
    menu_key_down(e) {
      // позиция: сохранить / восстановить
      let key_ind = -1;                                  // индекс функциональной клавиши 0, 1, ...
      for(let ind of [...Array(10).keys()]) {
        if (e.originalEvent.code == ('Digit'+ind)) {
          key_ind = ind;
          break;
        }
      }
      if (key_ind != -1) {
        if (e.originalEvent.shiftKey) { this.menu_pos_save(key_ind) }
        else                          { this.menu_pos_coord_load(key_ind) }
        return
      }

      if (e.originalEvent.shiftKey) {
        switch(e.originalEvent.code) {
          // Оформление
          case 'KeyA': { this.prop_range   = 1; return; } // Shift+Ф
          case 'KeyU': { this.prop_cluster = 1; return; } // Shift+Г
          case 'KeyB': { this.prop_info    = 1; return; } // Shift+И
          case 'KeyK': { this.prop_legend  = 1; return; } // Shift+Л
          case 'KeyP': { this.prop_notify  = 1; return; } // Shift+З
          case 'KeyV': { this.prop_scale   = 1; return; } // Shift+М
          case 'KeyH': { this.prop_measure = 1; return; } // Shift+Р
          case 'KeyC': { this.prop_logo    = 1; return; } // Shift+С

          // Подложка

          // Тесты
          case 'BracketLeft':  { this.test_item_add_1(); return; }
          case 'BracketRight': { this.test_item_add_2(); return; }
          case 'Quote':        { this.test_item_add_3(); return; }
          case 'Backslash':    { this.test_item_del();   return; }
        }
      }

      console.log(e.originalEvent.ctrlKey, e.originalEvent.code)
    },



    action_menu_pos_save(item) { this.menu_pos_save(item.slot); },
    action_menu_pos_load(item) { this.menu_pos_coord_load(item.slot); },

    // cookies: сохранить
    menu_pos_save: function(ind) {
      this.$refs.key_dialog.exec(ind, this.menu_pos_name_load(ind));
    },
    menu_pos_save_ok: function(ind, val) {
      let center = this.map.getCenter();
      let zoom   = this.map.getZoom();
      let s = center.lng.toString()+MAP_CONST.POS.SEPARATOR+center.lat.toString()+MAP_CONST.POS.SEPARATOR+zoom.toString();
      cook_set(this.menu_pos_coord +ind.toString(), s);
      cook_set(this.menu_pos_name+ind.toString(), val);
      this.addNotification({content: 'Фрагмент сохранен в слот '+ind+': ['+val+']', timeout: 3});
    },

    // cookies: загрузить
    menu_pos_coord_load: function(ind) {
      let s = cook_get_str(this.menu_pos_coord+ind.toString(), MAP_CONST.POS.DEFAULT).split(MAP_CONST.POS.SEPARATOR);
      this.map.setView([parseFloat(s[1]), parseFloat(s[0])], parseFloat(s[2]));
    },
    menu_pos_name_load: function(ind) {
      return cook_get_str(this.menu_pos_name+ind.toString(), 'Слот '+ind);
    },
  },
};
