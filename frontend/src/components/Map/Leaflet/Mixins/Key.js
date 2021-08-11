import { cook_set, cook_get_str } from '@/plugins/sys'

const KEY_POS_COOK    = 'KEY_POS_';
const KEY_SEPARATOR   = '_';
const KEY_POS_DEFAULT = '27.537231445312504_53.64138139745019_7';

export default {
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
                { title: 'Слот 1 (по умолчанию)', subtitle: 'Быстрый вызов: [Backspace]+[1]', slot: 1, action: this.key_action_save, },
                { divider: true },
                { title: 'Слот 2', subtitle: 'Быстрый вызов: [Backspace]+[2]', slot: 2, action: this.key_action_save, },
                { title: 'Слот 3', subtitle: 'Быстрый вызов: [Backspace]+[3]', slot: 3, action: this.key_action_save, },
                { title: 'Слот 4', subtitle: 'Быстрый вызов: [Backspace]+[4]', slot: 4, action: this.key_action_save, },
                { title: 'Слот 5', subtitle: 'Быстрый вызов: [Backspace]+[5]', slot: 5, action: this.key_action_save, },
                { title: 'Слот 6', subtitle: 'Быстрый вызов: [Backspace]+[6]', slot: 6, action: this.key_action_save, },
                { title: 'Слот 7', subtitle: 'Быстрый вызов: [Backspace]+[7]', slot: 7, action: this.key_action_save, },
                { title: 'Слот 8', subtitle: 'Быстрый вызов: [Backspace]+[8]', slot: 8, action: this.key_action_save, },
                { title: 'Слот 9', subtitle: 'Быстрый вызов: [Backspace]+[9]', slot: 9, action: this.key_action_save, },
                { title: 'Слот 0', subtitle: 'Быстрый вызов: [Backspace]+[0]', slot: 0, action: this.key_action_save, },
              ],
            },
            {
              icon:     'mdi-upload',
              title:    'Загрузить',
              //subtitle: 'Позиция и масштаб карты',
              menu:     [
                { title: 'Слот 1 (по умолчанию)', subtitle: 'Быстрый вызов: [~]+[1]', slot: 1, action: this.key_action_load, },
                { divider: true },
                { title: 'Слот 2', subtitle: 'Быстрый вызов: [~]+[2]', slot: 2, action: this.key_action_load, },
                { title: 'Слот 3', subtitle: 'Быстрый вызов: [~]+[3]', slot: 3, action: this.key_action_load, },
                { title: 'Слот 4', subtitle: 'Быстрый вызов: [~]+[4]', slot: 4, action: this.key_action_load, },
                { title: 'Слот 5', subtitle: 'Быстрый вызов: [~]+[5]', slot: 5, action: this.key_action_load, },
                { title: 'Слот 6', subtitle: 'Быстрый вызов: [~]+[6]', slot: 6, action: this.key_action_load, },
                { title: 'Слот 7', subtitle: 'Быстрый вызов: [~]+[7]', slot: 7, action: this.key_action_load, },
                { title: 'Слот 8', subtitle: 'Быстрый вызов: [~]+[8]', slot: 8, action: this.key_action_load, },
                { title: 'Слот 9', subtitle: 'Быстрый вызов: [~]+[9]', slot: 9, action: this.key_action_load, },
                { title: 'Слот 0', subtitle: 'Быстрый вызов: [~]+[0]', slot: 0, action: this.key_action_load, },
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

  methods: {
    // ВАЖНО
    // вызывать из родительского mounted или method.onMapReady
    // должна быть установлена переменная this.map
    key_mounted_after() {
      this.map.addEventListener('keydown', this.key_down);
      this.map.addEventListener('keyup',   this.key_up);
      this.key_pos_load(1);
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
      if (this.key_press.indexOf('Backspace') > -1) { this.key_pos_save(key_press_ind) }
      if (this.key_press.indexOf('Backquote') > -1) { this.key_pos_load(key_press_ind) }
    },

    // могут быть ситуации, когда keyup не вызывается
    key_up(e) { this.key_press.splice(this.key_press.indexOf(e.originalEvent.code), 1); },

    key_action_save(item) { this.key_pos_save(item.slot); },
    key_action_load(item) { this.key_pos_load(item.slot); },

    // cookies: сохранить позицию
    key_pos_save: function(ind) {
      let center = this.map.getCenter();
      let zoom   = this.map.getZoom();
      let s = center.lng.toString()+KEY_SEPARATOR+center.lat.toString()+KEY_SEPARATOR+zoom.toString();
      cook_set(KEY_POS_COOK+ind.toString(), s);
      this.appendErrorAlert({status: 501, content: 'Карта сохранена в слот '+ind, show_time: 3, });
    },

    // cookies: загрузить позицию
    key_pos_load: function(ind) {
      let s = cook_get_str(KEY_POS_COOK+ind.toString(), KEY_POS_DEFAULT).split(KEY_SEPARATOR);
      this.map.setView([parseFloat(s[1]), parseFloat(s[0])], parseFloat(s[2]));
    },
  },
};
