<script>
import {mapActions} from "vuex";

export default {
  name: "bodyContextMenu",
  data: () => ({
    objectWithActivatedMenu: null,
  }),
  computed: {
    changeTitle: {
      get: function () { return this.objectWithActivatedMenu.object.showTitle },
      set: function (value) { this.objectWithActivatedMenu.object.showTitle = value }
    },
    changeTooltip: {
      get: function () { return this.objectWithActivatedMenu.object.showTooltip },
      set: function (value) { this.objectWithActivatedMenu.object.showTooltip = value }
    },
    changeTriggers: {
      get: function () { return this.objectWithActivatedMenu.object.showTriggers },
      set: function (value) { this.objectWithActivatedMenu.object.showTriggers = value }
    },
    contextMenu: function () {
      if(this.objectWithActivatedMenu){
        return [
          {
            icon: 'mdi-pencil',
            title: 'Изменить',
            subtitle: 'Редактировать данный объект',
            action: 'setChangeObject'
          },
          {
            icon: 'mdi-cog-outline',
            title: 'Настройки',
            subtitle: 'Индивидуальные настройки объекта',
            menu: [
              {
                title: 'Отображение',
                menu: [
                  {
                    title: 'Подпись',
                    model: 'changeTitle',
                  },
                  {
                    title: 'Заголовок',
                    model: 'changeTooltip'
                  },
                  {
                    title: 'Триггеры',
                    model: 'changeTriggers'
                  }
                ]
              },
              {
                title: 'Классификаторы',
              },
            ],
          }
        ]
      } else {
        return [
          {
            icon: 'mdi-pencil',
            title: 'Переупорядочить граф',
            subtitle: 'Переупорядочить граф',
            action: 'reorderGraph'
          },
        ]
      }
    }
  },
  methods: {
    ...mapActions(['reorderGraph']),
    menuShow(event, object=null) {
      this.objectWithActivatedMenu = object
      this.$refs.contextMenu.show_root(event.x, event.y)
    },
    setChangeObject(event) {
      console.log(event)
    },
  },

}
</script>

