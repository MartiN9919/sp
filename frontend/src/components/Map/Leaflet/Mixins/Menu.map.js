import { mapGetters, mapActions } from 'vuex';

export default {
  computed: {
    ...mapGetters([
      'MAP_GET_TILES',
      'MAP_GET_TILE',
    ]),

    prop_tile: {
      set: function(val) { this.MAP_ACT_TILE({ind: val}); },
      get: function()    { return this.MAP_GET_TILE; },
    },
  },

  methods: {
    ...mapActions([
      'MAP_ACT_TILE',
    ]),

    // добавить в контекстное меню
    menu_map_add() {
      let val = {
        icon:     'mdi-map-outline',
        title:    'Подложка',
        subtitle: 'Фон карты',
        menu:     [
          {
            model: 'prop_tile',
          },
        ],
      };
      val.menu[0]['radio'] = this.MAP_GET_TILES;       // добавить выбор тайлов
      return val;
    },
  },
}
