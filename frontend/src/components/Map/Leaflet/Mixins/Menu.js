import contextMenuNested from '@/components/WebsiteShell/UIMainComponents/contextMenuNested';
import MixMenuTest       from '@/components/Map/Leaflet/Mixins/Menu.test';
import MixMenuMap        from '@/components/Map/Leaflet/Mixins/Menu.map';
import MixMenuSet        from '@/components/Map/Leaflet/Mixins/Menu.set';
import MixMenuPos        from '@/components/Map/Leaflet/Mixins/Menu.pos';

export default {
  mixins: [ MixMenuTest, MixMenuMap, MixMenuSet, MixMenuPos, ],
  components: { contextMenuNested, },

  data: () => ({
    menu_struct: undefined,
  }),

  computed: {
    form: vm => vm,
  },


  methods: {
    // ВАЖНО
    // вызывать из родительского mounted или method.onMapReady
    // должна быть установлена переменная this.map
    mounted_menu() {
      this.mounted_menu_set();
    //this.mounted_menu_map();
      this.mounted_menu_pos();
      this.mounted_menu_test();
    },

    // Показать первый уровень меню, вызывается из родителя
    on_menu_show(e, mode) {
      e.originalEvent.preventDefault();
      e.originalEvent.stopPropagation();

      // сформировать меню
      this.menu_struct = [];
      if (mode!='editor') {
        this.menu_struct.splice(0, 0, this.menu_test_add());                // добавить menu.test (тесты)
        this.menu_struct.splice(0, 0, { divider: true });
      }
      this.menu_struct.splice(0, 0, this.menu_set_add());                   // добавить menu.set (оформление)
      this.menu_struct.splice(0, 0, this.menu_map_add());                   // добавить menu.map (подложка)
      this.menu_struct.splice(0, 0, this.menu_pos_add());                   // добавить menu.pos (фрагмент)

      // показать корневой уровень меню
      this.$refs.menu.show_root(e.originalEvent.clientX, e.originalEvent.clientY);
    },
  },

}
