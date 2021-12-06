export default {
  data() {
    return {
      menu_struct_base: [
        // Menu.map
        // Menu.set

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