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
              title: 'Отображение',
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
              title: 'Редактирование',
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
          ],
        },
      ],
    };
  },
}
