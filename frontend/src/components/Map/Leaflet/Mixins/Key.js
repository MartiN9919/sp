import { cook_set, cook_get_str } from '@/plugins/sys'

const KEY_POS_COOK    = 'KEY_POS_';
const KEY_SEPARATOR   = '_';
const KEY_POS_DEFAULT = '27.537231445312504_53.64138139745019_7';

export default {
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

    key_up(e) {
      // могут быть ситуации, когда keyup не вызывается
      this.key_press.splice(this.key_press.indexOf(e.originalEvent.code), 1);
    },

    // cookies: сохранить позицию
    key_pos_save: function(ind) {
      let center = this.map.getCenter();
      let zoom   = this.map.getZoom();
      let s = center.lng.toString()+KEY_SEPARATOR+center.lat.toString()+KEY_SEPARATOR+zoom.toString();
      cook_set(KEY_POS_COOK+ind.toString(), s);
      this.appendErrorAlert({status: 501, content: 'Карта сохранена под номером '+ind, show_time: 3, });
    },

    // cookies: загрузить позицию
    key_pos_load: function(ind) {
      let s = cook_get_str(KEY_POS_COOK+ind.toString(), KEY_POS_DEFAULT).split(KEY_SEPARATOR);
      this.map.setView([parseFloat(s[1]), parseFloat(s[0])], parseFloat(s[2]));
    },
  },
};
