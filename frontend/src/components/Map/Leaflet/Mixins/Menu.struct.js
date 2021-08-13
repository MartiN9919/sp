export default {
  data() {
    return {
      menu_struct: [
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
              title:    'Дата-время',
              subtitle: 'Фильтр отображаемых данных по дате-времени',
              model:    'prop_range',
              color:    'blue',
            },
            {
              icon:     'mdi-google-circles-group',
              title:    'Группировка маркеров',
              subtitle: 'Объединять близлежащие маркеры в группы',
              model:    'prop_cluster',
            },
            {
              icon:     'mdi-message',
              title:    'Подсказки',
              subtitle: 'Показывать всплывающие подсказки',
              model:    'prop_hint',
            },
            {
              icon:     'mdi-map-legend',
              title:    'Легенды',
              subtitle: 'Показывать всплывающие легенды',
              model:    'prop_legend',
            },
            {
              icon:     'mdi-ruler',
              title:    'Масштаб',
              subtitle: 'Показывать масштабную линейку',
              model:    'prop_scale',
            },
            {
              icon:     'mdi-arrow-expand-right', //'mdi-tape-measure',
              title:    'Рулетка',
              subtitle: 'Показывать рулетку',
              model:    'prop_measure',
            },
            {
              icon:     'mdi-copyright',
              title:    'Логотип',
              subtitle: 'Показывать логотип',
              model:    'prop_logo',
            },
          ],
        },


        { divider: true },
        {
          icon:     'mdi-wrench',
          title:    'ТЕСТЫ',
          subtitle: 'На этапе разработки',
          menu:     [
            {
              title: 'Отображение элементов карты',
              menu:  [
                {
                  icon:     'mdi-map-marker-plus',
                  title:    'Набор 1',
                  subtitle: 'Добавить набор фигур 1 (font+animation)',
                  action:   'test_item_add_1',
                },
                {
                  icon:     'mdi-map-marker-plus',
                  title:    'Набор 2',
                  subtitle: 'Добавить набор фигур 2 (pulse)',
                  action:   'test_item_add_2',
                },
                {
                  icon:     'mdi-map-marker-plus',
                  title:    'Набор 3',
                  subtitle: 'Добавить набор фигур 3 (color)',
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
                  subtitle: 'Удалить набор 1',
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