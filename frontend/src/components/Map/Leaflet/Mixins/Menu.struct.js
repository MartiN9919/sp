export default {
  beforeDestroy: function() {
    if (this.map) {
      this.map.removeEventListener('keydown', this.menu_struct_key_down);
    };
  },

  methods: {
    // ВАЖНО
    // вызывать из родительского mounted или method.onMapReady
    // должна быть установлена переменная this.map
    mounted_menu_struct() {
      this.map.addEventListener('keydown', this.menu_struct_key_down);
    },

    // событие: нажатие клавиши
    menu_struct_key_down(e) {
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

  data() {
    return {
      menu_struct_base: [
        {
          icon:     'mdi-map-outline',
          title:    'Подложка',
          subtitle: 'Фон карты',
          menu:     [
            {
              model: 'prop_tile',
              // radio: see mounted
            },
          ],
        },
        {
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


        { divider: true },
        {
          icon:     'mdi-wrench',
          title:    'ТЕСТЫ',
          subtitle: 'Для разработчиков',
          menu:     [
            {
              title: 'Отображение элементов карты',
              menu:  [
                {
                  icon:     'mdi-map-marker-plus',
                  title:    'Набор 1',
                  subtitle: 'Добавить набор фигур 1 (font+animation) Shift+[',
                  action:   'test_item_add_1',
                },
                {
                  icon:     'mdi-map-marker-plus',
                  title:    'Набор 2',
                  subtitle: 'Добавить набор фигур 2 (pulse) Shift+]',
                  action:   'test_item_add_2',
                },
                {
                  icon:     'mdi-map-marker-plus',
                  title:    'Набор 3',
                  subtitle: 'Добавить набор фигур 3 (color) Shift+"',
                  action:   'test_item_add_3',
                },
                {
                  icon:     'mdi-border-color',
                  title:    'Цвет 0',
                  subtitle: 'Изменить цвет набора 1',
                  action:   'test_item_color',
                  // ВАРИАНТ 2 - РАБОТАЕТ
                  // action: 'MAP_ACT_ITEM_COLOR',
                },
                {
                  icon:     'mdi-map-marker-remove',
                  title:    'Удалить',
                  subtitle: 'Удалить набор 1 Shift+\\',
                  action:   'test_item_del',
                },
                {
                  icon:     'mdi-briefcase-check',
                  title:    'Прочитать',
                  subtitle: '',
                  action:   'test_item_get',
                },
              ],
            },

            {
              title: 'Редактирование элементов карты',
              menu:  [
                {
                  icon:     'mdi-vector-polyline-edit',
                  title:    'Данные 1',
                  subtitle: 'Изменение элементов карты',
                  action:   'test_edit_1',
                },
                {
                  icon:     'mdi-vector-polyline-edit',
                  title:    'Данные 2',
                  subtitle: 'Изменение элементов карты',
                  action:   'test_edit_2',
                },
              ],
            },

            {
              title: 'MENU',
              menu:  [
                {
                  icon:     'mdi-google-circles-group',
                  title:    '1111',
                  subtitle: '22222',
                  action:   'dd',
                },
                { title: "Menu Item 1" },
                { divider: true },
                { title: "Menu Item 2", menu: [], },
                {
                  title: "Sub 1",
                  menu: [
                    { title: "1.1" },
                    { title: "1.2" },
                    {
                      title: "Sub-menu 2",
                      menu: [
                        { title: "2.1" },
                        { title: "2.2" },
                        {
                          title: "Sub-menu 3",
                          menu: [
                            { title: "3.1" },
                            { title: "3.2" },
                            {
                              title: "Sub-menu 4",
                              menu: [{ title: "4.1" }, { title: "4.2" }, { title: "4.3" }]
                            }
                          ]
                        }
                      ]
                    }
                  ],
                },

                { title: "Menu Item 3" },
                { divider: true },
                { title: "Menu Item 4" },
                { title: "Menu Item 5" },
              ],
            }

          ],
        },
      ],
    }
  }
}