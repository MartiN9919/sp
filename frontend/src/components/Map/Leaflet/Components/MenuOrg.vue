<template>
  <div>
  <Menu
    ref="menu"
    :menuItems='menu_items'
    @click='menu_on_click'
  />
  </div>
</template>

<script>
import {
  mapGetters,
  mapActions,
} from 'vuex';

import Menu from '@/components/Map/Leaflet/Components/Menu';

export default {
  name: 'MenuOrg',

  components: {
    Menu,
  },

  data() {
    return {
      menu_items: [
        {
          title: 'ПОДЛОЖКА',
        },
        {
          title: 'ЭЛЕМЕНТЫ',
          menu: [
            {
              icon:        'mdi-calendar-range',
              title:       'Дата-время',
              subtitle:    'Фильтр отображаемых данных по дате-времени',
            },
            {
              icon:        'mdi-google-circles-group',
              title:       'Группировка маркеров',
              subtitle:    'Объединять близлежащие маркеры в группы',
            },
          ],
        },




        {
          title: "Menu Item 1",
          action: () => {
            console.log("menu-item-1");
          }
        },
        { divider: true },
        { title: "Menu Item 2" },
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
        {
          title: "Menu Item 4",
          action: () => {
            console.log("menu-item-4");
          }
        },
        {
          title: "Menu Item 5",
          action: () => {
            console.log("menu-item-5");
          }
        }
      ],

    };
  },

  methods: {
    menu_on_click (item) {
      console.log(2222, item)
      if (item.action) { item.action() }
    },
    menu_show(x, y) {
      this.$refs.menu.activate_root(x, y);
    },
  },

}

</script>
