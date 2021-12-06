import { mapGetters, mapActions } from 'vuex';

export default {
  data: () => ({
    menu_set_add: {
      icon:     'mdi-eye',
      title:    'Оформление',
      subtitle: 'Отображаемые элементы карты',
      menu:     [
        {
          icon:     'mdi-calendar-range',
          title:    'Фильтр объектов по дате-времени',
          subtitle: '[Shift+Ф]',
          model:    'prop_range',
          color:    'blue',
        },
        {
          icon:     'mdi-google-circles-group',
          title:    'Группировка близлежащих маркеров',
          subtitle: '[Shift+Г]',
          model:    'prop_cluster',
        },
        {
          icon:     'mdi-message',
          title:    'Информация об объектах',
          subtitle: '[Shift+И]',
          model:    'prop_info',
        },
        // работоспособен, но не требует регулирования ввиду незначительного функционала
        // {
        //   icon:     'mdi-map-legend',
        //   title:    'Легенда',
        //   subtitle: '[Shift+Л]',
        //   model:    'prop_legend',
        // },
        // работоспособен, но не требует регулирования ввиду незначительного функционала
        // {
        //   icon:     'mdi-message-outline',
        //   title:    'Заметки',
        //   subtitle: '[Shift+З]',
        //   model:    'prop_notify',
        // },
        {
          icon:     'mdi-ruler',
          title:    'Масштаб',
          subtitle: '[Shift+М]',
          model:    'prop_scale',
        },
        {
          icon:     'mdi-arrow-expand-right',
          title:    'Рулетка',
          subtitle: '[Shift+Р]',
          model:    'prop_measure',
        },
        {
          icon:     'mdi-copyright',
          title:    'Логотип',
          subtitle: '[Shift+С]',
          model:    'prop_logo',
        },
      ],
    },
  }),

  beforeDestroy: function() {
    if (this.map) {
      this.map.removeEventListener('keydown', this.menu_set_key_down);
    };
  },

  computed: {
    ...mapGetters([
      'MAP_GET_RANGE',
      'MAP_GET_CLUSTER',
      'MAP_GET_HINT',
      'MAP_GET_LEGEND',
      'MAP_GET_NOTIFY',
      'MAP_GET_SCALE',
      'MAP_GET_MEASURE',
      'MAP_GET_LOGO',
    ]),
    prop_range: {
      set: function(val) { this.MAP_ACT_RANGE({on: !this.MAP_GET_RANGE}); },
      get: function()    { return this.MAP_GET_RANGE; },
    },
    prop_cluster: {
      set: function(val) { this.MAP_ACT_CLUSTER({on: !this.MAP_GET_CLUSTER}); },
      get: function()    { return this.MAP_GET_CLUSTER; },
    },
    prop_info: {
      set: function(val) { this.MAP_ACT_HINT({on: !this.MAP_GET_HINT}); },
      get: function()    { return this.MAP_GET_HINT; },
    },
    prop_legend: {
      set: function(val) { this.MAP_ACT_LEGEND({on: !this.MAP_GET_LEGEND}); },
      get: function()    { return this.MAP_GET_LEGEND; },
    },
    prop_notify: {
      set: function(val) { this.MAP_ACT_NOTIFY({on: !this.MAP_GET_NOTIFY}); },
      get: function()    { return this.MAP_GET_NOTIFY; },
    },
    prop_scale: {
      set: function(val) { this.MAP_ACT_SCALE({on: !this.MAP_GET_SCALE}); },
      get: function()    { return this.MAP_GET_SCALE; },
    },
    prop_measure: {
      set: function(val) { this.MAP_ACT_MEASURE({on: !this.MAP_GET_MEASURE}); },
      get: function()    { return this.MAP_GET_MEASURE; },
    },
    prop_logo: {
      set: function(val) { this.MAP_ACT_LOGO({on: !this.MAP_GET_LOGO}); },
      get: function()    { return this.MAP_GET_LOGO; },
    },
  },


  methods: {
    ...mapActions([
      'MAP_ACT_RANGE',
      'MAP_ACT_CLUSTER',
      'MAP_ACT_HINT',
      'MAP_ACT_LEGEND',
      'MAP_ACT_NOTIFY',
      'MAP_ACT_SCALE',
      'MAP_ACT_MEASURE',
      'MAP_ACT_LOGO',
    ]),

    // ВАЖНО
    // вызывать из родительского mounted или method.onMapReady
    // должна быть установлена переменная this.map
    mounted_menu_set() {
      this.map.addEventListener('keydown', this.menu_set_key_down);
    },

    // событие: нажатие клавиши
    menu_set_key_down(e) {
      if (e.originalEvent.shiftKey) {
        switch(e.originalEvent.code) {
          // Оформление
          case 'KeyA': { this.prop_range   = 1; return; } // Shift+Ф
          case 'KeyU': { this.prop_cluster = 1; return; } // Shift+Г
          case 'KeyB': { this.prop_info    = 1; return; } // Shift+И
        //case 'KeyK': { this.prop_legend  = 1; return; } // Shift+Л
        //case 'KeyP': { this.prop_notify  = 1; return; } // Shift+З
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

      // console.log(e.originalEvent.ctrlKey, e.originalEvent.code)
    },
  },


}
