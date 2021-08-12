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

  data() {
    return {
      // добавляется в контекстное меню
      menu_items_key: [
        {
          icon:     'mdi-border-none-variant',
          title:    'Фрагмент',
          subtitle: 'Позиция и масштаб карты',
          menu:     [
            {
              icon:     'mdi-download',
              title:    'Сохранить',
              //subtitle: 'Позиция и масштаб карты',
              menu:     [
                { title: this.key_load_name(1), subtitle: '[Backspace]+[1]', slot: 1, action: this.key_action_save, },
                { divider: true },
                { title: this.key_load_name(2), subtitle: '[Backspace]+[2]', slot: 2, action: this.key_action_save, },
                { title: this.key_load_name(3), subtitle: '[Backspace]+[3]', slot: 3, action: this.key_action_save, },
                { title: this.key_load_name(4), subtitle: '[Backspace]+[4]', slot: 4, action: this.key_action_save, },
                { title: this.key_load_name(5), subtitle: '[Backspace]+[5]', slot: 5, action: this.key_action_save, },
                { title: this.key_load_name(6), subtitle: '[Backspace]+[6]', slot: 6, action: this.key_action_save, },
                { title: this.key_load_name(7), subtitle: '[Backspace]+[7]', slot: 7, action: this.key_action_save, },
                { title: this.key_load_name(8), subtitle: '[Backspace]+[8]', slot: 8, action: this.key_action_save, },
                { title: this.key_load_name(9), subtitle: '[Backspace]+[9]', slot: 9, action: this.key_action_save, },
                { title: this.key_load_name(0), subtitle: '[Backspace]+[0]', slot: 0, action: this.key_action_save, },
              ],
            },
            {
              icon:     'mdi-upload',
              title:    'Загрузить',
              //subtitle: 'Позиция и масштаб карты',
              menu:     [
                { title: this.key_load_name(1), subtitle: '[~]+[1]', slot: 1, action: this.key_action_load, },
                { divider: true },
                { title: this.key_load_name(2), subtitle: '[~]+[2]', slot: 2, action: this.key_action_load, },
                { title: this.key_load_name(3), subtitle: '[~]+[3]', slot: 3, action: this.key_action_load, },
                { title: this.key_load_name(4), subtitle: '[~]+[4]', slot: 4, action: this.key_action_load, },
                { title: this.key_load_name(5), subtitle: '[~]+[5]', slot: 5, action: this.key_action_load, },
                { title: this.key_load_name(6), subtitle: '[~]+[6]', slot: 6, action: this.key_action_load, },
                { title: this.key_load_name(7), subtitle: '[~]+[7]', slot: 7, action: this.key_action_load, },
                { title: this.key_load_name(8), subtitle: '[~]+[8]', slot: 8, action: this.key_action_load, },
                { title: this.key_load_name(9), subtitle: '[~]+[9]', slot: 9, action: this.key_action_load, },
                { title: this.key_load_name(0), subtitle: '[~]+[0]', slot: 0, action: this.key_action_load, },
              ],
            },
          ],
        },
      ],
    }
  },

  created: function() {
      this.key_press = [];

      // document.addEventListener('keyup', function (evt) {
      //     if (evt.keyCode === 27) { }
      // });
  },

  beforeDestroy: function() {
    if (this.map) {
      this.map.removeEventListener('keydown', this.key_down);
      this.map.removeEventListener('keyup',   this.key_up);
    };
  },

  computed: {
  },

  methods: {
    // ВАЖНО
    // вызывать из родительского mounted или method.onMapReady
    // должна быть установлена переменная this.map
    key_mounted_after() {
      this.map.addEventListener('keydown', this.key_down);
      this.map.addEventListener('keyup',   this.key_up);
      this.key_load_pos(1);
    },

    // событие: нажатие клавиши
    key_down(e) {
      // запонить нажатую клавишу
      if (this.key_press.indexOf(e.originalEvent.code)<0){
        this.key_press.push(e.originalEvent.code);
      }

      // key_press_ind - индекс функциональной клавиши 0, 1, ...
      let key_press_ind = -1;
      for(let key_press_item of this.key_press) {
        for(let ind of [...Array(10).keys()]) {
          if (key_press_item == ('Digit'+ind)) {
            key_press_ind = ind;
            break;
          }
        }
        if (key_press_ind > -1) break;
      }
      if (key_press_ind == -1) return;

      // позиция: сохранить / восстановить
      if (this.key_press.indexOf('Backspace') > -1) { this.key_save(key_press_ind) }
      if (this.key_press.indexOf('Backquote') > -1) { this.key_load_pos(key_press_ind) }
    },

    // могут быть ситуации, когда keyup не вызывается
    key_up(e) { this.key_press.splice(this.key_press.indexOf(e.originalEvent.code), 1); },

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
      //this.menu_items_set();
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
