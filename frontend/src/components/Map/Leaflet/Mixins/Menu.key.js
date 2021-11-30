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
      console.log(1)
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
                { title: this.menu_pos_name_load(1), subtitle: 'Быстрый вызов: [1]', slot: 1, action: this.action_menu_pos_load, },
                { divider: true },
                { title: this.menu_pos_name_load(2), subtitle: 'Быстрый вызов: [2]', slot: 2, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(3), subtitle: 'Быстрый вызов: [3]', slot: 3, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(4), subtitle: 'Быстрый вызов: [4]', slot: 4, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(5), subtitle: 'Быстрый вызов: [5]', slot: 5, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(6), subtitle: 'Быстрый вызов: [6]', slot: 6, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(7), subtitle: 'Быстрый вызов: [7]', slot: 7, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(8), subtitle: 'Быстрый вызов: [8]', slot: 8, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(9), subtitle: 'Быстрый вызов: [9]', slot: 9, action: this.action_menu_pos_load, },
                { title: this.menu_pos_name_load(0), subtitle: 'Быстрый вызов: [0]', slot: 0, action: this.action_menu_pos_load, },
              ],
            },
            {
              icon:     'mdi-download',
              title:    'Сохранить',
              //subtitle: 'Позиция и масштаб карты',
              menu:     [
                { title: this.menu_pos_name_load(1), subtitle: 'Быстрый вызов: [Shift]+[1]', slot: 1, action: this.action_menu_pos_save, },
                { divider: true },
                { title: this.menu_pos_name_load(2), subtitle: 'Быстрый вызов: [Shift]+[2]', slot: 2, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(3), subtitle: 'Быстрый вызов: [Shift]+[3]', slot: 3, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(4), subtitle: 'Быстрый вызов: [Shift]+[4]', slot: 4, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(5), subtitle: 'Быстрый вызов: [Shift]+[5]', slot: 5, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(6), subtitle: 'Быстрый вызов: [Shift]+[6]', slot: 6, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(7), subtitle: 'Быстрый вызов: [Shift]+[7]', slot: 7, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(8), subtitle: 'Быстрый вызов: [Shift]+[8]', slot: 8, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(9), subtitle: 'Быстрый вызов: [Shift]+[9]', slot: 9, action: this.action_menu_pos_save, },
                { title: this.menu_pos_name_load(0), subtitle: 'Быстрый вызов: [Shift]+[0]', slot: 0, action: this.action_menu_pos_save, },
              ],
            },
          ],
        },
      ]
    },

    // событие: нажатие клавиши
    menu_key_down(e) {
      let key_ind = -1;                                  // индекс функциональной клавиши 0, 1, ...
      for(let ind of [...Array(10).keys()]) {
        if (e.originalEvent.code == ('Digit'+ind)) {
          key_ind = ind;
          break;
        }
      }
      if (key_ind == -1) return;

      // позиция: сохранить / восстановить
      if (e.originalEvent.shiftKey) { this.menu_pos_save(key_ind) }
      else                          { this.menu_pos_coord_load(key_ind) }
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
