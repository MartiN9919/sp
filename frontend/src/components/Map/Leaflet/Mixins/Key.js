import { cook_set, cook_get_str } from '@/plugins/sys'
import KeyDialog from '@/components/Map/Leaflet/Components/KeyDialog';

const KEY_POS         = 'KEY_POS_';
const KEY_NAME        = 'KEY_NAME_';
const KEY_SEPARATOR   = '_';
const KEY_POS_DEFAULT = '27.537231445312504_53.64138139745019_7';

export default {
  components: {
    KeyDialog,
  },

  beforeDestroy: function() {
    if (this.map) {
      this.map.removeEventListener('keydown', this.key_down);
    };
  },

  methods: {
    // ВАЖНО
    // вызывать из родительского mounted или method.onMapReady
    // должна быть установлена переменная this.map
    key_mounted_after() {
      this.map.addEventListener('keydown', this.key_down);
      this.key_load_pos(1);
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
                { title: this.key_load_name(1), subtitle: 'Быстрый вызов: [1]', slot: 1, action: this.key_action_load, },
                { divider: true },
                { title: this.key_load_name(2), subtitle: 'Быстрый вызов: [2]', slot: 2, action: this.key_action_load, },
                { title: this.key_load_name(3), subtitle: 'Быстрый вызов: [3]', slot: 3, action: this.key_action_load, },
                { title: this.key_load_name(4), subtitle: 'Быстрый вызов: [4]', slot: 4, action: this.key_action_load, },
                { title: this.key_load_name(5), subtitle: 'Быстрый вызов: [5]', slot: 5, action: this.key_action_load, },
                { title: this.key_load_name(6), subtitle: 'Быстрый вызов: [6]', slot: 6, action: this.key_action_load, },
                { title: this.key_load_name(7), subtitle: 'Быстрый вызов: [7]', slot: 7, action: this.key_action_load, },
                { title: this.key_load_name(8), subtitle: 'Быстрый вызов: [8]', slot: 8, action: this.key_action_load, },
                { title: this.key_load_name(9), subtitle: 'Быстрый вызов: [9]', slot: 9, action: this.key_action_load, },
                { title: this.key_load_name(0), subtitle: 'Быстрый вызов: [0]', slot: 0, action: this.key_action_load, },
              ],
            },
            {
              icon:     'mdi-download',
              title:    'Сохранить',
              //subtitle: 'Позиция и масштаб карты',
              menu:     [
                { title: this.key_load_name(1), subtitle: 'Быстрый вызов: [Shift]+[1]', slot: 1, action: this.key_action_save, },
                { divider: true },
                { title: this.key_load_name(2), subtitle: 'Быстрый вызов: [Shift]+[2]', slot: 2, action: this.key_action_save, },
                { title: this.key_load_name(3), subtitle: 'Быстрый вызов: [Shift]+[3]', slot: 3, action: this.key_action_save, },
                { title: this.key_load_name(4), subtitle: 'Быстрый вызов: [Shift]+[4]', slot: 4, action: this.key_action_save, },
                { title: this.key_load_name(5), subtitle: 'Быстрый вызов: [Shift]+[5]', slot: 5, action: this.key_action_save, },
                { title: this.key_load_name(6), subtitle: 'Быстрый вызов: [Shift]+[6]', slot: 6, action: this.key_action_save, },
                { title: this.key_load_name(7), subtitle: 'Быстрый вызов: [Shift]+[7]', slot: 7, action: this.key_action_save, },
                { title: this.key_load_name(8), subtitle: 'Быстрый вызов: [Shift]+[8]', slot: 8, action: this.key_action_save, },
                { title: this.key_load_name(9), subtitle: 'Быстрый вызов: [Shift]+[9]', slot: 9, action: this.key_action_save, },
                { title: this.key_load_name(0), subtitle: 'Быстрый вызов: [Shift]+[0]', slot: 0, action: this.key_action_save, },
              ],
            },
          ],
        },
      ]
    },

    // событие: нажатие клавиши
    key_down(e) {
      let key_ind = -1;                                  // индекс функциональной клавиши 0, 1, ...
      for(let ind of [...Array(10).keys()]) {
        if (e.originalEvent.code == ('Digit'+ind)) {
          key_ind = ind;
          break;
        }
      }
      if (key_ind == -1) return;

      // позиция: сохранить / восстановить
      if (e.originalEvent.shiftKey) { this.key_save(key_ind) }
      else                          { this.key_load_pos(key_ind) }
    },



    key_action_save(item) { this.key_save(item.slot); },
    key_action_load(item) { this.key_load_pos(item.slot); },

    // cookies: сохранить
    key_save: function(ind) {
      this.$refs.key_dialog.exec(ind, this.key_load_name(ind));
    },
    key_save_ok: function(ind, val) {
      let center = this.map.getCenter();
      let zoom   = this.map.getZoom();
      let s = center.lng.toString()+KEY_SEPARATOR+center.lat.toString()+KEY_SEPARATOR+zoom.toString();
      cook_set(KEY_POS+ind.toString(), s);
      cook_set(KEY_NAME+ind.toString(), val);
      this.appendErrorAlert({status: 501, content: 'Фрагмент сохранен в слот '+ind+': ['+val+']' , show_time: 3, });
    },

    // cookies: загрузить
    key_load_pos: function(ind) {
      let s = cook_get_str(KEY_POS+ind.toString(), KEY_POS_DEFAULT).split(KEY_SEPARATOR);
      this.map.setView([parseFloat(s[1]), parseFloat(s[0])], parseFloat(s[2]));
    },
    key_load_name: function(ind) {
      return cook_get_str(KEY_NAME+ind.toString(), 'Слот '+ind);
    },
  },
};
