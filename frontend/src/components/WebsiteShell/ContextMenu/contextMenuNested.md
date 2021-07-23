# вложенные v-menu

### ПРИМЕР ВЫЗОВА
```html
  <template>
    <contextMenuNested
      :form="form"                    - указатель на vue-объект родителя
      :menuItems='menu_items'         - структура меню, см. ниже
      :color="'blue'"                 - цвет switch/radio по умолчанию
    />
  </template>
```
```js
data() => {
  menu_items: [
    {
      icon:     '...',
      title:    '...',
      subtitle: '...',
      menu: [
        {
          icon:     '...',
          title:    '...',
          subtitle: '...',
          model:    'prop_range',
          color:    'red',
          disabled: true,
        },
        ...
      ],
    },
    { divider: true },
    {
      icon:     '...',
      title:    '...',
      subtitle: '...',
      menu:     [
        {
          model: 'prop_tile',
          radio: [
            {
              title:    '...',
              subtitle: '...',
              color:    'red',
            },
            ...
          ],
        },
      ],
    },
  ],
},
computed: {
  form: vm => vm,
},

// активация в родителе
menu_show(x, y) { this.$refs.menu.show_root(x, y); },
```

### ВАЖНО
- item могуть быть:
  - с обработкой action (закрытие при выборе)
  - с обработкой model (switch)
  - c обработкой radio-group
- item.menu == [] - item disabled
***
[исходник](https://codepen.io/Moloth/pen/ZEBOzQP)
