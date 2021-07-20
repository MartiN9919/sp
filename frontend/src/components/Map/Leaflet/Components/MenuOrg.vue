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
          name: "Menu Item 1",
          action: () => {
            console.log("menu-item-1");
          }
        },
        { divider: true },
        { name: "Menu Item 2" },
        {
          name: "Sub 1",
          menu: [
            { name: "1.1" },
            { name: "1.2" },
            {
              name: "Sub-menu 2",
              menu: [
                { name: "2.1" },
                { name: "2.2" },
                {
                  name: "Sub-menu 3",
                  menu: [
                    { name: "3.1" },
                    { name: "3.2" },
                    {
                      name: "Sub-menu 4",
                      menu: [{ name: "4.1" }, { name: "4.2" }, { name: "4.3" }]
                    }
                  ]
                }
              ]
            }
          ],
        },

        { name: "Menu Item 3" },
        { divider: true },
        {
          name: "Menu Item 4",
          action: () => {
            console.log("menu-item-4");
          }
        },
        {
          name: "Menu Item 5",
          action: () => {
            console.log("menu-item-5");
          }
        }
      ],


      // menu: {
      //   visible:  false,
      //   x:        0,
      //   y:        0,
      // },

      hover_map_ind:     -1,      // MAP_ITEM[hover_map_ind]                   - блок, над которым находится курсор
      hover_feature_ind: -1,      // MAP_ITEM[].FC.features[hover_feature_ind] - фигура, над которой находится курсор

      mapOptions: {
        zoomControl: false,
        zoomSnap:    0.5,
      },
    };
  },

  methods: {
    menu_on_click (item) {
      console.log(2222, item)
      if (item.action) { item.action() }
    },
    menu_show(x, y) {
      console.log(1111, x, y)
      this.$refs.menu.activate_root(x, y);
    },
    // menu_show(e) {
    //   e.originalEvent.preventDefault();
    //   e.originalEvent.stopPropagation();
    //   this.$refs.menu.activate_root(e.originalEvent.clientX, e.originalEvent.clientY);
    // },
  },

}

</script>
