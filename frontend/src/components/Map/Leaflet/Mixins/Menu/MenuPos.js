import UserSetting from '@/store/addition';
import { MAP_CONST } from '@/components/Map/Leaflet/Lib/Const';
import DialogMenuPos from '@/components/Map/Leaflet/Components/DialogMenuPos';

export default {
  components: {
    DialogMenuPos,
  },

  beforeDestroy: function() {
    if (this.map) {
      this.map.removeEventListener('keydown', this.menu_pos_key_down);
    };
  },

  data: () => ({ menu_pos_state: [], }),

  methods: {
    // инициализация, вызывается из родителя
    mounted_menu_pos() {
      // инициализация пользовательских настроек
      for(let ind=0; ind<10; ind++) {
        this.menu_pos_state.push(
          new UserSetting('MAP_POS_'+ind.toString(), {
            'title': 'Не задано',
            'x':      MAP_CONST.POS.X,
            'y':      MAP_CONST.POS.Y,
            'zoom':   MAP_CONST.POS.ZOOM,
          })
        );
      }
      this.map.addEventListener('keydown', this.menu_pos_key_down);
      this.menu_pos_load(1);
    },


    // добавить в контекстное меню
    menu_pos_add() {
      const POS_LOAD = 2;
      const POS_SAVE = 3;
      let val = {
        icon:     'mdi-border-none-variant',
        title:    'Фрагмент',
        subtitle: 'Позиция и масштаб карты',
        menu:     [
          {
            icon:     'mdi-map-marker-multiple', // mdi-select-multiple-marker
            title:    'Показать все объекты',
            subtitle: '[Shit+П]',
            action:   this.action_menu_pos_show_all,
            disabled: (this.SCRIPT_GET.length == 0),
          },
          { divider: true },
          {
            icon:  'mdi-upload',
            title: 'Загрузить',
            menu:  [],
          },
          {
            icon:  'mdi-download',
            title: 'Сохранить',
            menu:  [],
          },
        ],
      };

      for(let ind=0; ind<10; ind++) {
        val.menu[POS_LOAD].menu.push({
          title:    this.menu_pos_state[ind].value.title,
          subtitle: '['+ind+']',
          slot:     ind,
          action:   this.action_menu_pos_load,
        });
        val.menu[POS_SAVE].menu.push({
          title:    this.menu_pos_state[ind].value.title,
          subtitle: '[Shift+'+ind+']',
          slot:     ind,
          action:   this.action_menu_pos_save,
        });
        if (ind==1) {
          val.menu[POS_LOAD].menu.push({ divider: true });
          val.menu[POS_SAVE].menu.push({ divider: true });
        }
      }
      val.menu[POS_LOAD].menu.push(val.menu[POS_LOAD].menu.shift());
      val.menu[POS_SAVE].menu.push(val.menu[POS_SAVE].menu.shift());
      return val;
    },

    // событие: нажатие клавиши
    menu_pos_key_down(e) {
      // Показать все [Shift+П]
      if ((e.originalEvent.shiftKey) && (e.originalEvent.code == 'KeyG')) {
        this.action_menu_pos_show_all();
        return;
      }

      // позиция: сохранить / загрузить
      let key_ind = -1;                                  // индекс функциональной клавиши 0, 1, ...
      for(let ind of [...Array(10).keys()]) {
        if (e.originalEvent.code == ('Digit'+ind)) {
          key_ind = ind;
          break;
        }
      }
      if (key_ind != -1) {
        if (e.originalEvent.shiftKey) { this.menu_pos_save(key_ind) }
        else                          { this.menu_pos_load(key_ind) }
      }
    },


    // показать все
    action_menu_pos_show_all() {
      let fg = new L.FeatureGroup();
      this.SCRIPT_GET.forEach(function(item){
        fg.addLayer(L.geoJSON(item.fc));
      });
      if (Object.keys(fg._layers).length > 0) {
        this.map.fitBounds(fg.getBounds(), { padding: [20, 20] });
      }
    },

    // сохранить
    action_menu_pos_save(item)   { this.menu_pos_save(item.slot); },
    menu_pos_save: function(ind) { this.$refs.key_dialog.exec(ind, this.menu_pos_state[ind].value.title); },
    menu_pos_save_ok: function(ind, title) {
      let val    = this.menu_pos_state[ind].value;
      let center = this.map.getCenter();
      val.x      =  center.lng;
      val.y      =  center.lat;
      val.zoom   = this.map.getZoom();
      val.title  = title;
      this.menu_pos_state[ind].value = val;
      this.addNotification({content: 'Фрагмент сохранен в слот '+ind+': ['+title+']', timeout: 3});
    },

    // загрузить
    action_menu_pos_load(item) { this.menu_pos_load(item.slot); },
    menu_pos_load: function(ind) {
      let val = this.menu_pos_state[ind].value;
      this.map.setView([val.y, val.x], val.zoom);
    },
  },
};
