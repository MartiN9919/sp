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
        let array = [{
            icon: 'mdi-pencil',
            title: 'Переупорядочить граф',
            subtitle: 'Переупорядочить граф',
            action: 'reorderGraph'
          }]
        this.checkRelationCreateStatus() ? array.push({
            icon: 'mdi-check',
            title: 'Создать связь',
            subtitle: 'Связать выбранные объекты',
            action: 'createRelation'
        }) : null
        return array
      }
    }
  },
  methods: {
    ...mapActions(['reorderGraph', 'setEditableRelation']),
    menuShow(event, object=null) {
      this.objectWithActivatedMenu = object
      this.$refs.contextMenu.show_root(event.x, event.y)
    },
    setChangeObject(event) {
      console.log(event)
    },
    checkRelationCreateStatus(){
      if(this.choosingObjects.length === 2){
        return true
      }
      if(this.choosingObjects.length === 3 && this.choosingObjects.findIndex(o => o.object.object.id === 20) !== -1){
        return true
      }
    },
    createRelation(){
      let edge = this.graphRelations.find(edge =>  this.choosingObjects.includes(edge.relation.o1) && this.choosingObjects.includes(edge.relation.o2))
      this.setEditableRelation(edge.relation)
    },
  },

}
</script>

